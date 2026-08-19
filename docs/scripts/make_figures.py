"""Regenerates the figures embedded in the tutorials.

Each figure is written twice, once for each site theme, as
``<name>-light.png`` and ``<name>-dark.png`` under ``docs/assets/figures/``.
The tutorials reference them with Material's ``#only-light`` and
``#only-dark`` suffixes, so the right one shows in either color scheme.

Run from the repository root, with the ``notebooks`` extra installed:

    python docs/scripts/make_figures.py

Every figure is seeded, so re-running reproduces the committed images
byte-for-byte in content, and a regenerated figure only changes when the
code that draws it changes.
"""

import pathlib

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

import wanderwalk as ww

OUT = pathlib.Path(__file__).resolve().parents[1] / "assets" / "figures"

# Foreground color and particle color per theme. The purples match the
# deep purple primary the Material theme is configured with.
THEMES = {
    "light": {"fg": "#31313a", "particles": "#5e35b1", "grid": "#d5d5dd"},
    "dark": {"fg": "#e3e3ea", "particles": "#b39ddb", "grid": "#4a4a55"},
}


def styled(theme):
    """Returns rcParams that make a transparent figure legible on one theme."""
    c = THEMES[theme]
    return {
        "figure.facecolor": "none",
        "axes.facecolor": "none",
        "savefig.facecolor": "none",
        "savefig.transparent": True,
        "text.color": c["fg"],
        "axes.labelcolor": c["fg"],
        "axes.edgecolor": c["fg"],
        "xtick.color": c["fg"],
        "ytick.color": c["fg"],
        "axes.titlecolor": c["fg"],
        "grid.color": c["grid"],
        "font.size": 11,
        "figure.dpi": 140,
    }


def render(name, draw):
    """Draws one figure once per theme and saves both variants."""
    OUT.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        with plt.rc_context(styled(theme)):
            fig = draw(THEMES[theme])
            path = OUT / f"{name}-{theme}.png"
            fig.savefig(path, bbox_inches="tight", transparent=True)
            plt.close(fig)
            print(f"wrote {path.relative_to(OUT.parents[2])}")


def sphere_scatter(colors):
    np.random.seed(0)
    early = ww.sphere_simulator(T=20, N=1500, dt=0.01, noise_type="isotropic")
    np.random.seed(0)
    late = ww.sphere_simulator(T=2000, N=1500, dt=0.01, noise_type="isotropic")

    fig = plt.figure(figsize=(8, 4))
    for i, (positions, title) in enumerate(
        [(early[-1], "t = 0.2"), (late[-1], "t = 20.0")]
    ):
        ax = fig.add_subplot(1, 2, i + 1, projection="3d")
        u, v = np.mgrid[0 : 2 * np.pi : 60j, 0 : np.pi : 30j]
        ax.plot_surface(
            np.cos(u) * np.sin(v),
            np.sin(u) * np.sin(v),
            np.cos(v),
            color=colors["grid"],
            alpha=0.25,
            linewidth=0,
        )
        ax.scatter(
            positions[:, 0],
            positions[:, 1],
            positions[:, 2],
            s=2,
            c=colors["particles"],
            alpha=0.6,
            depthshade=False,
        )
        ax.set_title(title)
        ax.set_box_aspect([1, 1, 1])
        ax.set_axis_off()
    fig.suptitle("1500 particles from (1, 0, 0), spreading over the sphere")
    return fig


def sphere_z_histogram(colors):
    np.random.seed(0)
    trajectory = ww.sphere_simulator(T=2000, N=4000, dt=0.01, noise_type="isotropic")

    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.hist(
        trajectory[-1][:, 2],
        bins=20,
        range=(-1, 1),
        color=colors["particles"],
        edgecolor="none",
    )
    ax.axhline(4000 / 20, color=colors["fg"], linestyle="--", linewidth=1.2)
    ax.set_xlabel("z coordinate")
    ax.set_ylabel("particles")
    ax.set_title("z is uniform on [-1, 1] once the particles equilibrate")
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    return fig


def torus_scatter(colors):
    R, r = 3.0, 1.0
    np.random.seed(0)
    trajectory = ww.torus_simulator(T=800, N=2000, dt=0.01, R=R, r=r)
    positions = trajectory[-1]

    fig = plt.figure(figsize=(6, 4.5))
    ax = fig.add_subplot(projection="3d")
    u, v = np.mgrid[0 : 2 * np.pi : 80j, 0 : 2 * np.pi : 40j]
    ax.plot_surface(
        (R + r * np.cos(v)) * np.cos(u),
        (R + r * np.cos(v)) * np.sin(u),
        r * np.sin(v),
        color=colors["grid"],
        alpha=0.25,
        linewidth=0,
    )
    ax.scatter(
        positions[:, 0],
        positions[:, 1],
        positions[:, 2],
        s=2,
        c=colors["particles"],
        alpha=0.6,
        depthshade=False,
    )
    ax.set_box_aspect([1, 1, 0.35])
    ax.set_axis_off()
    ax.set_title("2000 particles on a torus with R = 3, r = 1, at t = 8")
    return fig


def torus_angle_density(colors):
    R, r = 3.0, 1.0
    torus = ww.Torus(R, r)
    np.random.seed(0)
    trajectory = ww.torus_simulator(T=4000, N=4000, dt=0.01, R=R, r=r)
    _, poloidal = torus.angles_from_points(trajectory[-1])

    grid = np.linspace(-np.pi, np.pi, 400)
    # The invariant density is proportional to the area element
    # (R + r cos v), normalized over one full turn of v
    expected = (R + r * np.cos(grid)) / (2 * np.pi * R)

    fig, ax = plt.subplots(figsize=(6, 3.4))
    ax.hist(
        poloidal,
        bins=40,
        range=(-np.pi, np.pi),
        density=True,
        color=colors["particles"],
        edgecolor="none",
        label="simulated",
    )
    ax.plot(
        grid,
        expected,
        color=colors["fg"],
        linestyle="--",
        linewidth=1.6,
        label="(R + r cos v) / (2 pi R)",
    )
    ax.set_xlabel("poloidal angle v")
    ax.set_ylabel("density")
    ax.set_title("Particles pile up on the outside of the tube")
    ax.legend(frameon=False, labelcolor=colors["fg"])
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    return fig


def disk_scatter(colors):
    np.random.seed(0)
    trajectory = ww.hyperbolic_simulator(T=600, N=2000, dt=0.01)

    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    for ax, step, label in [(axes[0], 99, "t = 1.0"), (axes[1], 599, "t = 6.0")]:
        positions = trajectory[step]
        circle = plt.Circle(
            (0, 0), 1.0, fill=False, color=colors["fg"], linewidth=1.4
        )
        ax.add_patch(circle)
        ax.scatter(
            positions[:, 0],
            positions[:, 1],
            s=2,
            c=colors["particles"],
            alpha=0.5,
        )
        ax.set_xlim(-1.05, 1.05)
        ax.set_ylim(-1.05, 1.05)
        ax.set_aspect("equal")
        ax.set_axis_off()
        ax.set_title(label)
    fig.suptitle("Paths in the Poincare disk run out to the boundary circle")
    return fig


def hyperbolic_distance_growth(colors):
    disk = ww.PoincareDisk()
    np.random.seed(0)
    trajectory = ww.hyperbolic_simulator(T=1500, N=2000, dt=0.01)

    times = np.arange(1, trajectory.shape[0] + 1) * 0.01
    mean_distance = np.array(
        [disk.geodesic_distance_from_origin_multiple(step).mean() for step in trajectory]
    )

    # The theoretical rate is the slope, not the intercept: the radial SDE is
    # d(rho) = d(beta) + (1/2)coth(rho)dt, and coth(rho) exceeds 1 early on,
    # so the curve settles onto a line of slope 1/2 that is offset upward.
    late = times > 5.0
    slope, intercept = np.polyfit(times[late], mean_distance[late], 1)

    fig, ax = plt.subplots(figsize=(6, 3.4))
    ax.plot(times, mean_distance, color=colors["particles"], linewidth=1.8, label="simulated")
    ax.plot(
        times,
        slope * times + intercept,
        color=colors["fg"],
        linestyle="--",
        linewidth=1.4,
        label=f"fit for t > 5: slope {slope:.3f} (theory 0.5)",
    )
    ax.set_xlabel("time t")
    ax.set_ylabel("mean geodesic distance from origin")
    ax.set_title("Distance from the origin grows linearly, not like sqrt(t)")
    ax.legend(frameon=False, labelcolor=colors["fg"])
    ax.grid(alpha=0.3)
    ax.set_axisbelow(True)
    return fig


def sphere_density(colors):
    np.random.seed(0)
    trajectory = ww.sphere_simulator(T=60, N=3000, dt=0.01, noise_type="isotropic")

    u, v = np.mgrid[0 : 2 * np.pi : 120j, 0 : np.pi : 60j]
    x, y, z = np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), np.cos(v)
    density = ww.sphere_kde(trajectory[-1], x, y, z, N=3000)

    fig = plt.figure(figsize=(5.5, 4.5))
    ax = fig.add_subplot(projection="3d")
    ax.plot_surface(
        x,
        y,
        z,
        facecolors=plt.cm.magma(density),
        linewidth=0,
        antialiased=False,
        shade=False,
    )
    ax.set_box_aspect([1, 1, 1])
    ax.set_axis_off()
    ax.set_title("sphere_kde at t = 0.6, still concentrated near the start")
    return fig


def disk_density(colors):
    np.random.seed(0)
    trajectory = ww.hyperbolic_simulator(T=300, N=3000, dt=0.01)

    grid = np.linspace(-0.99, 0.99, 300)
    x_mesh, y_mesh = np.meshgrid(grid, grid)
    density = ww.disk_kde(trajectory[-1], x_mesh, y_mesh, k=40)

    fig, ax = plt.subplots(figsize=(4.8, 4.5))
    ax.pcolormesh(x_mesh, y_mesh, density, cmap="magma", shading="auto")
    ax.add_patch(plt.Circle((0, 0), 1.0, fill=False, color=colors["fg"], linewidth=1.4))
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.set_title("disk_kde at t = 3.0")
    return fig


def heat_kernel_comparison(colors):
    from wanderwalk.heat_kernel import (
        estimate_density,
        estimate_heat_kernel,
        estimate_theoretical_heat_kernel,
    )

    np.random.seed(0)
    samples = estimate_heat_kernel()

    fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.4), sharey=False)
    for ax, (index, t) in zip(axes, [(1, 0.5), (3, 2.0)]):
        theta_grid, phi_grid, empirical, _, _ = estimate_density(samples, index)
        theoretical = estimate_theoretical_heat_kernel(theta_grid, phi_grid, t)
        ax.plot(
            theta_grid,
            empirical.mean(axis=1),
            color=colors["particles"],
            linewidth=2,
            label="empirical (KDE)",
        )
        ax.plot(
            theta_grid,
            theoretical.mean(axis=1),
            color=colors["fg"],
            linestyle="--",
            linewidth=1.6,
            label="Legendre expansion",
        )
        ax.set_title(f"t = {t}")
        ax.set_xlabel("polar angle theta")
        ax.grid(alpha=0.3)
        ax.set_axisbelow(True)
    axes[0].set_ylabel("density")
    axes[0].legend(frameon=False, labelcolor=colors["fg"])
    fig.suptitle("Empirical heat kernel against the analytic one")
    fig.tight_layout()
    return fig


FIGURES = {
    "sphere-scatter": sphere_scatter,
    "sphere-z-histogram": sphere_z_histogram,
    "torus-scatter": torus_scatter,
    "torus-angle-density": torus_angle_density,
    "disk-scatter": disk_scatter,
    "hyperbolic-distance-growth": hyperbolic_distance_growth,
    "sphere-density": sphere_density,
    "disk-density": disk_density,
    "heat-kernel-comparison": heat_kernel_comparison,
}


def main():
    for name, draw in FIGURES.items():
        render(name, draw)


if __name__ == "__main__":
    main()
