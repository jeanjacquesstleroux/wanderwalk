import numpy as np
import math

# Plot the empirical surface distribution (KDE heatmap on the sphere)

def sphere_kde(final_positions, x_surface, y_surface, z_surface, k=None, N=None):
    """
    Computes a kernel density estimate of particle positions on the unit sphere.
    The kernel uses the dot product between each particle's position and each
    point on the sphere surface to measure closeness.

    Points on the unit sphere have a norm of 1, so a larger dot product
    corresponds to a smaller geodesic distance between two points. The kernel
    assigns larger weights to points on the mesh surface that are closer to
    the particles and smaller weights to points that are farther to the
    particles.

    Arguments:
        final_positions: An (N, 3) array of final particle positions on the
            unit sphere.
        x_surface: A 2D array containing the x-coordinates of the sphere
            mesh.
        y_surface: A 2D array containing the y-coordinates of the sphere
            mesh.
        z_surface: A 2D array containing the z-coordinates of the sphere
            mesh.
        k: The concentration parameter for the kernel. Larger values produce
            more concentrated density around the particles. Defaults to
            sqrt(N) when N is given, else 20 (same default convention as
            disk_kde).
        N: Number of particles, used to pick a default k.

    Returns:
        A 2D array (same shape as x-, y-, z-surface meshes) containing
        the normalized density values on the sphere.
    """

    # Flatten each 2D surface to a coordinate on the sphere surface
    x_one_dim = x_surface.flatten()
    y_one_dim = y_surface.flatten()
    z_one_dim = z_surface.flatten()

    # Put the coordinates as points on the mesh surface
    mesh = np.stack([x_one_dim, y_one_dim, z_one_dim], axis=1)

    # Choose the value of k parameter: honor an explicitly given k, and
    # only fall back to a default (scaled by N when available) if none was given
    if k is None:
        k = math.sqrt(N) if N else 20

    # Compute all the dot products
    mesh = mesh.transpose()  # shape becomes (3, M)
    dot_prod = np.dot(final_positions, mesh)

    # Apply k to get the weights
    weights = np.exp(k * dot_prod)

    # Add up all the weights for each mesh point
    density = np.sum(weights, axis=0)

    # Normalize the density by dividing by the maximum
    density /= density.max()

    # Reshape density back onto the sphere grid
    density = density.reshape(x_surface.shape)

    return density