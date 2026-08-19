"""Empirical and theoretical heat kernel on the unit sphere S^2.

Estimates the heat kernel two ways so they can be compared: empirically, by
running many Brownian paths and applying a kernel density estimate with the
sphere's Riemannian volume normalization, and analytically, from the Legendre
spectral expansion.

This module needs SciPy, which ships in the ``notebooks`` extra rather than
the numpy-only core install, so it is deliberately not re-exported from
``wanderwalk/__init__.py``. Import it explicitly:

    from wanderwalk.heat_kernel import estimate_heat_kernel
"""

import numpy as np
from scipy.special import eval_legendre
from scipy.stats import gaussian_kde

from .manifolds.sphere import Sphere

def estimate_heat_kernel():
    """Runs 2000 Brownian paths from the north pole and samples four times.

    Each path starts at (0, 0, 1) and is advanced one step at a time with
    ``Sphere.euler_maruyama_step`` at ``dt = 0.01`` for 200 steps. Positions
    are recorded at steps 10, 50, 100, and 200, which correspond to times
    0.1, 0.5, 1.0, and 2.0.

    This is deliberately a single-particle loop rather than a call to
    ``sphere_simulator``, so the samples come from the same stepping code the
    manifold exposes. It takes a few seconds to run.

    Returns:
        A (2000, 4, 3) array of positions on the sphere, indexed by path,
        then by time (0.1, 0.5, 1.0, 2.0), then by Cartesian coordinate.
    """
    sphere = Sphere()
    initial_point = np.array([0.0, 0.0, 1.0])
    times = [0.1, 0.5, 1.0, 2.0]
    chosen_steps = [10, 50, 100, 200] # Corresponding step from time (chosen_steps = times / dt)
    samples = np.zeros((2000, 4, 3))
    dt = 0.01

    # Run 2000 paths
    for path in range(2000):
        point = initial_point.copy()
        # Simulate path
        for step in range(1, 201):
            point = sphere.euler_maruyama_step(point, dt)
            if step in chosen_steps:
                time_index = chosen_steps.index(step)
                samples[path, time_index] = point

    return samples

def estimate_density(samples, time_index):
    """Estimates the empirical heat kernel density at one sampled time.

    Fits a Gaussian kernel density estimate to the sampled positions in
    ambient R^3, evaluates it on a 50 by 50 grid in spherical coordinates,
    then renormalizes by the sphere's area element sin(theta) d(theta) d(phi)
    so the result integrates to 1 over the surface rather than over R^3.

    Arguments:
        samples: A (paths, times, 3) array as returned by
            estimate_heat_kernel.
        time_index: Which of the sampled times to estimate, indexing the
            second axis of samples. With estimate_heat_kernel's defaults,
            0, 1, 2, and 3 mean t = 0.1, 0.5, 1.0, and 2.0.

    Returns:
        A tuple (theta_grid, phi_grid, normalized_density, dtheta, dphi).
        theta_grid is 50 polar angles over [0, pi] and phi_grid is 50
        azimuthal angles over [0, 2*pi); normalized_density is the
        (50, 50) density over that grid, indexed as [theta, phi]; dtheta
        and dphi are the grid spacings, returned so callers can integrate
        the density without recomputing them.
    """
    samples_time = samples[:, time_index, :] # Get all the samples at given time

    x = samples_time[:, 0]
    y = samples_time[:, 1]
    z = samples_time[:, 2]

    # Convert (x, y, z) to spherical (rho is already 1, due to unit sphere)
    theta = np.arccos(z)
    phi = np.mod(np.arctan2(y, x), 2 * np.pi) # Phi between 0 and 2pi, not -pi and pi

    # Create meshgrids from theta and phi
    theta_grid = np.linspace(0, np.pi, 50)
    phi_grid = np.linspace(0, 2*np.pi, 50)
    theta_mesh, phi_mesh = np.meshgrid(theta_grid, phi_grid, indexing="ij") # Rows theta, cols phi

    dtheta = theta_grid[1] - theta_grid[0]
    dphi = phi_grid[1] - phi_grid[0]

    # Store sampled points in Cartesian coordinates
    sampled_points = np.vstack([x, y, z])

    # Compute KDE on sampled points
    kernel = gaussian_kde(sampled_points)

    # Convert spherical grid points to Cartesian coordinates
    x_grid = np.sin(theta_mesh) * np.cos(phi_mesh)
    y_grid = np.sin(theta_mesh) * np.sin(phi_mesh)
    z_grid = np.cos(theta_mesh)

    # Transform grid coordinates to positions for KDE
    positions = np.vstack([x_grid.ravel(),
                           y_grid.ravel(),
                           z_grid.ravel()])

    # Compute KDE at each grid point
    density = kernel(positions)

    # Reshape the density to 50x50 grid for plotting
    density = density.reshape(theta_mesh.shape)

    # Correct the KDE density for a sphere
    # Calculate the Riemannian integral using area element
    area_element = np.sin(theta_mesh) * dtheta * dphi

    # Normalize density
    total_density = np.sum(density * area_element)
    normalized_density = density / total_density

    return theta_grid, phi_grid, normalized_density, dtheta, dphi

def estimate_theoretical_heat_kernel(theta_grid, phi_grid, t):
    """Evaluates the analytic heat kernel on S^2 from its Legendre expansion.

    The heat kernel from the north pole depends only on the polar angle, and
    has the spectral expansion

        p(t, theta) = (1/4*pi) * sum_l (2l+1) exp(-l(l+1)t/2) P_l(cos theta)

    where P_l is the Legendre polynomial of degree l and l(l+1) is the
    eigenvalue of the Laplace-Beltrami operator on the sphere. The sum is
    truncated at l = 50. The exponential decay makes that ample for the
    times sampled by estimate_heat_kernel, but the series converges slowly
    as t approaches 0, where many more terms would be needed.

    The factor of 1/2 in the exponent is the generator convention this
    project uses throughout: Brownian motion is the diffusion generated by
    (1/2)*Laplacian, not the Laplacian (see ONBOARDING.md). Sources that
    state this expansion as exp(-l(l+1)t) are using the other convention,
    and their t is half of this one.

    Arguments:
        theta_grid: Polar angles over [0, pi], as returned by
            estimate_density.
        phi_grid: Azimuthal angles over [0, 2*pi), as returned by
            estimate_density. Used only to set the output shape, since the
            kernel is symmetric about the axis through the starting point.
        t: The time at which to evaluate the kernel.

    Returns:
        A (len(theta_grid), len(phi_grid)) array of density values, indexed
        as [theta, phi] to match estimate_density's output.
    """
    l_max = 50 # Chosen max value of l in the infinite series
    phi_mesh, theta_mesh = np.meshgrid(phi_grid, theta_grid)
    density = np.zeros_like(theta_mesh)

    # Calculate summation (total density). The eigenvalue is halved because
    # the generator is (1/2)*Laplacian, matching the simulators.
    for l in range(l_max + 1):
        density += (
            (2 * l + 1)
            * np.exp(-l * (l + 1) * t / 2)
            * eval_legendre(l, np.cos(theta_mesh))
        )

    # Divide sum by 4 pi
    theoretical_density = density / (4 * np.pi)

    return theoretical_density