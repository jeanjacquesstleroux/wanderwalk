# Driving the manifolds directly

The simulators are a convenience wrapper. Underneath, each surface is a small
class that knows three things: how to project a vector into the tangent plane
at a point, how to project a stray point back onto the surface, and how to
draw random noise that lies in the tangent plane. Everything else is built
from those.

Reach for this layer when you want to step one particle at a time, inspect
the geometry, interleave the simulation with your own logic, or add a surface
of your own.

## The shared interface

`ww.Manifold` is the abstract base class. It declares exactly three methods:

```python
import wanderwalk as ww

print(sorted(ww.Manifold.__abstractmethods__))
print([issubclass(c, ww.Manifold) for c in (ww.Sphere, ww.Torus, ww.PoincareDisk)])
```

```text
['project_to_manifold', 'project_to_tangent', 'sample_tangent_noise']
[True, True, True]
```

| Method | Job |
| --- | --- |
| `project_to_tangent(x, v)` | Strip off the part of `v` that points away from the surface, leaving a vector a particle at `x` could actually move along. |
| `project_to_manifold(x)` | Pull a point that has drifted off the surface back onto it. |
| `sample_tangent_noise(x)` | Draw a random vector already lying in the tangent plane at `x`. |

On top of those, each class adds `euler_maruyama_step(x, dt)`, which is the
whole simulation loop for a single particle and a single step.

## Stepping one particle

```python
import numpy as np
import wanderwalk as ww

np.random.seed(0)
sphere = ww.Sphere()

point = np.array([1.0, 0.0, 0.0])
for _ in range(100):
    point = sphere.euler_maruyama_step(point, dt=0.01)

print("after 100 steps:", np.round(point, 4))
print("norm:", np.linalg.norm(point))
```

```text
after 100 steps: [ 0.4427  0.3769 -0.8136]
norm: 1.0
```

That loop is what `ww.sphere_simulator` runs, except the simulator does it
for all `N` particles at once with array operations instead of a Python loop
per particle. For anything beyond a handful of particles, prefer the
simulator; see [reproducibility and performance](../guides/reproducibility.md)
for how much difference it makes.

## Inspecting the geometry

The projection methods are useful on their own. On the unit sphere, the
tangent plane at a point is everything orthogonal to it, so projecting a
vector there just removes its radial component:

```python
import numpy as np
import wanderwalk as ww

sphere = ww.Sphere()

north_pole = np.array([0.0, 0.0, 1.0])
vector = np.array([1.0, 2.0, 3.0])

tangential = sphere.project_to_tangent(north_pole, vector)
print("tangential part:", tangential)
print("dot with the point:", np.dot(tangential, north_pole))
```

```text
tangential part: [1. 2. 0.]
dot with the point: 0.0
```

The `z` component is gone, and the result is orthogonal to the point, which
is the defining property of a tangent vector on the sphere.

`project_to_manifold` is just as direct. On the sphere it normalizes:

```python
import numpy as np
import wanderwalk as ww

print(ww.Sphere().project_to_manifold(np.array([3.0, 4.0, 0.0])))
```

```text
[0.6 0.8 0. ]
```

On the torus it finds the nearest point on the tube:

```python
import numpy as np
import wanderwalk as ww

torus = ww.Torus(R=3.0, r=1.0)

print("normal at (u, v) = (0, 0):", torus.normal_vector(0.0, 0.0))
print("nearest torus point to [5, 0, 0]:", torus.project_to_manifold(np.array([5.0, 0.0, 0.0])))
```

```text
normal at (u, v) = (0, 0): [1. 0. 0.]
nearest torus point to [5, 0, 0]: [4. 0. 0.]
```

The point `[5, 0, 0]` sits one unit outside the outer equator, and gets pulled
straight back in to `[4, 0, 0] = R + r`.

## The `_multiple` variants

Every method has a vectorized twin that takes an `(N, d)` array instead of a
single point, and these are what the simulators actually call:

| Single point | Many points |
| --- | --- |
| `project_to_manifold(x)` | `project_to_manifold_multiple(X)` |
| `project_to_tangent(x, v)` | `project_to_tangent_multiple(X, V)` |
| `sample_tangent_noise(x)` | `sample_tangent_noise_multiple(X)` |

They compute the same thing:

```python
import numpy as np
import wanderwalk as ww

sphere = ww.Sphere()
points = np.array([[3.0, 4.0, 0.0], [0.0, 0.0, 2.0], [1.0, 1.0, 1.0]])

one_at_a_time = np.array([sphere.project_to_manifold(p) for p in points])
all_at_once = sphere.project_to_manifold_multiple(points)

print("identical:", np.allclose(one_at_a_time, all_at_once))
```

```text
identical: True
```

!!! note "Sphere and torus only"

    `sample_tangent_noise_anisotropic` and its `_multiple` twin exist on
    `Sphere` and `Torus` but not on `PoincareDisk`. The anisotropic direction
    is chosen using the ambient R^3 embedding, and the Poincare disk does not
    have one. See [the hyperbolic tutorial](03-hyperbolic.md).

## Torus angles

`Torus` carries two extra pairs of methods, because a torus point is more
naturally described by two angles than by three coordinates:

```python
import numpy as np
import wanderwalk as ww

torus = ww.Torus(R=3.0, r=1.0)

point = torus.parametrize(np.pi / 2, np.pi / 4)
print("point at (pi/2, pi/4):", np.round(point, 4))

u, v = torus.angles_from_point(point)
print("angles recovered:", round(u, 4), round(v, 4))
```

```text
point at (pi/2, pi/4): [0.     3.7071 0.7071]
angles recovered: 1.5708 0.7854
```

`angles_from_points` (plural) does the same for an `(N, 3)` array and returns
two `(N,)` arrays, which is what you want when post-processing a trajectory.

## Poincare disk extras

`PoincareDisk` adds the metric quantities that have no analogue on an
embedded surface:

```python
import numpy as np
import wanderwalk as ww

disk = ww.PoincareDisk()

a = np.array([0.3, 0.0])
b = np.array([0.0, 0.3])

print(f"conformal factor at a: {disk.conformal_factor(a):.4f}")
print(f"distance from origin to a: {disk.geodesic_distance_from_origin(a):.4f}")
print(f"distance from a to b: {disk.geodesic_distance(a, b):.4f}")
```

```text
conformal factor at a: 2.1978
distance from origin to a: 0.6190
distance from a to b: 0.9016
```

Note that `a` and `b` are the same Euclidean distance from the origin but
`0.9016` apart from each other, which is more than either is from the origin.
Hyperbolic space has more room in it than the picture suggests.

## Writing your own surface

Subclass `ww.Manifold` and implement the three abstract methods. Here is a
cylinder of radius 1 about the `z` axis, which is flat but not simply
connected:

```python
import numpy as np
import wanderwalk as ww


class Cylinder(ww.Manifold):
    """The unit cylinder x^2 + y^2 = 1, unbounded in z."""

    def project_to_manifold(self, x):
        radial = x.copy()
        radial[2] = 0.0
        radial /= np.linalg.norm(radial)
        return np.array([radial[0], radial[1], x[2]])

    def project_to_tangent(self, x, v):
        normal = np.array([x[0], x[1], 0.0])
        return v - np.dot(v, normal) * normal

    def sample_tangent_noise(self, x):
        return self.project_to_tangent(x, np.random.randn(3))


np.random.seed(0)
cylinder = Cylinder()

point = np.array([1.0, 0.0, 0.0])
for _ in range(500):
    point = cylinder.project_to_manifold(point + np.sqrt(0.01) * cylinder.sample_tangent_noise(point))

print("radius stayed at:", round(float(np.hypot(point[0], point[1])), 12))
print("drifted in z to:", round(float(point[2]), 4))
```

```text
radius stayed at: 1.0
drifted in z to: -2.7251
```

The particle wraps around the cylinder forever while diffusing freely up and
down, which is the behavior you would expect on a surface that is compact in
one direction and infinite in the other.

To plug a new surface into the vectorized simulators you would also need the
`_multiple` variants, since that is what the simulator loop calls. The
existing implementations in
[`src/wanderwalk/manifolds/`](https://github.com/jeanjacquesstleroux/wanderwalk/tree/main/src/wanderwalk/manifolds)
are the pattern to follow.

## What next

- [Density estimation](05-density.md), for turning positions into a picture.
- The [API reference](../reference/manifolds.md), which lists every method on
  every manifold with its arguments and return values.
