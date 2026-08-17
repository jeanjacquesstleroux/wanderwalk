"""Shared geometric checks used across the test modules."""

import numpy as np

R = 3.0
r = 1.0


def on_torus(points, major=R, minor=r):
    """Residual of the torus implicit equation, zero for points on the torus.

    Arguments:
        points: A point in R^3, or an (N, 3) array of points.
        major: Major radius of the torus.
        minor: Minor radius of the torus.

    Returns:
        An (N,) array of residuals (rho - major)^2 + z^2 - minor^2.
    """
    points = np.atleast_2d(points)
    rho = np.sqrt(points[:, 0] ** 2 + points[:, 1] ** 2)
    return (rho - major) ** 2 + points[:, 2] ** 2 - minor**2
