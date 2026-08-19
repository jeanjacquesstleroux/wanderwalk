# Manifolds

Each surface is a class implementing a shared three-method interface:
project a vector into the tangent plane, project a stray point back onto the
surface, and sample noise that already lies in the tangent plane. Every
method has a vectorized `_multiple` twin that takes an `(N, d)` array, and
those are what the simulators call.

See [driving the manifolds directly](../tutorials/04-manifolds.md) for worked
examples, including how to add a surface of your own.

## Manifold

::: wanderwalk.manifolds.base.Manifold

## Sphere

::: wanderwalk.manifolds.sphere.Sphere

## Torus

::: wanderwalk.manifolds.torus.Torus

## PoincareDisk

::: wanderwalk.manifolds.hyperbolic.PoincareDisk
