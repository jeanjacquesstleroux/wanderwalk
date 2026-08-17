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

# Returns array of particles' position at times 0.1, 0.5, 1.0, 2.0
def estimate_heat_kernel():
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

# Returns KDE estimate
def estimate_density(samples, time_index):
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

# Returns theoretical heat kernel density at given time t
def estimate_theoretical_heat_kernel(theta_grid, phi_grid, t):
    l_max = 50 # Chosen max value of l in the infinite series
    phi_mesh, theta_mesh = np.meshgrid(phi_grid, theta_grid)
    density = np.zeros_like(theta_mesh)
    
    # Calculate summation (total density)
    for l in range(l_max + 1):
        density += (
            (2 * l + 1) * np.exp(-l * (l + 1) * t) * eval_legendre(l, np.cos(theta_mesh))
        )
    
    # Divide sum by 4 pi
    theoretical_density = density / (4 * np.pi)
    
    return theoretical_density