"""wanderwalk: Brownian motion on Riemannian 2-manifolds.

Simulates Brownian motion on curved surfaces using the Euler-Maruyama
scheme, vectorized over many particles with NumPy. Three surfaces are
supported: the unit sphere S^2, the torus T^2, and the hyperbolic plane H^2
in the Poincare disk model.

Basic use:

    import numpy as np
    from wanderwalk import sphere_simulator

    np.random.seed(0)
    trajectory = sphere_simulator(T=200, N=500, dt=0.01, noise_type="isotropic")
    final_positions = trajectory[-1]
"""

from .manifolds import Manifold, PoincareDisk, Sphere, Torus
from .simulation import hyperbolic_simulator, sphere_simulator, torus_simulator
from .visualization import boundary_angle_histogram, disk_kde, sphere_kde

__version__ = "0.1.0"

__all__ = [
    "Manifold",
    "PoincareDisk",
    "Sphere",
    "Torus",
    "boundary_angle_histogram",
    "disk_kde",
    "hyperbolic_simulator",
    "sphere_kde",
    "sphere_simulator",
    "torus_simulator",
    "__version__",
]
