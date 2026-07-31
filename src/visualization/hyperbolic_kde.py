import numpy as np
import math

# Plot the empirical density of particles on the Poincare disk (geodesic KDE)
# and the empirical distribution of their angular position near the boundary.

def disk_kde(final_positions, x_mesh, y_mesh, k=None, N=None):
    '''Computes a kernel density estimate of particle positions on the
    Poincare disk, using the exact hyperbolic geodesic distance as the
    kernel argument (the direct analogue of sphere_kde's use of the
    ambient dot product, which is a geodesic-invariant closeness measure
    for the sphere; see src/manifolds/hyperbolic.py:geodesic_distance).

    Since H^2 has no invariant/stationary density to compare against (BM
    on H^2 is transient, see docs/writeups/2-poincare-disk-derivation.md),
    this is purely a particle visualization, the same role sphere_kde plays 
    for the sphere.

    Arguments:
        final_positions: An (N, 2) array of particle positions in the disk.
        x_mesh: A 2D array of x-coordinates of mesh points (only points
        strictly inside the unit disk are meaningful; others are masked
        out with NaN in the returned density).
        y_mesh: A 2D array of y-coordinates of mesh points, same shape as
        x_mesh.
        k: Concentration parameter for the kernel exp(-k * d(x_i, y)^2).
        Larger k concentrates each particle's contribution more tightly
        around itself. Defaults to sqrt(N) if N is given, else 20 (same
        default convention as sphere_kde).
        N: Number of particles, used only to pick a default k.

    Returns:
        A 2D array (same shape as x_mesh) of normalized density values,
        with NaN at mesh points outside the open unit disk.
    '''
    if k is None:
        k = math.sqrt(N) if N else 20

    mesh_x = x_mesh.flatten()
    mesh_y = y_mesh.flatten()
    inside = (mesh_x**2 + mesh_y**2) < 1.0
    valid_mesh = np.stack([mesh_x[inside], mesh_y[inside]], axis=1)

    # Vectorized hyperbolic distance between every particle (rows) and every
    # valid mesh point (columns): d(z,w) = arccosh(1 + 2|z-w|^2 / ((1-|z|^2)(1-|w|^2)))
    z_norm_sq = np.sum(final_positions**2, axis=1)[:, None]        # (N, 1)
    w_norm_sq = np.sum(valid_mesh**2, axis=1)[None, :]             # (1, M)
    # |z - w|^2 = |z|^2 + |w|^2 - 2 z.w, via broadcasting over (N, M)
    cross = final_positions @ valid_mesh.T                          # (N, M)
    diff_norm_sq = z_norm_sq + w_norm_sq - 2.0 * cross
    argument = 1.0 + 2.0 * diff_norm_sq / ((1.0 - z_norm_sq) * (1.0 - w_norm_sq))
    # Clip below 1.0 to guard against tiny negative floating-point residue
    # from the subtraction above at argument == 1 (identical points)
    distances = np.arccosh(np.clip(argument, 1.0, None))

    weights = np.exp(-k * distances**2)
    weights_sum = np.sum(weights, axis=0)                            # (M,)

    if weights_sum.max() > 0:
        weights_sum = weights_sum / weights_sum.max()

    density = np.full(mesh_x.shape[0], np.nan)
    density[inside] = weights_sum
    return density.reshape(x_mesh.shape)


def boundary_angle_histogram(final_positions, radius_threshold=0.9, bins=36):
    '''Computes a histogram of the angular position (theta = atan2(y, x)) of
    particles that have travelled beyond a given Euclidean radius
    threshold. Since paths converge almost surely to a random point on the
    boundary circle (the Poisson boundary), and the hyperbolic metric is
    rotationally symmetric about the origin, that limiting angle must be
    uniformly distributed on [0, 2*pi) (see
    docs/writeups/2-poincare-disk-derivation.md and
    notebooks/Notebook-04.ipynb for the corresponding statistical test).

    Arguments:
        final_positions: An (N, 2) array of particle positions in the disk.
        radius_threshold: Only particles with Euclidean norm at least this
        value are included, so the histogram reflects particles that have
        travelled meaningfully close to the boundary.
        bins: Number of angular bins over [0, 2*pi).

    Returns:
        A tuple (histogram, bin_edges) as returned by np.histogram, or
        (None, None) if no particles meet the radius threshold.
    '''
    radii = np.linalg.norm(final_positions, axis=1)
    near_boundary = final_positions[radii >= radius_threshold]

    if near_boundary.shape[0] == 0:
        return None, None

    angles = np.arctan2(near_boundary[:, 1], near_boundary[:, 0]) % (2 * np.pi)
    histogram, bin_edges = np.histogram(angles, bins=bins, range=(0, 2 * np.pi))
    return histogram, bin_edges
