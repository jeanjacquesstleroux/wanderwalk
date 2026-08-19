"""The heat kernel on S^2, empirical and analytic.

These need SciPy, which ships in the "notebooks" extra rather than the
numpy-only core, so the whole module skips when it is absent.
"""

import numpy as np
import pytest

pytest.importorskip("scipy")

from wanderwalk.heat_kernel import (  # noqa: E402
    estimate_density,
    estimate_heat_kernel,
    estimate_theoretical_heat_kernel,
)

UNIFORM = 1.0 / (4.0 * np.pi)


@pytest.fixture(scope="module")
def grids():
    return np.linspace(0, np.pi, 50), np.linspace(0, 2 * np.pi, 50)


@pytest.fixture(scope="module")
def samples():
    np.random.seed(0)
    return estimate_heat_kernel()


class TestTheoreticalHeatKernel:
    def test_shape_is_theta_by_phi(self, grids):
        theta, phi = grids
        assert estimate_theoretical_heat_kernel(theta, phi, 1.0).shape == (
            len(theta),
            len(phi),
        )

    def test_is_axisymmetric(self, grids):
        theta, phi = grids
        kernel = estimate_theoretical_heat_kernel(theta, phi, 1.0)
        assert np.allclose(kernel, kernel[:, :1])

    def test_flattens_to_the_uniform_density(self, grids):
        theta, phi = grids
        assert np.allclose(
            estimate_theoretical_heat_kernel(theta, phi, 50.0), UNIFORM
        )

    def test_integrates_to_one_over_the_sphere(self):
        # A finer grid than the 50 points estimate_density uses, so this
        # tests the kernel normalization rather than the rectangle rule.
        theta = np.linspace(0, np.pi, 800)
        phi = np.linspace(0, 2 * np.pi, 800)
        kernel = estimate_theoretical_heat_kernel(theta, phi, 2.0)
        dtheta = theta[1] - theta[0]
        dphi = phi[1] - phi[0]
        integral = np.sum(kernel * np.sin(theta)[:, None] * dtheta * dphi)
        assert integral == pytest.approx(1.0, abs=0.005)

    def test_hotter_at_the_pole_it_started_from(self, grids):
        theta, phi = grids
        kernel = estimate_theoretical_heat_kernel(theta, phi, 0.5)
        assert kernel[0, 0] > kernel[-1, 0]

    def test_uses_the_half_laplacian_generator_convention(self, grids):
        # This project generates Brownian motion with (1/2)Laplacian, so the
        # expansion carries exp(-l(l+1)t/2). The l=1 mode therefore decays
        # like exp(-t), not exp(-2t). Isolate it as the pole-to-pole
        # difference, where even-l terms cancel and l>=3 is negligible.
        theta, phi = grids

        def dipole(t):
            kernel = estimate_theoretical_heat_kernel(theta, phi, t)
            return kernel[0, 0] - kernel[-1, 0]

        # One unit of time must attenuate the mode by exactly e, which is
        # what separates this convention from the exp(-l(l+1)t) one (e^2).
        # Measured out at t = 4 and 5, where the l = 3 residual is ~1e-9.
        assert dipole(4.0) / dipole(5.0) == pytest.approx(np.e, rel=1e-6)


class TestEmpiricalHeatKernel:
    def test_samples_have_one_row_per_path_and_time(self, samples):
        assert samples.shape == (2000, 4, 3)

    def test_every_sample_is_on_the_unit_sphere(self, samples):
        assert np.allclose(np.linalg.norm(samples, axis=2), 1.0)

    @pytest.mark.parametrize("time_index", range(4))
    def test_density_integrates_to_one(self, samples, time_index):
        theta, _, density, dtheta, dphi = estimate_density(samples, time_index)
        integral = np.sum(density * np.sin(theta)[:, None] * dtheta * dphi)
        assert integral == pytest.approx(1.0, abs=1e-6)

    @pytest.mark.parametrize(
        "time_index, t, tolerance",
        [(1, 0.5, 0.06), (2, 1.0, 0.03), (3, 2.0, 0.01)],
    )
    def test_matches_the_analytic_kernel(self, samples, time_index, t, tolerance):
        # t = 0.1 is excluded: the particles are still packed into a cap much
        # narrower than the KDE bandwidth, so the estimate is smoothing-bound
        # rather than simulation-bound. The tolerance tightens as t grows for
        # the same reason.
        theta, phi, empirical, _, _ = estimate_density(samples, time_index)
        theoretical = estimate_theoretical_heat_kernel(theta, phi, t)
        largest_gap = np.abs(empirical.mean(axis=1) - theoretical.mean(axis=1)).max()
        assert largest_gap < tolerance
