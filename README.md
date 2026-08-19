<p align="center">
  <img src="https://raw.githubusercontent.com/jeanjacquesstleroux/wanderwalk/main/docs/assets/wanderwalk-logo.png" alt="wanderwalk" width="280">
</p>

<h1 align="center">wanderwalk</h1>

<p align="center">Brownian motion on Riemannian manifolds</p>

<p align="center">
  <a href="https://pypi.org/project/wanderwalk/"><img src="https://img.shields.io/badge/version-0.2.0-5e35b1" alt="version 0.2.0"></a>
  <a href="https://pypi.org/project/wanderwalk/"><img src="https://img.shields.io/badge/python-3.9%2B-blue" alt="Python 3.9 and newer"></a>
  <a href="https://github.com/jeanjacquesstleroux/wanderwalk/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="MIT license"></a>
  <a href="https://jeanjacquesstleroux.github.io/wanderwalk/"><img src="https://img.shields.io/badge/docs-github.io-purple" alt="Documentation"></a>
</p>

This project simulates Brownian motion on Riemannian manifolds. It pairs a small, testable Python library for running these simulations with an interactive Streamlit app for watching the diffusion unfold in real time.

```bash
pip install wanderwalk
```

```python
import numpy as np
import wanderwalk as ww

np.random.seed(0)
trajectory = ww.sphere_simulator(T=200, N=500, dt=0.01, noise_type="isotropic")
final_positions = trajectory[-1]        # (500, 3), every point on the sphere
```

Full documentation, including six tutorials and a generated API reference,
is at [jeanjacquesstleroux.github.io/wanderwalk](https://jeanjacquesstleroux.github.io/wanderwalk/).

## What This Project Is About

Brownian motion is the random, erratic motion first observed in pollen grains suspended in water and later given a rigorous mathematical treatment by Einstein and Wiener. It underlies fields ranging from statistical physics to quantitative finance, and, more recently, the diffusion models behind modern generative AI.

The question this project explores is what happens to that random motion when the space it lives in is curved. A particle wandering on the surface of a sphere behaves differently from one wandering on a flat plane or on the surface of a donut (a torus): the curvature of the space bends and constrains the motion. This project builds simulations of that behavior and visualizes it directly.

For the full motivation, mathematical background, and the theory connecting this project to diffusion models and quantitative finance, see [ONBOARDING.md](https://github.com/jeanjacquesstleroux/wanderwalk/blob/main/ONBOARDING.md). 

## Surfaces Implemented

- **Sphere (S²)**: positively curved, particle paths are recurrent, and the particle distribution converges to uniform over the surface.
- **Torus (T²)**: zero average curvature but non-trivial global topology; particles wrap around the surface rather than escaping it.
- **Hyperbolic plane (H²)**: represented via the Poincaré disk model. Its constant negative curvature makes random paths transient -- rather than equilibrating to a uniform distribution, particle paths converge almost surely to a random point on the boundary circle (the Poisson boundary). See `docs/writeups/2-poincare-disk-derivation.md` for the full derivation of the governing SDE from this project's own conventions, and `notebooks/Notebook-05.ipynb` for its validation.

## How the Simulation Works

Each manifold is represented by a small class (`src/wanderwalk/manifolds/sphere.py`, `src/wanderwalk/manifolds/torus.py`, `src/wanderwalk/manifolds/hyperbolic.py`) implementing a shared interface (`src/wanderwalk/manifolds/base.py`):

- `sample_tangent_noise`: generates a random vector constrained to the tangent plane at a point, so a step never points off the surface.
- `euler_maruyama_step`: advances a point one time step using the Euler-Maruyama method, the standard numerical scheme for stochastic differential equations.
- `project_to_manifold`: pulls a point back onto the surface after a step, correcting for the small numerical drift introduced by moving in a straight line through the ambient space.

For the Sphere and Torus, this is the *projection method*: propose a step in the tangent plane, take it, then project back onto the surface -- both are embedded in R³, so ambient Euclidean lengths agree with the surface's own metric. The Poincaré disk has no such embedding (Hilbert's theorem), so it is handled intrinsically instead: points are 2D vectors in the open unit disk, `sample_tangent_noise` rescales an isotropic Gaussian by the disk's own conformal factor rather than projecting an ambient vector, and `project_to_manifold` is a numerical safety clamp rather than an exact geometric projection (see the derivation doc for why).

Running this update for many particles at once (vectorized with NumPy) is handled by `src/wanderwalk/simulation/simulator.py`, and the resulting particle distributions are visualized with a kernel density estimate in `src/wanderwalk/visualization/kde.py` (sphere) and `src/wanderwalk/visualization/hyperbolic_kde.py` (Poincaré disk, using the exact hyperbolic geodesic distance as the kernel). The geometry, the simulation loop, and the visualization are kept in separate modules, so adding a new surface mostly requires implementing its geometry, without changes to the simulator's vectorized-loop pattern.

## Installation

The core library depends only on NumPy:

```bash
pip install wanderwalk
```

The Streamlit app is optional, since it pulls in Streamlit and Plotly:

```bash
pip install wanderwalk[app]
```

Requires Python 3.9 or newer.

## Library Usage

The three simulators each return a trajectory array of shape `(T, N, d)`, holding the positions of all `N` particles at each of the `T` time steps. The sphere and torus live in R^3 so `d` is 3; the Poincaré disk is intrinsically two-dimensional so `d` is 2.

The library is conventionally imported under the alias `ww`, the way NumPy is
imported as `np`. Every example in the documentation uses that convention.

```python
import numpy as np
import wanderwalk as ww

np.random.seed(0)                                     # for a repeatable run

on_sphere = ww.sphere_simulator(T=200, N=500, dt=0.01, noise_type="isotropic")
on_torus = ww.torus_simulator(T=200, N=500, dt=0.01, R=3.0, r=1.0)
in_disk = ww.hyperbolic_simulator(T=200, N=500, dt=0.01)

on_sphere.shape, in_disk.shape                        # ((200, 500, 3), (200, 500, 2))
```

The manifold classes can also be driven directly, one step at a time:

```python
sphere = ww.Sphere()
point = np.array([1.0, 0.0, 0.0])
for _ in range(100):
    point = sphere.euler_maruyama_step(point, dt=0.01)   # stays on the sphere

disk = ww.PoincareDisk()
disk.geodesic_distance_from_origin(np.array([0.6, 0.0]))  # hyperbolic distance
```

And the density estimators turn final positions into a heatmap:

```python
density = ww.disk_kde(in_disk[-1], x_mesh, y_mesh, N=500)
counts, edges = ww.boundary_angle_histogram(in_disk[-1], radius_threshold=0.9)
```

One module sits outside the alias. `wanderwalk.heat_kernel` needs SciPy, which
the numpy-only core install does not pull in, so it is not re-exported at the
top level and `ww.heat_kernel` will not resolve. Import it by path:

```python
from wanderwalk.heat_kernel import estimate_heat_kernel
```

## Project Layout

```
src/wanderwalk/manifolds/       Sphere, torus, and Poincare disk geometry (tangent
                                 projection/noise, stepping)
src/wanderwalk/simulation/      Vectorized Euler-Maruyama simulators
src/wanderwalk/visualization/   Kernel density estimation for particle distributions
src/wanderwalk/app/             Streamlit application and its launcher
tests/                          Test suite
notebooks/                      Jupyter notebooks (also exported to HTML for viewing
                                 without running code)
docs/writeups/                  Mathematical background, the differential geometry
                                 curriculum, and the Poincare disk SDE derivation
ONBOARDING.md                   Motivation, theory, and project background
```

## Development

```bash
git clone https://github.com/jeanjacquesstleroux/wanderwalk.git
cd wanderwalk
pip install -r requirements.txt     # editable install with all extras
pytest
```

## Starting the App

Once the `app` extra is installed, launch it with the bundled console script:

```bash
wanderwalk-app
```

This opens the app in your browser. From the sidebar you can:

- Choose the manifold (sphere, torus, or Poincaré disk).
- Set the number of particles, number of time steps, and the size of each time step.
- Choose isotropic noise (motion in all tangent directions) or, for the sphere and the torus, anisotropic noise (motion constrained to a single tangent direction).
- Set the starting point (latitude and longitude for the sphere, the toroidal and poloidal angles for the torus, or the radius and angle for the Poincaré disk) and, for the torus, its major and minor radius.

Click "Run Simulation" to generate an animated trajectory, the final particle distribution, and a density heatmap of where the particles ended up.

## Notebooks

The `notebooks/` directory contains the exploratory work behind the library, each one also exported to HTML in the same folder so it can be read without running any code. To run them yourself, install the notebook extra:

```bash
pip install wanderwalk[notebooks]
jupyter lab notebooks/
```

## Authors

- Jean-Jacques St. Leroux
- Danielle Prilepskiy

## License

Released under the MIT License. See [LICENSE](https://github.com/jeanjacquesstleroux/wanderwalk/blob/main/LICENSE).
