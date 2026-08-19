# API reference

Generated from the docstrings in the installed package, so it always matches
the version you have.

The library is conventionally imported as `ww`:

```python
import wanderwalk as ww
```

## Public API

Everything below is re-exported at the top level and reachable through the
alias.

| Name | What it is |
| --- | --- |
| [`Manifold`](manifolds.md#wanderwalk.manifolds.base.Manifold) | Abstract base class for a surface. |
| [`Sphere`](manifolds.md#wanderwalk.manifolds.sphere.Sphere) | The unit sphere `S^2`. |
| [`Torus`](manifolds.md#wanderwalk.manifolds.torus.Torus) | The torus `T^2`, with major radius `R` and minor radius `r`. |
| [`PoincareDisk`](manifolds.md#wanderwalk.manifolds.hyperbolic.PoincareDisk) | The hyperbolic plane `H^2` in the Poincare disk model. |
| [`sphere_simulator`](simulation.md#wanderwalk.simulation.simulator.sphere_simulator) | Many particles on the sphere. Returns `(T, N, 3)`. |
| [`torus_simulator`](simulation.md#wanderwalk.simulation.simulator.torus_simulator) | Many particles on the torus. Returns `(T, N, 3)`. |
| [`hyperbolic_simulator`](simulation.md#wanderwalk.simulation.simulator.hyperbolic_simulator) | Many particles in the disk. Returns `(T, N, 2)`. |
| [`sphere_kde`](visualization.md#wanderwalk.visualization.kde.sphere_kde) | Density estimate on a sphere mesh. |
| [`disk_kde`](visualization.md#wanderwalk.visualization.hyperbolic_kde.disk_kde) | Density estimate on a disk mesh, using hyperbolic distance. |
| [`boundary_angle_histogram`](visualization.md#wanderwalk.visualization.hyperbolic_kde.boundary_angle_histogram) | Angular histogram of particles near the boundary circle. |
| `__version__` | The installed version string. |

## Outside the alias

[`wanderwalk.heat_kernel`](heat-kernel.md) needs SciPy, so it is not imported
at the top level and `ww.heat_kernel` will not resolve. Import it by path.

## Not in the public API

`wanderwalk.app` holds the Streamlit application and its launcher. It is an
application, not a library surface, and is documented in
[the app guide](../guides/streamlit-app.md) instead.
