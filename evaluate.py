"""
evaluate.py

Quantify how accurately the estimator recovers the sun azimuth, using
synthetic frames rendered at real Turku sun positions. This produces the
numbers and the figures for the simulation accuracy section of the results
chapter, and it runs regardless of the weather, so the thesis is never blocked
waiting for a clear sky.

Noise model
    Three degradations are applied so the synthetic frames are not unrealistically
    clean. Sensor noise is added as zero mean Gaussian noise. Cloud is modelled
    by reducing the maximum degree of polarisation, since cloud depolarises the
    sky, and by adding a smooth large scale brightness gradient of the kind that
    an overcast sky produces. The severity of both is a command line argument,
    so the accuracy can be reported as a function of sky condition, which is
    what section 6.5 of the thesis needs.

Usage
    python3 evaluate.py                          clear sky baseline
    python3 evaluate.py --dmax 0.3 --clutter 0.3 hazy or thin cloud
    python3 evaluate.py --dmax 0.1 --clutter 0.6 heavy cloud
    python3 evaluate.py --radial                 the gore dome instead of a flat filter
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone

import numpy as np

from estimate_azimuth import angular_error, estimate
from skyframe import analysis_mask
from synthetic_sky_polarizer import make_sky_image
from turku_sun import generate_history

SIZE = 128


def sample_real_sun_positions(n, start, end, step_minutes=10, seed=0):
    """Draw n sun positions at random from the real Turku daylight history."""
    table = [(az, el) for _, az, el in
             generate_history(start, end, step_minutes, min_elevation_deg=5.0)]
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(table), size=min(n, len(table)), replace=False)
    return [table[i] for i in idx], len(table)


def degrade(img, mask, rng, noise=0.02, clutter=0.0):
    """Add sensor noise and a smooth brightness gradient to a rendered frame."""
    out = img.copy()
    if clutter > 0:
        size = img.shape[0]
        ys, xs = np.mgrid[0:size, 0:size].astype(float) / size
        a, b, c = rng.uniform(-1, 1, size=3)
        gradient = a * xs + b * ys + c * (xs * ys)
        gradient = gradient / (np.abs(gradient).max() + 1e-9)
        out = out + clutter * 0.5 * gradient
    if noise > 0:
        out = out + rng.normal(0.0, noise, size=img.shape)
    out = np.clip(out, 0.0, None)
    out[~mask] = 0.0
    return out


def run(n=60, dmax=0.75, noise=0.02, clutter=0.0, radial=False,
        axis_deg=35.0, up_az=0.0, step_deg=2.0, seed=1, plot=True):
    start = datetime(2026, 5, 14, tzinfo=timezone.utc)
    end = datetime(2026, 7, 14, tzinfo=timezone.utc)
    positions, total = sample_real_sun_positions(n, start, end, seed=seed)
    print("drew {} test positions from {} real daylight sun positions "
          "between {} and {}".format(len(positions), total,
                                     start.date(), end.date()))
    print("optic: {}, film axis {:.0f} deg, image up heading {:.0f} deg"
          .format("radial gore dome" if radial else "flat filter",
                  axis_deg, up_az))
    print("sky:   d_max {:.2f}, sensor noise {:.3f}, clutter {:.2f}"
          .format(dmax, noise, clutter))
    print()

    rng = np.random.default_rng(seed + 100)
    errors, elevations, confidences = [], [], []
    for az_true, el_true in positions:
        img, _, _, dmask = make_sky_image(
            size=SIZE, sun_az_deg=az_true, sun_el_deg=el_true,
            polariser_axis_deg=axis_deg, image_up_azimuth_deg=up_az,
            d_max=dmax, radial_axis=radial)
        img = degrade(img, dmask, rng, noise=noise, clutter=clutter)
        amask = analysis_mask(SIZE, dmask, horizon_margin_deg=15.0)
        az_rel, conf, _ = estimate(img, amask, el_true, axis_deg=axis_deg,
                                   radial=radial, step_deg=step_deg)
        az_est = (az_rel + up_az) % 360.0
        errors.append(angular_error(az_est, az_true))
        elevations.append(el_true)
        confidences.append(conf)

    errors = np.array(errors)
    elevations = np.array(elevations)
    confidences = np.array(confidences)

    print("mean absolute error   {:7.3f} deg".format(errors.mean()))
    print("median absolute error {:7.3f} deg".format(np.median(errors)))
    print("90th percentile       {:7.3f} deg".format(np.percentile(errors, 90)))
    print("worst case            {:7.3f} deg".format(errors.max()))
    print("fraction within 5 deg {:7.1f} percent"
          .format(100.0 * (errors < 5.0).mean()))
    print("mean confidence       {:7.2f}".format(confidences.mean()))

    gross = errors > 45.0
    if gross.any():
        print()
        print("{} of {} estimates are gross failures above 45 degrees, which is "
              "the solar and antisolar ambiguity discussed in the limitations "
              "section".format(int(gross.sum()), len(errors)))

    if plot:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 2, figsize=(11, 4))
        axes[0].hist(errors, bins=24, color="#3b82f6", edgecolor="white")
        axes[0].set_xlabel("absolute azimuth error, degrees")
        axes[0].set_ylabel("frames")
        axes[0].set_title("Error distribution")
        axes[1].scatter(elevations, errors, s=22, color="#3b82f6", alpha=0.8)
        axes[1].set_xlabel("sun elevation, degrees")
        axes[1].set_ylabel("absolute azimuth error, degrees")
        axes[1].set_title("Error against sun elevation")
        fig.suptitle("Model based azimuth estimation, {}, d_max {:.2f}, "
                     "clutter {:.2f}".format(
                         "radial dome" if radial else "flat filter", dmax, clutter))
        fig.tight_layout()
        name = "accuracy_{}_dmax{:.2f}_clutter{:.2f}.png".format(
            "radial" if radial else "flat", dmax, clutter)
        fig.savefig(name, dpi=110)
        print()
        print("figure written to " + name)
    return errors


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=60)
    ap.add_argument("--dmax", type=float, default=0.75)
    ap.add_argument("--noise", type=float, default=0.02)
    ap.add_argument("--clutter", type=float, default=0.0)
    ap.add_argument("--radial", action="store_true")
    ap.add_argument("--axis", type=float, default=35.0)
    ap.add_argument("--up", type=float, default=0.0)
    ap.add_argument("--step", type=float, default=2.0)
    ap.add_argument("--no-plot", action="store_true")
    a = ap.parse_args()
    run(n=a.n, dmax=a.dmax, noise=a.noise, clutter=a.clutter, radial=a.radial,
        axis_deg=a.axis, up_az=a.up, step_deg=a.step, plot=not a.no_plot)
