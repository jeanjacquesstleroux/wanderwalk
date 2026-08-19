"""Vectorized Euler-Maruyama simulators for Brownian motion on each manifold.

Each simulator advances N independent particles for T time steps at once,
returning the full trajectory rather than only the final positions, so that
both the time evolution and the terminal distribution can be inspected.

Reproducibility: these simulators draw from NumPy's global random state via
``np.random``. Call ``np.random.seed(...)`` before a simulator to obtain a
repeatable trajectory.

All three are re-exported at the top level, so under the conventional alias
they are reached as ``ww.sphere_simulator``, ``ww.torus_simulator``, and
``ww.hyperbolic_simulator``.
"""

import numpy as np

from ..manifolds.hyperbolic import PoincareDisk
from ..manifolds.sphere import Sphere
from ..manifolds.torus import Torus

_NOISE_TYPES = ("isotropic", "anisotropic")


def sphere_simulator(T, N, dt, noise_type, starting_point=None):
    """Simulates Brownian motion for N particles on the unit sphere S^2.

    Arguments:
        T: Number of time steps to advance.
        N: Number of independent particles to simulate.
        dt: Size of each time step.
        noise_type: Either "isotropic" (motion in all tangent directions) or
            "anisotropic" (motion constrained to a single tangent direction).
        starting_point: Optional point in R^3 for every particle to start
            from. It is projected onto the sphere first, so it need not be
            normalized. Defaults to (1, 0, 0).

    Returns:
        A (T, N, 3) array of particle positions, where entry [t] holds the
        positions of all N particles after time step t.

    Raises:
        ValueError: If noise_type is not one of the two supported values.
    """
    if noise_type not in _NOISE_TYPES:
        raise ValueError(
            f"noise_type must be one of {_NOISE_TYPES}, got {noise_type!r}"
        )

    # Initialize a sphere object
    sphere = Sphere()

    # Initialize N particles at a point on the sphere
    if starting_point is None:
        points = np.tile([1.0, 0.0, 0.0], (N, 1))
    else:
        # Avoid floating point errors, ensure point is on sphere
        starting_point = sphere.project_to_manifold(
            np.asarray(starting_point, dtype=float)
        )
        points = np.tile(starting_point, (N, 1))
    # Initialize the trajectory to an empty array to later store the new
    # positions of each point in points
    trajectory = np.zeros((T, N, 3))

    # Go through each time step
    for t in range(T):
        if noise_type == "isotropic":
            noise = sphere.sample_tangent_noise_multiple(points)
        else:
            noise = sphere.sample_tangent_noise_anisotropic_multiple(points)
        # Scale the noise by square root of dt
        noise_scaled = np.sqrt(dt) * noise
        # Add the noise to all of the particles in points
        points += noise_scaled
        # Project all particles back onto the sphere
        points = sphere.project_to_manifold_multiple(points)
        # Store the new positions of each point in the trajectory array
        trajectory[t] = points
    return trajectory


def torus_simulator(T, N, dt, R, r, noise_type="isotropic", starting_point=None):
    """Simulates Brownian motion for N particles on the torus T^2.

    Arguments:
        T: Number of time steps to advance.
        N: Number of independent particles to simulate.
        dt: Size of each time step.
        R: Major radius, from the center of the hole to the center of the tube.
        r: Minor radius, the radius of the tube.
        noise_type: Either "isotropic" (motion in all tangent directions) or
            "anisotropic" (motion constrained to e_u, the direction around the
            central axis). Defaults to "isotropic".
        starting_point: Optional point in R^3 on the torus for every particle
            to start from. Defaults to the point at toroidal and poloidal
            angles (0, 0).

    Returns:
        A (T, N, 3) array of particle positions.

    Raises:
        ValueError: If noise_type is not one of the two supported values.
    """
    if noise_type not in _NOISE_TYPES:
        raise ValueError(
            f"noise_type must be one of {_NOISE_TYPES}, got {noise_type!r}"
        )

    torus = Torus(R, r)

    if starting_point is None:
        starting_point = torus.parametrize(0.0, 0.0)
    points = np.tile(np.asarray(starting_point, dtype=float), (N, 1))
    trajectory = np.zeros((T, N, 3))

    for t in range(T):
        if noise_type == "isotropic":
            noise = torus.sample_tangent_noise_multiple(points)
        else:
            noise = torus.sample_tangent_noise_anisotropic_multiple(points)
        noise_scaled = np.sqrt(dt) * noise
        points = points + noise_scaled
        points = torus.project_to_manifold_multiple(points)
        trajectory[t] = points
    return trajectory


def hyperbolic_simulator(T, N, dt, starting_point=None):
    """Simulates Brownian motion for N particles on the hyperbolic plane H^2.

    Unlike the sphere and torus simulators, trajectories here have shape
    (T, N, 2), not (T, N, 3): H^2 has no isometric embedding into R^3
    (Hilbert's theorem), so points are genuine 2D vectors in the Poincare
    disk rather than 3D ambient points constrained to a surface. See
    :class:`wanderwalk.manifolds.PoincareDisk` and
    docs/writeups/2-poincare-disk-derivation.md.

    Arguments:
        T: Number of time steps to advance.
        N: Number of independent particles to simulate.
        dt: Size of each time step.
        starting_point: Optional point in the open unit disk for every
            particle to start from. It is clamped inside the disk first.
            Defaults to the origin.

    Returns:
        A (T, N, 2) array of particle positions in the Poincare disk.
    """
    disk = PoincareDisk()

    if starting_point is None:
        starting_point = np.array([0.0, 0.0])
    else:
        starting_point = disk.project_to_manifold(
            np.asarray(starting_point, dtype=float)
        )
    points = np.tile(starting_point, (N, 1))
    trajectory = np.zeros((T, N, 2))

    for t in range(T):
        noise = disk.sample_tangent_noise_multiple(points)
        noise_scaled = np.sqrt(dt) * noise
        points = points + noise_scaled
        points = disk.project_to_manifold_multiple(points)
        trajectory[t] = points
    return trajectory
