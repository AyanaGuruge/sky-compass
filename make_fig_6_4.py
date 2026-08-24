"""
make_fig_6_4.py

Build the annotated figure for Section 6.4 from the first sky frame recorded
through the polarising dome.

Nothing in the photograph is altered. The image data is drawn exactly as
captured; every mark is an overlay, and the per-gore levels in the right hand
panel are measured from the unmodified pixels by this script. Re-running it
reproduces the figure and the numbers together, so the caption can never drift
away from the data.

    python3 make_fig_6_4.py

Geometry
    The eight gore seams were fitted as eight bright ridges 45 degrees apart
    radiating from a common apex, searching over apex position and rotation.
    The camera heading was recovered from the solar glare in the same frame and
    is uncertain by roughly +/- 20 degrees, which is half a gore; that caveat
    belongs in the caption and is printed by this script.
"""

from __future__ import annotations

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

FRAME = "captures/2026-07-31_dome/dome_exp0012_20260731T130604Z.png"
OUT = "Doc images/NEW_fig_6_4_dome_frame_annotated.png"

SUN_AZ, SUN_EL = 228.5, 40.2      # ephemeris, 2026-07-31 13:06 UTC, Turku
HEADING = 196.2                   # image up, degrees from North, from the glare
HEADING_ERR = 20.0
APEX = (765.0, 545.0)             # fitted dome apex, pixels
SEAM0 = 16.0                      # first seam, degrees ccw from image +x
R_IN, R_OUT = 90.0, 300.0         # analysis annulus about the apex
SKY_LEVEL = 60.0                  # below this is tree, building or vignette

# categorical slots 1 and 2 of the reference palette
BLUE, ORANGE = "#2a78d6", "#eb6834"
GREY = "#9a9a95"
INK, MUTED = "#0b0b0b", "#52514e"


def polar(ax, ay, r, phi_deg):
    """Pixel coordinates at radius r and angle phi (ccw from +x, image y up)."""
    a = np.deg2rad(phi_deg)
    return ax + r * np.cos(a), ay - r * np.sin(a)


def main():
    gray = np.asarray(Image.open(FRAME).convert("L"), dtype=np.float32)
    h, w = gray.shape
    ax_, ay_ = APEX

    ys, xs = np.mgrid[0:h, 0:w].astype(float)
    rho = np.hypot(xs - ax_, ay_ - ys)
    phi = np.degrees(np.arctan2(ay_ - ys, xs - ax_)) % 360.0
    annulus = (rho > R_IN) & (rho < R_OUT)
    sky = annulus & (gray > SKY_LEVEL)

    anti = (SUN_AZ + 180.0) % 360.0
    gores = []
    for k in range(8):
        a0 = (SEAM0 + 45.0 * k) % 360.0
        mid = (a0 + 22.5) % 360.0
        caz = (HEADING + 90.0 - mid) % 360.0
        sel = sky & (((phi - a0) % 360.0) < 45.0)
        cover = sel.sum() / max((annulus & (((phi - a0) % 360.0) < 45.0)).sum(), 1)
        gores.append({
            "name": "G%d" % (k + 1), "a0": a0, "mid": mid, "az": caz,
            "mean": float(gray[sel].mean()), "cover": cover,
            "d_anti": min(abs(caz - anti), 360 - abs(caz - anti)),
            "d_sun": min(abs(caz - SUN_AZ), 360 - abs(caz - SUN_AZ)),
        })

    dark = sorted(gores, key=lambda g: g["d_anti"])[:2]
    lit = sorted(gores, key=lambda g: g["d_sun"])[:2]
    dark_names = {g["name"] for g in dark}
    lit_names = {g["name"] for g in lit}

    for g in gores:
        g["color"] = (ORANGE if g["name"] in dark_names
                      else BLUE if g["name"] in lit_names else GREY)

    fig = plt.figure(figsize=(13.0, 6.8), facecolor="white")
    gs = fig.add_gridspec(1, 2, width_ratios=[1.24, 1.0], wspace=0.30,
                          left=0.03, right=0.975, top=0.90, bottom=0.19)

    # ---------------- left: the photograph, unaltered, with overlays --------
    a = fig.add_subplot(gs[0, 0])
    a.imshow(gray, cmap="gray", vmin=0, vmax=255, interpolation="nearest")
    a.set_xlim(150, 1450)
    a.set_ylim(1150, 20)
    a.set_xticks([])
    a.set_yticks([])
    for s in a.spines.values():
        s.set_visible(False)

    # seams
    for k in range(8):
        s = (SEAM0 + 45.0 * k) % 360.0
        x0, y0 = polar(ax_, ay_, R_IN * 0.45, s)
        x1, y1 = polar(ax_, ay_, R_OUT * 1.18, s)
        a.plot([x0, x1], [y0, y1], color="white", lw=0.9, ls=(0, (5, 4)),
               alpha=0.75, zorder=3)

    # highlighted gores: closed outline, no fill over the data
    arc = np.linspace(0, 45, 80)
    for g in gores:
        if g["color"] is GREY:
            continue
        t = (g["a0"] + arc) % 360.0
        xo, yo = polar(ax_, ay_, R_OUT, t)
        xi, yi = polar(ax_, ay_, R_IN, t)
        px = np.concatenate([xo, xi[::-1], xo[:1]])
        py = np.concatenate([yo, yi[::-1], yo[:1]])
        a.plot(px, py, color=g["color"], lw=2.0, zorder=5,
               solid_joinstyle="round")

    # apex
    a.plot([ax_], [ay_], marker="+", ms=13, mew=1.8, color="white", zorder=6)

    # antisolar and solar bearings
    for az_, col, lab in ((anti, ORANGE, "antisolar\n%.0f$\\degree$" % anti),
                          (SUN_AZ, BLUE, "sun\n%.0f$\\degree$" % SUN_AZ)):
        p = (HEADING + 90.0 - az_) % 360.0
        x0, y0 = polar(ax_, ay_, R_OUT * 1.12, p)
        x1, y1 = polar(ax_, ay_, R_OUT * 1.46, p)
        a.annotate("", xy=(x1, y1), xytext=(x0, y0),
                   arrowprops=dict(arrowstyle="-|>", color=col, lw=2.0,
                                   mutation_scale=17), zorder=6)
        xt, yt = polar(ax_, ay_, R_OUT * 1.60, p)
        a.text(xt, yt, lab, color=col, fontsize=9.5, ha="center", va="center",
               linespacing=1.25, zorder=6,
               bbox=dict(fc="white", ec="none", alpha=0.82, pad=1.6))

    # gore labels
    for g in gores:
        xt, yt = polar(ax_, ay_, R_OUT * 0.79, g["mid"])
        a.text(xt, yt, g["name"], color="white", fontsize=9.5, fontweight="bold",
               ha="center", va="center", zorder=6,
               bbox=dict(boxstyle="round,pad=0.22", fc="black", ec="none",
                         alpha=0.42))

    a.set_title("Frame recorded through the dome, unmodified",
                fontsize=11.5, color=INK, pad=9, loc="left")
    a.text(0.0, -0.035,
           "31 July 2026, 13:06 UTC  ·  exposure 1.2 ms, gain 0  ·  "
           "seams dashed, apex +, analysis annulus 90–300 px",
           transform=a.transAxes, fontsize=8.6, color=MUTED, va="top")

    # ---------------- right: measured level per gore ------------------------
    b = fig.add_subplot(gs[0, 1])
    order = list(range(8))
    ypos = np.arange(8)[::-1]
    vals = [gores[k]["mean"] for k in order]
    cols = [gores[k]["color"] for k in order]

    b.barh(ypos, vals, height=0.62, color=cols, zorder=3)
    # gore name and its metadata live in two right-aligned columns outside the
    # axes, so neither can collide with the other however long the values run.
    lab_tr = matplotlib.transforms.blended_transform_factory(
        b.transAxes, b.transData)
    for y, k in zip(ypos, order):
        g = gores[k]
        b.text(g["mean"] + 3.5, y, "%.1f" % g["mean"], va="center", ha="left",
               fontsize=9.6, color=INK, zorder=4)
        b.text(-0.015, y, g["name"], transform=lab_tr, va="center", ha="right",
               fontsize=9.6, color=INK, fontweight="bold")
        b.text(-0.065, y, "az %3.0f$\\degree$    %2.0f%% sky"
               % (g["az"], 100 * g["cover"]), transform=lab_tr, va="center",
               ha="right", fontsize=8.4, color=MUTED)

    b.set_xlim(0, 258)
    b.set_ylim(-0.75, 7.75)
    b.set_yticks([])
    b.set_xlabel("mean level over sky pixels (0–255)", fontsize=9.6,
                 color=MUTED)
    b.tick_params(axis="x", labelsize=9, colors=MUTED, length=3)
    b.xaxis.grid(True, color="#e6e6e2", lw=0.8, zorder=0)
    b.set_axisbelow(True)
    for s in ("top", "right", "left"):
        b.spines[s].set_visible(False)
    b.spines["bottom"].set_color("#d8d8d3")

    ratio = max(vals) / min(vals)
    b.set_title("Measured level per gore", fontsize=11.5, color=INK, pad=9,
                loc="left")

    fig.text(0.03, 0.125,
             "orange: the antisolar pair, predicted darkest before the data "
             "was examined   ·   blue: the solar pair   ·   ratio %.1f×"
             % ratio, fontsize=8.8, color=INK, va="top")
    fig.text(0.03, 0.083,
             "Sky was broken to overcast. Cloud alone produces a comparable "
             "bright-toward-sun gradient, so this ordering is consistent with "
             "the model but is not by itself a measurement of sky polarisation.",
             fontsize=8.4, color=MUTED, va="top")
    fig.text(0.03, 0.045,
             "No shading or contrast adjustment has been applied to the image "
             "data; every mark on the photograph is an overlay.",
             fontsize=8.4, color=MUTED, va="top")

    fig.savefig(OUT, dpi=300, facecolor="white")
    print("wrote", OUT)
    print("\npredicted darkest (antisolar): %s"
          % ", ".join(g["name"] for g in dark))
    print("predicted brightest (solar)  : %s"
          % ", ".join(g["name"] for g in lit))
    print("\n%-5s %8s %8s %8s %8s" % ("gore", "az", "mean", "cover", "d_anti"))
    for g in sorted(gores, key=lambda g: g["mean"]):
        print("%-5s %7.0f%s %8.1f %7.0f%% %7.0f%s"
              % (g["name"], g["az"], "°", g["mean"], 100 * g["cover"],
                 g["d_anti"], "°"))
    print("\nmeasured darkest: %s  (ratio %.2f against the brightest)"
          % (", ".join(g["name"] for g in sorted(gores,
                                                 key=lambda g: g["mean"])[:2]),
             ratio))
    print("heading uncertain by +/-%.0f deg, half a gore" % HEADING_ERR)


if __name__ == "__main__":
    main()
