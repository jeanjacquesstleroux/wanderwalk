# Getting started

## Install

The core library depends only on NumPy:

```bash
pip install wanderwalk
```

That is all you need for every simulator and every manifold. The tutorials
that draw pictures also use matplotlib, and the heat kernel tutorial uses
SciPy; both arrive with the `notebooks` extra:

```bash
pip install "wanderwalk[notebooks]"
```

## The `ww` alias

wanderwalk is conventionally imported under the alias `ww`, the way NumPy is
imported as `np`:

```python
import numpy as np
import wanderwalk as ww
```

Every example in this documentation uses that convention. The whole public
API hangs off the alias:

```text
Simulators               Geometry            Density estimation
ww.sphere_simulator      ww.Sphere           ww.sphere_kde
ww.torus_simulator       ww.Torus            ww.disk_kde
ww.hyperbolic_simulator  ww.PoincareDisk     ww.boundary_angle_histogram
                         ww.Manifold
```

That list is exactly what the package declares as public, so you can always
recover it at runtime:

```python
import wanderwalk as ww

print(sorted(n for n in ww.__all__ if not n.startswith("__")))
```

```text
['Manifold', 'PoincareDisk', 'Sphere', 'Torus', 'boundary_angle_histogram', 'disk_kde', 'hyperbolic_simulator', 'sphere_kde', 'sphere_simulator', 'torus_simulator']
```

!!! note "One module sits outside the alias"

    `wanderwalk.heat_kernel` needs SciPy, which the numpy-only core install
    does not pull in. So it is not imported into the top-level namespace, and
    `ww.heat_kernel` will not resolve. Import it by path when you need it:

    ```python
    from wanderwalk.heat_kernel import estimate_heat_kernel
    ```

## Your first simulation

```python
import numpy as np
import wanderwalk as ww

np.random.seed(0)
trajectory = ww.sphere_simulator(T=200, N=500, dt=0.01, noise_type="isotropic")

print(trajectory.shape)
```

```text
(200, 500, 3)
```

That single call simulated 500 independent particles for 200 time steps. The
four arguments are:

| Argument | Meaning |
| --- | --- |
| `T` | How many time steps to advance. |
| `N` | How many independent particles to simulate at once. |
| `dt` | The size of each time step. Total simulated time is `T * dt`. |
| `noise_type` | `"isotropic"` for motion in all tangent directions, `"anisotropic"` for motion constrained to a single tangent direction. |

## Reading a trajectory array

Every simulator returns the full trajectory, not just where the particles
ended up, so you can inspect both the time evolution and the terminal
distribution. The array is indexed `[time, particle, coordinate]`:

```python
trajectory[-1]        # (500, 3) final position of every particle
trajectory[:, 0]      # (200, 3) the whole path of particle 0
trajectory[50, 7]     # (3,)     particle 7 at time step 50
```

The last axis is the ambient coordinate. It is 3 for the sphere and the
torus, which are surfaces sitting inside R^3, and 2 for the Poincare disk,
which is represented intrinsically:

```python
np.random.seed(0)

on_sphere = ww.sphere_simulator(T=200, N=500, dt=0.01, noise_type="isotropic")
on_torus = ww.torus_simulator(T=200, N=500, dt=0.01, R=3.0, r=1.0)
in_disk = ww.hyperbolic_simulator(T=200, N=500, dt=0.01)

print(on_sphere.shape, on_torus.shape, in_disk.shape)
```

```text
(200, 500, 3) (200, 500, 3) (200, 500, 2)
```

## Checking that the particles stayed on the surface

The point of the projection step in each simulator is that a particle never
drifts off its surface. On the unit sphere that is easy to check: every
position should have norm 1.

```python
import numpy as np
import wanderwalk as ww

np.random.seed(0)
trajectory = ww.sphere_simulator(T=200, N=500, dt=0.01, noise_type="isotropic")

norms = np.linalg.norm(trajectory[-1], axis=1)
print(f"largest deviation from 1: {np.abs(norms - 1).max():.2e}")
```

```text
largest deviation from 1: 2.22e-16
```

That is floating-point rounding, not drift. It stays there no matter how
long you run, because every step ends with a projection back onto the
surface.

## Reproducibility

The simulators draw from NumPy's global random state, so seeding `np.random`
before a run makes it repeatable:

```python
np.random.seed(0)
first = ww.sphere_simulator(T=50, N=10, dt=0.01, noise_type="isotropic")

np.random.seed(0)
second = ww.sphere_simulator(T=50, N=10, dt=0.01, noise_type="isotropic")

print(np.array_equal(first, second))
```

```text
True
```

[Reproducibility and performance](guides/reproducibility.md) covers the
consequences of using the global state, and how to choose `dt`, `T`, and `N`.

## Next steps

- [Brownian motion on the sphere](tutorials/01-sphere.md), which is the best
  place to build intuition, since the long-run answer is known exactly.
- [The hyperbolic plane](tutorials/03-hyperbolic.md), where the behavior is
  most unlike the flat case.
- [Driving the manifolds directly](tutorials/04-manifolds.md), if you want to
  step one particle at a time or add your own surface.
