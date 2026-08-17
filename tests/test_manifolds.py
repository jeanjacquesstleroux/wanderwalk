"""Geometric invariants each manifold must satisfy."""

import math

import numpy as np
import pytest

from wanderwalk import Manifold, PoincareDisk, Sphere, Torus

from tests.helpers import R, on_torus, r


class TestManifoldInterface:
    def test_base_class_is_abstract(self):
        with pytest.raises(TypeError):
            Manifold()

    @pytest.mark.parametrize(
        "manifold", [Sphere(), Torus(R, r), PoincareDisk()]
    )
    def test_implements_full_interface(self, manifold):
        for name in (
            "project_to_tangent",
            "project_to_manifold",
            "sample_tangent_noise",
            "project_to_tangent_multiple",
            "project_to_manifold_multiple",
            "sample_tangent_noise_multiple",
            "euler_maruyama_step",
        ):
            assert callable(getattr(manifold, name)), name

    @pytest.mark.parametrize(
        "manifold, dim", [(Sphere(), 3), (Torus(R, r), 3), (PoincareDisk(), 2)]
    )
    def test_project_to_tangent_accepts_shared_signature(self, manifold, dim):
        # Every manifold must accept (point, vector), so callers can treat
        # them polymorphically
        x = manifold.project_to_manifold(np.full(dim, 0.5))
        v = np.ones(dim)
        assert manifold.project_to_tangent(x, v).shape == (dim,)


class TestSphere:
    def test_project_to_manifold_gives_unit_norm(self):
        sphere = Sphere()
        assert np.linalg.norm(sphere.project_to_manifold(np.array([3.0, 4.0, 0.0]))) == pytest.approx(1.0)

    def test_project_to_manifold_multiple_gives_unit_norms(self):
        sphere = Sphere()
        X = np.array([[3.0, 4.0, 0.0], [0.0, 0.0, 2.0], [1.0, 1.0, 1.0]])
        norms = np.linalg.norm(sphere.project_to_manifold_multiple(X), axis=1)
        assert norms == pytest.approx(np.ones(3))

    def test_tangent_vector_is_orthogonal_to_point(self):
        sphere = Sphere()
        x = sphere.project_to_manifold(np.array([1.0, 2.0, 3.0]))
        v = sphere.project_to_tangent(x, np.array([4.0, -1.0, 0.5]))
        assert np.dot(x, v) == pytest.approx(0.0, abs=1e-12)

    def test_project_to_tangent_is_idempotent(self):
        sphere = Sphere()
        x = sphere.project_to_manifold(np.array([1.0, 2.0, 3.0]))
        once = sphere.project_to_tangent(x, np.array([4.0, -1.0, 0.5]))
        twice = sphere.project_to_tangent(x, once)
        assert twice == pytest.approx(once)

    def test_multiple_matches_single_projection(self):
        sphere = Sphere()
        X = sphere.project_to_manifold_multiple(np.random.RandomState(0).randn(5, 3))
        V = np.random.RandomState(1).randn(5, 3)
        batched = sphere.project_to_tangent_multiple(X, V)
        for i in range(5):
            assert batched[i] == pytest.approx(sphere.project_to_tangent(X[i], V[i]))

    def test_sampled_noise_is_tangent(self):
        sphere = Sphere()
        np.random.seed(0)
        x = sphere.project_to_manifold(np.array([1.0, 2.0, 3.0]))
        for _ in range(20):
            assert np.dot(x, sphere.sample_tangent_noise(x)) == pytest.approx(0.0, abs=1e-12)

    def test_sampled_noise_multiple_is_tangent(self):
        sphere = Sphere()
        np.random.seed(0)
        X = sphere.project_to_manifold_multiple(np.random.randn(50, 3))
        noise = sphere.sample_tangent_noise_multiple(X)
        assert np.sum(X * noise, axis=1) == pytest.approx(np.zeros(50), abs=1e-12)

    def test_anisotropic_noise_is_tangent(self):
        sphere = Sphere()
        np.random.seed(0)
        X = sphere.project_to_manifold_multiple(np.random.randn(50, 3))
        noise = sphere.sample_tangent_noise_anisotropic_multiple(X)
        assert np.sum(X * noise, axis=1) == pytest.approx(np.zeros(50), abs=1e-12)

    def test_anisotropic_noise_handles_degenerate_point(self):
        # x parallel to the default direction (1,1,1) makes its tangential
        # component vanish, so the fallback direction must take over
        sphere = Sphere()
        np.random.seed(0)
        x = sphere.project_to_manifold(np.array([1.0, 1.0, 1.0]))
        noise = sphere.sample_tangent_noise_anisotropic(x)
        assert np.linalg.norm(noise) > 0.0
        assert np.dot(x, noise) == pytest.approx(0.0, abs=1e-12)

    def test_anisotropic_noise_multiple_handles_degenerate_point(self):
        sphere = Sphere()
        np.random.seed(0)
        X = np.vstack([
            sphere.project_to_manifold(np.array([1.0, 1.0, 1.0])),
            sphere.project_to_manifold(np.array([1.0, 0.0, 0.0])),
        ])
        noise = sphere.sample_tangent_noise_anisotropic_multiple(X)
        assert np.all(np.isfinite(noise))
        assert np.sum(X * noise, axis=1) == pytest.approx(np.zeros(2), abs=1e-12)

    def test_euler_maruyama_step_stays_on_sphere(self):
        sphere = Sphere()
        np.random.seed(0)
        x = np.array([1.0, 0.0, 0.0])
        for _ in range(100):
            x = sphere.euler_maruyama_step(x, 0.01)
            assert np.linalg.norm(x) == pytest.approx(1.0)


class TestTorus:
    def test_parametrize_lands_on_torus(self):
        torus = Torus(R, r)
        for u in np.linspace(0, 2 * math.pi, 7):
            for v in np.linspace(0, 2 * math.pi, 7):
                assert on_torus(torus.parametrize(u, v)) == pytest.approx([0.0], abs=1e-12)

    def test_normal_vector_is_unit_length(self):
        torus = Torus(R, r)
        for u in np.linspace(0, 2 * math.pi, 5):
            for v in np.linspace(0, 2 * math.pi, 5):
                assert np.linalg.norm(torus.normal_vector(u, v)) == pytest.approx(1.0)

    def test_angles_round_trip_through_parametrize(self):
        torus = Torus(R, r)
        for u in (0.0, 1.0, 2.5, -1.5):
            for v in (0.0, 0.7, -2.0, 3.0):
                point = torus.parametrize(u, v)
                u_out, v_out = torus.angles_from_point(point)
                assert torus.parametrize(u_out, v_out) == pytest.approx(point, abs=1e-12)

    def test_angles_from_points_matches_scalar_version(self):
        torus = Torus(R, r)
        angles = [(0.3, 1.2), (2.0, -0.5), (-1.1, 2.7)]
        X = np.array([torus.parametrize(u, v) for u, v in angles])
        u_batch, v_batch = torus.angles_from_points(X)
        for i, point in enumerate(X):
            u_one, v_one = torus.angles_from_point(point)
            assert u_batch[i] == pytest.approx(u_one)
            assert v_batch[i] == pytest.approx(v_one)

    def test_project_to_manifold_lands_on_torus(self):
        torus = Torus(R, r)
        X = np.random.RandomState(0).uniform(-5, 5, size=(20, 3))
        for x in X:
            assert on_torus(torus.project_to_manifold(x)) == pytest.approx([0.0], abs=1e-10)

    def test_project_to_manifold_multiple_matches_single(self):
        torus = Torus(R, r)
        X = np.random.RandomState(0).uniform(-5, 5, size=(20, 3))
        batched = torus.project_to_manifold_multiple(X)
        assert on_torus(batched) == pytest.approx(np.zeros(20), abs=1e-10)
        for i, x in enumerate(X):
            assert batched[i] == pytest.approx(torus.project_to_manifold(x))

    def test_tangent_vector_is_orthogonal_to_normal(self):
        torus = Torus(R, r)
        u, v = 0.8, 2.1
        x = torus.parametrize(u, v)
        tangential = torus.project_to_tangent(x, np.array([1.0, -2.0, 0.5]))
        assert np.dot(tangential, torus.normal_vector(u, v)) == pytest.approx(0.0, abs=1e-12)

    def test_project_to_tangent_agrees_with_angle_version(self):
        torus = Torus(R, r)
        u, v = 1.3, -0.4
        x = torus.parametrize(u, v)
        vector = np.array([0.5, 1.5, -2.0])
        assert torus.project_to_tangent(x, vector) == pytest.approx(
            torus.project_to_tangent_at_angles(u, v, vector)
        )

    def test_project_to_tangent_multiple_matches_single(self):
        torus = Torus(R, r)
        angles = [(0.3, 1.2), (2.0, -0.5), (-1.1, 2.7)]
        X = np.array([torus.parametrize(u, v) for u, v in angles])
        V = np.random.RandomState(2).randn(3, 3)
        batched = torus.project_to_tangent_multiple(X, V)
        for i in range(3):
            assert batched[i] == pytest.approx(torus.project_to_tangent(X[i], V[i]))

    def test_sampled_noise_is_tangent(self):
        torus = Torus(R, r)
        np.random.seed(0)
        u, v = 0.6, 1.9
        x = torus.parametrize(u, v)
        normal = torus.normal_vector(u, v)
        for _ in range(20):
            assert np.dot(torus.sample_tangent_noise(x), normal) == pytest.approx(0.0, abs=1e-12)

    def test_sampled_noise_multiple_is_tangent(self):
        torus = Torus(R, r)
        np.random.seed(0)
        angles = np.random.uniform(0, 2 * math.pi, size=(30, 2))
        X = np.array([torus.parametrize(u, v) for u, v in angles])
        noise = torus.sample_tangent_noise_multiple(X)
        normals = np.array([torus.normal_vector(u, v) for u, v in angles])
        assert np.sum(noise * normals, axis=1) == pytest.approx(np.zeros(30), abs=1e-12)

    def test_euler_maruyama_step_stays_on_torus(self):
        torus = Torus(R, r)
        np.random.seed(0)
        x = torus.parametrize(0.0, 0.0)
        for _ in range(100):
            x = torus.euler_maruyama_step(x, 0.01)
            assert on_torus(x) == pytest.approx([0.0], abs=1e-10)


class TestPoincareDisk:
    def test_conformal_factor_at_origin_is_two(self):
        assert PoincareDisk().conformal_factor(np.zeros(2)) == pytest.approx(2.0)

    def test_conformal_factor_grows_toward_boundary(self):
        disk = PoincareDisk()
        factors = [disk.conformal_factor(np.array([radius, 0.0])) for radius in (0.0, 0.5, 0.9, 0.99)]
        assert all(b > a for a, b in zip(factors, factors[1:]))

    def test_project_to_tangent_is_identity(self):
        disk = PoincareDisk()
        v = np.array([1.0, -2.0])
        assert np.array_equal(disk.project_to_tangent(np.array([0.3, 0.4]), v), v)

    def test_project_to_tangent_multiple_is_identity(self):
        disk = PoincareDisk()
        V = np.random.RandomState(0).randn(4, 2)
        assert np.array_equal(disk.project_to_tangent_multiple(np.zeros((4, 2)), V), V)

    def test_interior_point_is_left_alone(self):
        disk = PoincareDisk()
        x = np.array([0.3, 0.4])
        assert np.array_equal(disk.project_to_manifold(x), x)

    def test_boundary_point_is_clamped_inside(self):
        disk = PoincareDisk(epsilon=1e-6)
        clamped = disk.project_to_manifold(np.array([3.0, 4.0]))
        assert np.linalg.norm(clamped) == pytest.approx(1.0 - 1e-6)
        # Clamping is radial, so the direction must be preserved
        assert clamped[1] / clamped[0] == pytest.approx(4.0 / 3.0)

    def test_project_to_manifold_multiple_matches_single(self):
        disk = PoincareDisk(epsilon=1e-6)
        X = np.array([[0.1, 0.2], [3.0, 4.0], [0.0, 0.999999], [-2.0, 0.0]])
        batched = disk.project_to_manifold_multiple(X)
        assert np.all(np.linalg.norm(batched, axis=1) < 1.0)
        for i, x in enumerate(X):
            assert batched[i] == pytest.approx(disk.project_to_manifold(x))

    def test_geodesic_distance_from_origin_matches_closed_form(self):
        disk = PoincareDisk()
        for radius in (0.0, 0.1, 0.5, 0.9):
            x = np.array([radius, 0.0])
            assert disk.geodesic_distance_from_origin(x) == pytest.approx(2 * math.atanh(radius))

    def test_geodesic_distance_from_origin_multiple_matches_single(self):
        disk = PoincareDisk()
        X = np.array([[0.0, 0.0], [0.3, 0.4], [-0.5, 0.0], [0.1, -0.8]])
        batched = disk.geodesic_distance_from_origin_multiple(X)
        for i, x in enumerate(X):
            assert batched[i] == pytest.approx(disk.geodesic_distance_from_origin(x))

    def test_geodesic_distance_is_zero_between_identical_points(self):
        disk = PoincareDisk()
        x = np.array([0.3, -0.4])
        assert disk.geodesic_distance(x, x) == pytest.approx(0.0, abs=1e-12)

    def test_geodesic_distance_is_symmetric(self):
        disk = PoincareDisk()
        z, w = np.array([0.3, -0.4]), np.array([-0.1, 0.5])
        assert disk.geodesic_distance(z, w) == pytest.approx(disk.geodesic_distance(w, z))

    def test_geodesic_distance_agrees_with_radial_formula_from_origin(self):
        disk = PoincareDisk()
        origin = np.zeros(2)
        x = np.array([0.6, 0.0])
        assert disk.geodesic_distance(origin, x) == pytest.approx(
            disk.geodesic_distance_from_origin(x)
        )

    def test_geodesic_distance_multiple_matches_single(self):
        disk = PoincareDisk()
        Z = np.array([[0.1, 0.2], [-0.5, 0.3], [0.0, 0.0]])
        w = np.array([0.4, -0.2])
        batched = disk.geodesic_distance_multiple(Z, w)
        for i, z in enumerate(Z):
            assert batched[i] == pytest.approx(disk.geodesic_distance(z, w))

    def test_euler_maruyama_step_stays_in_disk(self):
        disk = PoincareDisk()
        np.random.seed(0)
        x = np.zeros(2)
        for _ in range(200):
            x = disk.euler_maruyama_step(x, 0.01)
            assert np.linalg.norm(x) < 1.0
