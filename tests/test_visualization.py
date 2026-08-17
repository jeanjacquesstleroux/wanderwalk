"""Kernel density estimates and the boundary angle histogram."""

import numpy as np
import pytest

from wanderwalk import boundary_angle_histogram, disk_kde, sphere_kde


def sphere_mesh(n=20):
    """Builds a (theta, phi) mesh of Cartesian coordinates on the unit sphere."""
    theta = np.linspace(0, np.pi, n)
    phi = np.linspace(0, 2 * np.pi, n)
    theta_grid, phi_grid = np.meshgrid(theta, phi)
    return (
        np.sin(theta_grid) * np.cos(phi_grid),
        np.sin(theta_grid) * np.sin(phi_grid),
        np.cos(theta_grid),
    )


def disk_mesh(n=25):
    """Builds a mesh over the square [-1, 1]^2, which overhangs the disk."""
    axis = np.linspace(-1, 1, n)
    return np.meshgrid(axis, axis)


class TestSphereKde:
    def test_density_matches_mesh_shape(self):
        x, y, z = sphere_mesh()
        positions = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
        assert sphere_kde(positions, x, y, z, k=10).shape == x.shape

    def test_density_is_normalized_to_one(self):
        x, y, z = sphere_mesh()
        positions = np.array([[1.0, 0.0, 0.0]])
        assert np.nanmax(sphere_kde(positions, x, y, z, k=10)) == pytest.approx(1.0)

    def test_density_is_positive_and_finite(self):
        x, y, z = sphere_mesh()
        positions = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
        density = sphere_kde(positions, x, y, z, k=10)
        assert np.all(density > 0.0)
        assert np.all(np.isfinite(density))

    def test_density_peaks_nearest_a_single_particle(self):
        x, y, z = sphere_mesh(40)
        north_pole = np.array([[0.0, 0.0, 1.0]])
        density = sphere_kde(north_pole, x, y, z, k=20)
        peak = np.unravel_index(np.argmax(density), density.shape)
        assert z[peak] == pytest.approx(1.0, abs=0.05)

    def test_explicit_k_overrides_the_particle_count_default(self):
        x, y, z = sphere_mesh()
        positions = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
        tight = sphere_kde(positions, x, y, z, k=40)
        loose = sphere_kde(positions, x, y, z, k=2)
        assert not np.allclose(tight, loose)

    def test_defaults_are_used_when_k_and_n_are_absent(self):
        x, y, z = sphere_mesh()
        positions = np.array([[1.0, 0.0, 0.0]])
        assert np.all(np.isfinite(sphere_kde(positions, x, y, z)))

    def test_n_selects_a_default_k(self):
        x, y, z = sphere_mesh()
        positions = np.array([[1.0, 0.0, 0.0]])
        from_n = sphere_kde(positions, x, y, z, N=100)
        explicit = sphere_kde(positions, x, y, z, k=10.0)
        assert from_n == pytest.approx(explicit)


class TestDiskKde:
    def test_density_matches_mesh_shape(self):
        x, y = disk_mesh()
        positions = np.array([[0.0, 0.0], [0.3, 0.2]])
        assert disk_kde(positions, x, y, k=5).shape == x.shape

    def test_points_outside_the_disk_are_nan(self):
        x, y = disk_mesh()
        density = disk_kde(np.array([[0.0, 0.0]]), x, y, k=5)
        outside = (x**2 + y**2) >= 1.0
        assert np.all(np.isnan(density[outside]))
        assert not np.any(np.isnan(density[~outside]))

    def test_density_is_normalized_to_one(self):
        x, y = disk_mesh()
        density = disk_kde(np.array([[0.0, 0.0]]), x, y, k=5)
        assert np.nanmax(density) == pytest.approx(1.0)

    def test_density_peaks_nearest_a_single_particle(self):
        x, y = disk_mesh(41)
        density = disk_kde(np.array([[0.5, 0.0]]), x, y, k=5)
        peak = np.unravel_index(np.nanargmax(density), density.shape)
        assert x[peak] == pytest.approx(0.5, abs=0.1)
        assert y[peak] == pytest.approx(0.0, abs=0.1)

    def test_identical_points_do_not_produce_nan(self):
        # d(z, w) == 0 leaves tiny negative residue in the arccosh argument,
        # which must be clipped rather than becoming NaN
        x, y = disk_mesh(11)
        positions = np.array([[x[5, 5], y[5, 5]]])
        assert np.isfinite(disk_kde(positions, x, y, k=5)[5, 5])

    def test_n_selects_a_default_k(self):
        x, y = disk_mesh()
        positions = np.array([[0.1, 0.1]])
        assert disk_kde(positions, x, y, N=100) == pytest.approx(
            disk_kde(positions, x, y, k=10.0), nan_ok=True
        )


class TestBoundaryAngleHistogram:
    def test_returns_none_when_no_particle_reaches_the_threshold(self):
        histogram, edges = boundary_angle_histogram(np.zeros((10, 2)), radius_threshold=0.9)
        assert histogram is None
        assert edges is None

    def test_bin_count_and_edges_span_the_full_circle(self):
        positions = np.array([[0.95, 0.0], [0.0, -0.95], [-0.95, 0.0]])
        histogram, edges = boundary_angle_histogram(positions, radius_threshold=0.9, bins=36)
        assert len(histogram) == 36
        assert len(edges) == 37
        assert edges[0] == pytest.approx(0.0)
        assert edges[-1] == pytest.approx(2 * np.pi)

    def test_counts_only_particles_past_the_threshold(self):
        positions = np.array([[0.95, 0.0], [0.1, 0.0], [0.0, 0.99]])
        histogram, _ = boundary_angle_histogram(positions, radius_threshold=0.9)
        assert histogram.sum() == 2

    def test_angles_are_wrapped_into_zero_to_two_pi(self):
        # A particle at angle -pi/2 must be counted at 3*pi/2, not dropped
        # for falling outside the [0, 2*pi) histogram range
        positions = np.array([[0.0, -0.95]])
        histogram, _ = boundary_angle_histogram(positions, radius_threshold=0.9, bins=4)
        assert histogram.sum() == 1
        assert histogram[3] == 1

    def test_particles_are_binned_by_direction(self):
        positions = np.array([[0.95, 0.0], [0.0, 0.95], [-0.95, 0.0], [0.0, -0.95]])
        histogram, _ = boundary_angle_histogram(positions, radius_threshold=0.9, bins=4)
        assert list(histogram) == [1, 1, 1, 1]
