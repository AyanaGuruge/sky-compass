"""
turku_sun.py

Solar position for Turku, Finland, following the NOAA solar calculation
(after Meeus, Astronomical Algorithms). This is the independent ground truth
model referred to in section 3.1 of the thesis. It is deliberately kept
separate from the supervisor's MATLAB derivation so that the two can be
compared against each other.

Azimuth convention
    Azimuth is measured in degrees CLOCKWISE FROM NORTH, so North is 0,
    East is 90, South is 180, and West is 270. This is the robot heading
    convention and it is the convention used by every downstream tool in this
    project, meaning the synthetic generator, the capture labelling, and the
    estimator.

    The supervisor's MATLAB model measures azimuth from SOUTH toward West.
    The two differ by a fixed rotation of 180 degrees:

        azimuth_north = (azimuth_south + 180) mod 360

    Both models are correct. Never mix them silently, because a mixed
    convention still runs and still returns a plausible number.

Validation targets (all computed by the self test at the bottom)
    Winter solstice, local solar noon:  elevation  90 - 60.45 - 23.44 = 6.11 deg
    Summer solstice, local solar noon:  elevation  90 - 60.45 + 23.44 = 52.99 deg
    At local solar noon the sun is due South, so azimuth is close to 180 deg.

Usage
    from turku_sun import sun_position
    az, el = sun_position(datetime(2026, 7, 24, 12, 0, tzinfo=timezone.utc))

Dependencies
    standard library only.
"""

from __future__ import annotations

import csv
import math
from datetime import datetime, timedelta, timezone

# Site constants, Turku, Iso-Heikkila
LAT_DEG = 60.4520
LON_DEG = 22.2298  # East positive


def _julian_day(dt_utc: datetime) -> float:
    """Julian day number, including the fractional part, from a UTC datetime."""
    if dt_utc.tzinfo is None:
        dt_utc = dt_utc.replace(tzinfo=timezone.utc)
    dt_utc = dt_utc.astimezone(timezone.utc)

    year, month = dt_utc.year, dt_utc.month
    day = dt_utc.day
    if month <= 2:
        year -= 1
        month += 12
    a = year // 100
    b = 2 - a + a // 4
    jd0 = (math.floor(365.25 * (year + 4716))
           + math.floor(30.6001 * (month + 1))
           + day + b - 1524.5)
    frac = (dt_utc.hour + dt_utc.minute / 60.0
            + (dt_utc.second + dt_utc.microsecond / 1e6) / 3600.0) / 24.0
    return jd0 + frac


def sun_position(dt_utc: datetime,
                 lat_deg: float = LAT_DEG,
                 lon_deg: float = LON_DEG,
                 refraction: bool = True):
    """Return (azimuth_deg_from_north, elevation_deg) for a UTC datetime.

    Elevation is the apparent elevation above the horizon when refraction is
    True, and the geometric elevation when it is False. The validation figures
    quoted in the thesis are geometric, so the self test calls this with
    refraction set to False.
    """
    jd = _julian_day(dt_utc)
    t = (jd - 2451545.0) / 36525.0  # Julian centuries since J2000.0

    # Geometric mean longitude and mean anomaly of the sun
    l0 = (280.46646 + t * (36000.76983 + t * 0.0003032)) % 360.0
    m = 357.52911 + t * (35999.05029 - 0.0001537 * t)
    m_rad = math.radians(m)

    # Orbital eccentricity and the equation of the centre
    ecc = 0.016708634 - t * (0.000042037 + 0.0000001267 * t)
    c = (math.sin(m_rad) * (1.914602 - t * (0.004817 + 0.000014 * t))
         + math.sin(2 * m_rad) * (0.019993 - 0.000101 * t)
         + math.sin(3 * m_rad) * 0.000289)

    true_long = l0 + c
    omega = 125.04 - 1934.136 * t
    app_long = true_long - 0.00569 - 0.00478 * math.sin(math.radians(omega))

    # Obliquity of the ecliptic, with the nutation correction
    seconds = 21.448 - t * (46.815 + t * (0.00059 - t * 0.001813))
    eps0 = 23.0 + (26.0 + seconds / 60.0) / 60.0
    eps = eps0 + 0.00256 * math.cos(math.radians(omega))
    eps_rad = math.radians(eps)

    # Declination
    decl_rad = math.asin(math.sin(eps_rad) * math.sin(math.radians(app_long)))

    # Equation of time, in minutes
    y = math.tan(eps_rad / 2.0) ** 2
    l0_rad = math.radians(l0)
    eq_time = 4.0 * math.degrees(
        y * math.sin(2 * l0_rad)
        - 2.0 * ecc * math.sin(m_rad)
        + 4.0 * ecc * y * math.sin(m_rad) * math.cos(2 * l0_rad)
        - 0.5 * y * y * math.sin(4 * l0_rad)
        - 1.25 * ecc * ecc * math.sin(2 * m_rad)
    )

    # True solar time and hour angle
    minutes_utc = (dt_utc.astimezone(timezone.utc).hour * 60.0
                   + dt_utc.astimezone(timezone.utc).minute
                   + dt_utc.astimezone(timezone.utc).second / 60.0)
    true_solar_time = (minutes_utc + eq_time + 4.0 * lon_deg) % 1440.0
    hour_angle = true_solar_time / 4.0 - 180.0
    ha_rad = math.radians(hour_angle)

    lat_rad = math.radians(lat_deg)
    cos_zenith = (math.sin(lat_rad) * math.sin(decl_rad)
                  + math.cos(lat_rad) * math.cos(decl_rad) * math.cos(ha_rad))
    cos_zenith = max(-1.0, min(1.0, cos_zenith))
    zenith_rad = math.acos(cos_zenith)
    elevation = 90.0 - math.degrees(zenith_rad)

    # Atmospheric refraction, the standard NOAA piecewise approximation
    if refraction and elevation > -1.0:
        e = elevation
        if e > 85.0:
            corr = 0.0
        elif e > 5.0:
            te = math.tan(math.radians(e))
            corr = (58.1 / te - 0.07 / te ** 3 + 0.000086 / te ** 5) / 3600.0
        elif e > -0.575:
            corr = (1735.0 + e * (-518.2 + e * (103.4 + e * (-12.79 + e * 0.711)))) / 3600.0
        else:
            corr = (-20.772 / math.tan(math.radians(e))) / 3600.0
        elevation += corr

    # Azimuth, clockwise from North
    denom = math.cos(lat_rad) * math.sin(zenith_rad)
    if abs(denom) < 1e-12:
        azimuth = 180.0
    else:
        arg = ((math.sin(lat_rad) * cos_zenith) - math.sin(decl_rad)) / denom
        arg = max(-1.0, min(1.0, arg))
        if hour_angle > 0.0:
            azimuth = (math.degrees(math.acos(arg)) + 180.0) % 360.0
        else:
            azimuth = (540.0 - math.degrees(math.acos(arg))) % 360.0

    return azimuth, elevation


def azimuth_south_to_north(az_south_deg: float) -> float:
    """Convert the supervisor's South referenced azimuth to the North one."""
    return (az_south_deg + 180.0) % 360.0


def azimuth_north_to_south(az_north_deg: float) -> float:
    """Convert a North referenced azimuth to the supervisor's South one."""
    return (az_north_deg + 180.0) % 360.0


def generate_history(start: datetime, end: datetime, step_minutes: int = 10,
                     min_elevation_deg: float = 0.0):
    """Yield (utc_datetime, azimuth_deg, elevation_deg) over a date range.

    Only positions above min_elevation_deg are returned, so the output is a
    daylight only table.
    """
    if start.tzinfo is None:
        start = start.replace(tzinfo=timezone.utc)
    if end.tzinfo is None:
        end = end.replace(tzinfo=timezone.utc)
    step = timedelta(minutes=step_minutes)
    t = start
    while t <= end:
        az, el = sun_position(t)
        if el >= min_elevation_deg:
            yield t, az, el
        t += step


def write_history_csv(path: str, start: datetime, end: datetime,
                      step_minutes: int = 10, min_elevation_deg: float = 0.0) -> int:
    """Write a daylight sun position table to CSV and return the row count."""
    n = 0
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["utc_iso", "sun_az_deg_from_north", "sun_el_deg"])
        for t, az, el in generate_history(start, end, step_minutes, min_elevation_deg):
            w.writerow([t.strftime("%Y-%m-%dT%H:%M:%SZ"), round(az, 4), round(el, 4)])
            n += 1
    return n


def solar_noon_utc(date_utc: datetime) -> datetime:
    """Find the UTC time of highest elevation on a given date, to the minute."""
    base = date_utc.replace(hour=0, minute=0, second=0, microsecond=0,
                            tzinfo=timezone.utc)
    best_t, best_el = base, -90.0
    for minute in range(0, 1440):
        t = base + timedelta(minutes=minute)
        _, el = sun_position(t, refraction=False)
        if el > best_el:
            best_el, best_t = el, t
    return best_t


if __name__ == "__main__":
    print("turku_sun.py self test, latitude {:.4f}, longitude {:.4f}".format(
        LAT_DEG, LON_DEG))
    print()

    checks = [
        ("winter solstice 2025", datetime(2025, 12, 21, tzinfo=timezone.utc),
         90.0 - LAT_DEG - 23.44),
        ("summer solstice 2026", datetime(2026, 6, 21, tzinfo=timezone.utc),
         90.0 - LAT_DEG + 23.44),
    ]
    for label, day, expected in checks:
        noon = solar_noon_utc(day)
        az, el = sun_position(noon, refraction=False)
        print("{:22s} solar noon {} UTC".format(label, noon.strftime("%H:%M")))
        print("    elevation {:7.3f} deg, expected about {:6.3f}, difference {:5.3f}"
              .format(el, expected, abs(el - expected)))
        print("    azimuth   {:7.3f} deg from North, expected close to 180.000"
              .format(az))
        assert abs(el - expected) < 0.25, "elevation check failed for " + label
        assert abs(az - 180.0) < 0.5, "azimuth check failed for " + label
    print()

    az, el = sun_position(datetime(2026, 7, 24, 9, 0, tzinfo=timezone.utc))
    print("24 July 2026, 09:00 UTC (12:00 Finnish summer time)")
    print("    azimuth {:.2f} deg from North, elevation {:.2f} deg".format(az, el))
    print("    the same azimuth in the supervisor South convention is {:.2f} deg"
          .format(azimuth_north_to_south(az)))
    print()
    print("All checks passed.")
