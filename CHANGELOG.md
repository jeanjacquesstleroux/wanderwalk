# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `Torus.sample_tangent_noise_anisotropic` and
  `Torus.sample_tangent_noise_anisotropic_multiple`, which restrict noise to
  `e_u`, the tangent direction around the torus's central axis.
- `wanderwalk.heat_kernel`, comparing the empirical heat kernel on `S^2`
  (kernel density estimate over many simulated paths, normalized by the
  spherical area element) against the Legendre spectral expansion. It needs
  SciPy, so it is not re-exported at the top level and must be imported as
  `from wanderwalk.heat_kernel import ...`.
- `notebooks/Notebook-04.ipynb`, validating that empirical heat kernel against
  the theoretical one. The Poincaré disk notebook it displaces is now
  `notebooks/Notebook-05.ipynb`.

### Changed

- `torus_simulator` accepts `noise_type`, defaulting to `"isotropic"`, and
  raises `ValueError` on an unrecognized value. It is keyword-friendly and
  placed after `R` and `r`, so existing positional calls keep working.

## [0.1.0] - 2026-08-17

First packaged release. The simulation code existed beforehand as a set of
scripts under `src/`; this release turns it into an installable library.

### Added

- Installable `wanderwalk` package with a public API re-exported at the top
  level: `Manifold`, `Sphere`, `Torus`, `PoincareDisk`, `sphere_simulator`,
  `torus_simulator`, `hyperbolic_simulator`, `sphere_kde`, `disk_kde`, and
  `boundary_angle_histogram`.
- `wanderwalk-app` console script that launches the Streamlit app, installed
  with the optional `app` extra.
- Optional dependency extras: `app` (Streamlit and Plotly), `notebooks`
  (JupyterLab, matplotlib, SciPy), and `test` (pytest).
- Test suite covering the geometric invariants of each manifold, simulator
  output shapes and constraints, the kernel density estimators, and the
  packaging contract.
- `Torus.angles_from_point` and `Torus.angles_from_points`, which recover the
  toroidal and poloidal angles from a Cartesian point.
- `Torus.project_to_tangent_multiple`, for interface parity with `Sphere` and
  `PoincareDisk`.

### Changed

- The sphere simulator is now named `sphere_simulator` rather than
  `simulator`, so all three simulators name the surface they run on.
- `Torus.project_to_tangent` now takes `(x, v)` with a Cartesian point,
  matching `Manifold.project_to_tangent` and the other two manifolds. The
  previous angle-based form is still available as
  `Torus.project_to_tangent_at_angles(u, v, vector)`.
- `sphere_simulator` raises `ValueError` on an unrecognized `noise_type`
  instead of failing later with `UnboundLocalError`.
- Simulator starting points are coerced to float arrays, so integer input is
  accepted.
- `requirements.txt` no longer pins a frozen environment; dependencies are
  declared in `pyproject.toml`.

### Removed

- The `src` top-level import package. Imports are now `from wanderwalk import
  ...` rather than `from src.manifolds.sphere import ...`, and the
  `sys.path.append("..")` workaround is no longer needed.

[Unreleased]: https://github.com/jeanjacquesstleroux/wanderwalk/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/jeanjacquesstleroux/wanderwalk/releases/tag/v0.1.0
