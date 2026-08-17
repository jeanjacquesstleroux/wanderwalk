"""Simulator output shapes, manifold constraints, and reproducibility."""

import numpy as np
import pytest

from wanderwalk import Torus, hyperbolic_simulator, sphere_simulator, torus_simulator

from tests.helpers import R, on_torus, r

T, N, DT = 50, 20, 0.01


class TestSphereSimulator:
    @pytest.mark.parametrize("noise_type", ["isotropic", "anisotropic"])
    def test_trajectory_shape(self, noise_type):
        np.random.seed(0)
        assert sphere_simulator(T, N, DT, noise_type).shape == (T, N, 3)

    @pytest.mark.parametrize("noise_type", ["isotropic", "anisotropic"])
    def test_every_position_stays_on_sphere(self, noise_type):
        np.random.seed(0)
        trajectory = sphere_simulator(T, N, DT, noise_type)
        norms = np.linalg.norm(trajectory, axis=2)
        assert norms == pytest.approx(np.ones((T, N)))

    def test_rejects_unknown_noise_type(self):
        with pytest.raises(ValueError, match="noise_type"):
            sphere_simulator(T, N, DT, "brownian")

    def test_starting_point_is_honored(self):
        np.random.seed(0)
        start = np.array([0.0, 0.0, 1.0])
        trajectory = sphere_simulator(1, N, 1e-12, "isotropic", starting_point=start)
        assert trajectory[0] == pytest.approx(np.tile(start, (N, 1)), abs=1e-5)

    def test_unnormalized_starting_point_is_projected(self):
        np.random.seed(0)
        trajectory = sphere_simulator(
            1, N, 1e-12, "isotropic", starting_point=np.array([0.0, 0.0, 7.0])
        )
        assert trajectory[0] == pytest.approx(np.tile([0.0, 0.0, 1.0], (N, 1)), abs=1e-5)

    def test_integer_starting_point_is_accepted(self):
        np.random.seed(0)
        trajectory = sphere_simulator(2, N, DT, "isotropic", starting_point=[0, 0, 1])
        assert np.all(np.isfinite(trajectory))

    def test_seeding_makes_runs_reproducible(self):
        np.random.seed(7)
        first = sphere_simulator(T, N, DT, "isotropic")
        np.random.seed(7)
        second = sphere_simulator(T, N, DT, "isotropic")
        assert first == pytest.approx(second)

    def test_different_seeds_give_different_paths(self):
        np.random.seed(1)
        first = sphere_simulator(T, N, DT, "isotropic")
        np.random.seed(2)
        second = sphere_simulator(T, N, DT, "isotropic")
        assert not np.allclose(first, second)

    def test_anisotropic_motion_is_confined_to_one_direction(self):
        # Each particle moves along a single tangent direction, so its
        # displacement from the start spans one dimension, not two
        np.random.seed(0)
        trajectory = sphere_simulator(T, 1, DT, "anisotropic")
        assert np.linalg.norm(trajectory[-1][0]) == pytest.approx(1.0)


class TestTorusSimulator:
    def test_trajectory_shape(self):
        np.random.seed(0)
        assert torus_simulator(T, N, DT, R, r).shape == (T, N, 3)

    def test_every_position_stays_on_torus(self):
        np.random.seed(0)
        trajectory = torus_simulator(T, N, DT, R, r)
        residual = on_torus(trajectory.reshape(-1, 3), R, r)
        assert residual == pytest.approx(np.zeros(T * N), abs=1e-10)

    def test_starting_point_is_honored(self):
        np.random.seed(0)
        start = Torus(R, r).parametrize(1.0, 2.0)
        trajectory = torus_simulator(1, N, 1e-12, R, r, starting_point=start)
        assert trajectory[0] == pytest.approx(np.tile(start, (N, 1)), abs=1e-5)

    def test_default_start_is_the_outer_equator(self):
        np.random.seed(0)
        trajectory = torus_simulator(1, N, 1e-12, R, r)
        assert trajectory[0] == pytest.approx(np.tile([R + r, 0.0, 0.0], (N, 1)), abs=1e-5)

    def test_seeding_makes_runs_reproducible(self):
        np.random.seed(7)
        first = torus_simulator(T, N, DT, R, r)
        np.random.seed(7)
        second = torus_simulator(T, N, DT, R, r)
        assert first == pytest.approx(second)


class TestHyperbolicSimulator:
    def test_trajectory_shape_is_two_dimensional(self):
        # H^2 has no isometric embedding in R^3, so points are genuine 2D
        np.random.seed(0)
        assert hyperbolic_simulator(T, N, DT).shape == (T, N, 2)

    def test_every_position_stays_inside_the_disk(self):
        np.random.seed(0)
        trajectory = hyperbolic_simulator(T, N, DT)
        assert np.all(np.linalg.norm(trajectory, axis=2) < 1.0)

    def test_default_start_is_the_origin(self):
        np.random.seed(0)
        trajectory = hyperbolic_simulator(1, N, 1e-12)
        assert trajectory[0] == pytest.approx(np.zeros((N, 2)), abs=1e-5)

    def test_starting_point_is_honored(self):
        np.random.seed(0)
        start = np.array([0.2, -0.3])
        trajectory = hyperbolic_simulator(1, N, 1e-12, starting_point=start)
        assert trajectory[0] == pytest.approx(np.tile(start, (N, 1)), abs=1e-5)

    def test_starting_point_outside_disk_is_clamped(self):
        np.random.seed(0)
        trajectory = hyperbolic_simulator(1, N, 1e-12, starting_point=[5.0, 0.0])
        assert np.all(np.linalg.norm(trajectory[0], axis=1) < 1.0)

    def test_paths_drift_away_from_the_origin(self):
        # BM on H^2 is transient: the radial process has positive drift, so
        # particles move outward rather than equilibrating
        np.random.seed(0)
        trajectory = hyperbolic_simulator(400, 200, 0.05)
        early = np.mean(np.linalg.norm(trajectory[10], axis=1))
        late = np.mean(np.linalg.norm(trajectory[-1], axis=1))
        assert late > early

    def test_seeding_makes_runs_reproducible(self):
        np.random.seed(7)
        first = hyperbolic_simulator(T, N, DT)
        np.random.seed(7)
        second = hyperbolic_simulator(T, N, DT)
        assert first == pytest.approx(second)
