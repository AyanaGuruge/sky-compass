"""
make_figures.py

Regenerate the three figures the results chapter refers to. They were produced
in an earlier session and were not kept, so this script rebuilds them from the
solar model and the generator, which means they can always be reproduced and
the thesis never depends on a file that cannot be regenerated.

    turku_sun_coverage.png        the range of sun positions the method has to
                                  handle over two months at Turku
    polarizer_band_demo.png       the flat filter against the radial gore dome,
                                  showing that the radial axis aligns the dark
                                  axis of the image with the solar meridian. The
                                  darker of its two ends is the antisolar one,
                                  not the solar one; verified by binning the
                                  rendered image into azimuth wedges.
    matched_synthetic_example.png a real timestamp turned into a synthetic frame
    sun_position_validation.png   the model against its own analytic solstice
                                  reference values across a year

Usage
    python3 make_figures.py
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from synthetic_sky_polarizer import make_sky_image, sun_pixel
from turku_sun import LAT_DEG, generate_history, solar_noon_utc, sun_position

SIZE = 320


def fig_coverage():
    start = datetime(2026, 5, 14, tzinfo=timezone.utc)
    end = datetime(2026, 7, 14, tzinfo=timezone.utc)
    rows = list(generate_history(start, end, 10, min_elevation_deg=0.0))
    az = np.array([r[1] for r in rows])
    el = np.array([r[2] for r in rows])
    day = np.array([(r[0] - start).days for r in rows])

    fig = plt.figure(figsize=(12, 5))
    ax1 = fig.add_subplot(1, 2, 1)
    sc = ax1.scatter(az, el, c=day, s=3, cmap="viridis")
    ax1.set_xlabel("sun azimuth, degrees clockwise from North")
    ax1.set_ylabel("sun elevation, degrees")
    ax1.set_xlim(0, 360)
    ax1.set_xticks(range(0, 361, 45))
    ax1.grid(alpha=0.25)
    ax1.set_title("Daylight sun positions, Turku, 14 May to 14 July 2026")
    fig.colorbar(sc, ax=ax1, label="days after 14 May")

    ax2 = fig.add_subplot(1, 2, 2, projection="polar")
    ax2.set_theta_zero_location("N")
    ax2.set_theta_direction(-1)
    ax2.scatter(np.deg2rad(az), 90.0 - el, c=day, s=3, cmap="viridis")
    ax2.set_rlim(0, 90)
    ax2.set_rticks([30, 60, 90])
    ax2.set_yticklabels(["60", "30", "0"])
    ax2.set_title("The same positions on the sky hemisphere\n"
                  "radius is zenith angle, so the centre is overhead")

    fig.suptitle("Azimuth spans {:.0f} to {:.0f} degrees, elevation reaches "
                 "{:.1f} degrees at latitude {:.2f} North"
                 .format(az.min(), az.max(), el.max(), LAT_DEG))
    fig.tight_layout()
    fig.savefig("turku_sun_coverage.png", dpi=120)
    plt.close(fig)
    print("turku_sun_coverage.png   {} daylight positions, azimuth {:.0f} to "
          "{:.0f} deg, elevation up to {:.1f} deg"
          .format(len(rows), az.min(), az.max(), el.max()))


def fig_band_demo():
    az_sun, el_sun = 135.0, 30.0
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.6))
    for ax, radial in zip(axes, (False, True)):
        img, _, _, mask = make_sky_image(
            size=SIZE, sun_az_deg=az_sun, sun_el_deg=el_sun,
            polariser_axis_deg=0.0, image_up_azimuth_deg=0.0,
            radial_axis=radial)
        disp = np.where(mask, img, np.nan)
        ax.imshow(disp, cmap="gray", vmin=0.0, vmax=1.0)

        # the solar meridian, drawn as a diameter so the reader can check where
        # the dark axis actually falls. The antisolar point itself sits below the
        # horizon, so what is marked is the antisolar AZIMUTH at the disc edge.
        cx = cy = SIZE / 2.0 - 0.5
        for a_deg, style, lab in ((az_sun, "-", "toward sun"),
                                  ((az_sun + 180.0) % 360.0, "--", "antisolar azimuth")):
            phi = np.deg2rad(90.0 - a_deg)
            ax.plot([cx, cx + (SIZE / 2.0) * np.cos(phi)],
                    [cy, cy - (SIZE / 2.0) * np.sin(phi)],
                    style, color="#22d3ee", linewidth=1.4, alpha=0.9,
                    label=lab if not radial else None)

        c, r = sun_pixel(SIZE, 180.0, az_sun, el_sun, 0.0)
        ax.plot([c], [r], marker="o", markersize=16, markerfacecolor="none",
                markeredgecolor="red", markeredgewidth=2)
        ax.set_title("radial gore dome" if radial else "single flat filter")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(0.5, -0.06,
                "dark axis follows the solar meridian, darker at the antisolar end"
                if radial
                else "dark band set by the fixed film axis, not by the sun",
                transform=ax.transAxes, ha="center", fontsize=10)
    fig.suptitle("Sky through the polarising optic, sun azimuth {:.0f} deg, "
                 "elevation {:.0f} deg, image up is North.\nThe circle marks the "
                 "true sun; the cyan diameter is the solar meridian, solid toward "
                 "the sun and dashed toward the antisolar azimuth."
                 .format(az_sun, el_sun), fontsize=11)
    axes[0].legend(loc="lower left", fontsize=8, framealpha=0.8)
    fig.tight_layout(rect=(0, 0.05, 1, 0.94))
    fig.savefig("polarizer_band_demo.png", dpi=120)
    plt.close(fig)
    print("polarizer_band_demo.png  flat filter against radial dome at the "
          "same sun position")


def fig_matched_example():
    times = [datetime(2026, 6, 21, h, 0, tzinfo=timezone.utc)
             for h in (3, 7, 11, 15)]
    fig, axes = plt.subplots(1, 4, figsize=(15, 4.4))
    for ax, t in zip(axes, times):
        az, el = sun_position(t)
        img, _, _, mask = make_sky_image(
            size=SIZE, sun_az_deg=az, sun_el_deg=max(el, 0.5),
            polariser_axis_deg=0.0, image_up_azimuth_deg=0.0)
        ax.imshow(np.where(mask, img, np.nan), cmap="gray", vmin=0, vmax=1)
        c, r = sun_pixel(SIZE, 180.0, az, max(el, 0.5), 0.0)
        ax.plot([c], [r], marker="o", markersize=13, markerfacecolor="none",
                markeredgecolor="red", markeredgewidth=1.8)
        ax.set_title("{} UTC\naz {:.0f} deg, el {:.0f} deg"
                     .format(t.strftime("%H:%M"), az, el), fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.suptitle("Synthetic frames rendered at the true Turku sun positions "
                 "for 21 June 2026, single flat filter. Ordinary photographs "
                 "record no polarisation, so labelled frames are produced this "
                 "way from real sun geometry.")
    fig.tight_layout()
    fig.savefig("matched_synthetic_example.png", dpi=120)
    plt.close(fig)
    print("matched_synthetic_example.png  four real timestamps rendered as "
          "synthetic frames")


def fig_validation():
    days, elevs = [], []
    base = datetime(2026, 1, 1, tzinfo=timezone.utc)
    for d in range(0, 365, 5):
        t = solar_noon_utc(base + timedelta(days=d))
        _, el = sun_position(t, refraction=False)
        days.append(d)
        elevs.append(el)
    fig, ax = plt.subplots(figsize=(9, 4.6))
    ax.plot(days, elevs, color="#3b82f6", linewidth=2,
            label="model, elevation at solar noon")
    ax.axhline(90 - LAT_DEG + 23.44, color="#f59e0b", linestyle="--",
               label="analytic summer solstice, {:.2f} deg"
                     .format(90 - LAT_DEG + 23.44))
    ax.axhline(90 - LAT_DEG - 23.44, color="#ef4444", linestyle="--",
               label="analytic winter solstice, {:.2f} deg"
                     .format(90 - LAT_DEG - 23.44))
    ax.set_xlabel("day of 2026")
    ax.set_ylabel("solar noon elevation, degrees")
    ax.set_title("Solar model validated against its analytic solstice values "
                 "at Turku")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig("sun_position_validation.png", dpi=120)
    plt.close(fig)
    print("sun_position_validation.png  noon elevation across the year against "
          "the two analytic reference values")


if __name__ == "__main__":
    fig_coverage()
    fig_band_demo()
    fig_matched_example()
    fig_validation()
    print()
    print("Four figures written into the current directory.")
