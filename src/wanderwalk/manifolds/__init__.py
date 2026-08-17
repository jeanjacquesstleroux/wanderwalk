"""Manifold geometry: tangent projection, noise sampling, and stepping."""

from .base import Manifold
from .hyperbolic import PoincareDisk
from .sphere import Sphere
from .torus import Torus

__all__ = ["Manifold", "PoincareDisk", "Sphere", "Torus"]
