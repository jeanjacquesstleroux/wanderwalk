# Brownian Motion on Manifolds

This project simulates Brownian motion on Riemannian manifolds. It pairs a small, testable Python library for running these simulations with an interactive Streamlit app for watching the diffusion unfold in real time.

## What This Project Is About

Brownian motion is the random, erratic motion first observed in pollen grains suspended in water and later given a rigorous mathematical treatment by Einstein and Wiener. It underlies fields ranging from statistical physics to quantitative finance, and, more recently, the diffusion models behind modern generative AI.

The question this project explores is what happens to that random motion when the space it lives in is curved. A particle wandering on the surface of a sphere behaves differently from one wandering on a flat plane or on the surface of a donut (a torus): the curvature of the space bends and constrains the motion. This project builds simulations of that behavior and visualizes it directly.

For the full motivation, mathematical background, and the theory connecting this project to diffusion models and quantitative finance, see [ONBOARDING.md](ONBOARDING.md). 

## Surfaces Implemented

- **Sphere (S²)**: positively curved, particle paths are recurrent, and the particle distribution converges to uniform over the surface.
- **Torus (T²)**: zero average curvature but non-trivial global topology; particles wrap around the surface rather than escaping it.
- **Hyperbolic plane (H²)**: represented via the Poincaré disk model. Its constant negative curvature makes random paths transient -- rather than equilibrating to a uniform distribution, particle paths converge almost surely to a random point on the boundary circle (the Poisson boundary). See `docs/writeups/2-poincare-disk-derivation.md` for the full derivation of the governing SDE from this project's own conventions, and `notebooks/Notebook-04.ipynb` for its validation.

## How the Simulation Works

Each manifold is represented by a small class (`src/manifolds/sphere.py`, `src/manifolds/torus.py`, `src/manifolds/hyperbolic.py`) implementing a shared interface (`src/manifolds/base.py`):

- `sample_tangent_noise`: generates a random vector constrained to the tangent plane at a point, so a step never points off the surface.
- `euler_maruyama_step`: advances a point one time step using the Euler-Maruyama method, the standard numerical scheme for stochastic differential equations.
- `project_to_manifold`: pulls a point back onto the surface after a step, correcting for the small numerical drift introduced by moving in a straight line through the ambient space.

For the Sphere and Torus, this is the *projection method*: propose a step in the tangent plane, take it, then project back onto the surface -- both are embedded in R³, so ambient Euclidean lengths agree with the surface's own metric. The Poincaré disk has no such embedding (Hilbert's theorem), so it is handled intrinsically instead: points are 2D vectors in the open unit disk, `sample_tangent_noise` rescales an isotropic Gaussian by the disk's own conformal factor rather than projecting an ambient vector, and `project_to_manifold` is a numerical safety clamp rather than an exact geometric projection (see the derivation doc for why).

Running this update for many particles at once (vectorized with NumPy) is handled by `src/simulation/simulator.py`, and the resulting particle distributions are visualized with a kernel density estimate in `src/visualization/kde.py` (sphere) and `src/visualization/hyperbolic_kde.py` (Poincaré disk, using the exact hyperbolic geodesic distance as the kernel). The geometry, the simulation loop, and the visualization are kept in separate modules, so adding a new surface mostly requires implementing its geometry, without changes to the simulator's vectorized-loop pattern.

## Project Layout

```
app/                   Streamlit application
src/manifolds/         Sphere, torus, and Poincare disk geometry (tangent projection/noise, stepping)
src/simulation/        Vectorized Euler-Maruyama simulators
src/visualization/     Kernel density estimation for particle distributions
notebooks/             Jupyter notebooks (also exported to HTML for viewing without running code)
docs/writeups/         Mathematical background, the differential geometry curriculum, and the
                        Poincare disk SDE derivation
ONBOARDING.md          Motivation, theory, and project background
```

## Requirements

- Python 3.x
- Dependencies listed in `requirements.txt`, most notably `numpy`, `streamlit`, and `plotly`

## Starting the App

From the project root (`2manifold-brownian-motion/`):

```bash
pip install -r requirements.txt
streamlit run app/app.py
```

This opens the app in your browser. From the sidebar you can:

- Choose the manifold (sphere, torus, or Poincaré disk).
- Set the number of particles, number of time steps, and the size of each time step.
- Choose isotropic noise (motion in all tangent directions) or, for the sphere only, anisotropic noise (motion constrained to a single tangent direction).
- Set the starting point (latitude and longitude for the sphere, the toroidal and poloidal angles for the torus, or the radius and angle for the Poincaré disk) and, for the torus, its major and minor radius.

Click "Run Simulation" to generate an animated trajectory, the final particle distribution, and a density heatmap of where the particles ended up.

## Notebooks

The `notebooks/` directory contains the exploratory work behind the library, each one also exported to HTML in the same folder so it can be read without running any code.
