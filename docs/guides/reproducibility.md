# Reproducibility and performance

Practical notes on getting the same answer twice, choosing `dt`, `T`, and
`N`, and not running out of memory.

## Seeding

The simulators draw from NumPy's global random state through `np.random`.
Seeding it before a run makes that run repeatable:

```python
import numpy as np
import wanderwalk as ww

np.random.seed(0)
first = ww.sphere_simulator(T=50, N=10, dt=0.01, noise_type="isotropic")

np.random.seed(0)
second = ww.sphere_simulator(T=50, N=10, dt=0.01, noise_type="isotropic")

print("identical:", np.array_equal(first, second))
```

```text
identical: True
```

The seed has to be reset before every run you want to reproduce, not just
once at the top of the script. Two consecutive calls after a single seed
consume different draws and give different answers:

```python
import numpy as np
import wanderwalk as ww

np.random.seed(0)
a = ww.sphere_simulator(T=50, N=10, dt=0.01, noise_type="isotropic")
b = ww.sphere_simulator(T=50, N=10, dt=0.01, noise_type="isotropic")

print("second call matches the first:", np.array_equal(a, b))
```

```text
second call matches the first: False
```

That is correct behavior for a stream of random numbers, and it is what you
want when running independent replicates. It only bites when you assume one
seed at the top of a notebook pins every cell below it.

!!! warning "The global state is shared"

    Because the simulators use `np.random` rather than taking a `Generator`,
    anything else in your process that draws from the global state will shift
    the results, including library code you did not write. If you need
    airtight reproducibility across a larger program, seed immediately before
    each simulator call.

    A `rng` or `seed` parameter would be a natural future addition. Today
    there is not one.

## Choosing `dt`

Euler-Maruyama is a first-order scheme, so its error shrinks as `dt` shrinks.
Too large a step and the answer is simply wrong, not merely noisy. The
hyperbolic plane makes this dramatic, because the conformal factor varies
steeply and a large step can jump across a region where the metric changed a
lot.

Here is the same physical quantity, the mean geodesic distance from the
origin at `t = 5`, computed at four step sizes:

```python
import numpy as np
import wanderwalk as ww

disk = ww.PoincareDisk()

for dt in (0.5, 0.1, 0.01, 0.001):
    T = int(round(5.0 / dt))
    np.random.seed(0)
    trajectory = ww.hyperbolic_simulator(T=T, N=4000, dt=dt)
    mean_distance = disk.geodesic_distance_from_origin_multiple(trajectory[-1]).mean()
    print(f"dt = {dt:<7} T = {T:<6} mean geodesic distance = {mean_distance:.4f}")
```

```text
dt = 0.5     T = 10     mean geodesic distance = 11.6818
dt = 0.1     T = 50     mean geodesic distance = 4.2869
dt = 0.01    T = 500    mean geodesic distance = 3.7259
dt = 0.001   T = 5000   mean geodesic distance = 3.7291
```

At `dt = 0.5` the answer is off by a factor of three. At `dt = 0.01` it has
converged: shrinking by another factor of ten moves it by 0.003, which is
less than the sampling noise across seeds.

The practical recipe is the one this table demonstrates. Pick a `dt`, halve
it, and check whether the quantity you care about moves. If it does, halve
again. `dt = 0.01` is a reasonable default for all three surfaces at unit
scale, and it is what every example in these docs uses.

!!! note "`dt` interacts with the size of your surface"

    A step is small or large relative to the local geometry. On a torus with
    `r = 0.05`, a step of `sqrt(0.01) = 0.1` is larger than the tube itself,
    and the projection back onto the surface stops meaning anything. Scale
    `dt` down with the smallest length scale in your geometry.

## Choosing `T` and `N`

The two do different jobs and are not interchangeable:

- `T` sets how long you simulate. Total simulated time is `T * dt`. Increase
  it when the process has not equilibrated, or has not gone far enough for
  whatever asymptotic behavior you are after.
- `N` sets how many independent particles you average over. Increase it when
  your estimate is too noisy.

Statistical error falls like `1 / sqrt(N)`, so quadrupling `N` halves the
noise. That is why the [sphere tutorial](../tutorials/01-sphere.md) sees the
mean position stall around 0.03 with `N = 2000`: `1 / sqrt(2000)` is about
0.022, and no amount of extra `T` gets past a floor set by `N`.

If a statistic looks wrong, work out which knob it is asking for. Not yet
equilibrated is a `T` problem. Noisy is an `N` problem. Systematically off is
a `dt` problem.

## Memory

The simulators return the whole trajectory, not just the final positions.
That is deliberate, since the time evolution is usually the interesting part,
but it means memory grows with `T * N`.

An array of float64 costs `T * N * d * 8` bytes:

| `T` | `N` | `d` | Size |
| --- | --- | --- | --- |
| 200 | 500 | 3 | 2.4 MB |
| 1000 | 1000 | 3 | 24 MB |
| 1000 | 1000 | 2 | 16 MB |
| 5000 | 10000 | 3 | 1.2 GB |

```python
def trajectory_megabytes(T, N, d):
    return T * N * d * 8 / 1e6

print(f"{trajectory_megabytes(5000, 10000, 3):.0f} MB")
```

```text
1200 MB
```

The bottom row of that table will exhaust a laptop. If you only need the
final distribution, run several smaller batches and keep just `trajectory[-1]`
from each:

```python
import numpy as np
import wanderwalk as ww

final_positions = []
for batch in range(5):
    np.random.seed(batch)
    trajectory = ww.sphere_simulator(T=1000, N=2000, dt=0.01, noise_type="isotropic")
    final_positions.append(trajectory[-1])

combined = np.concatenate(final_positions)
print("combined shape:", combined.shape)
```

```text
combined shape: (10000, 3)
```

Peak memory there is one batch, 48 MB, rather than 240 MB, and each batch has
its own seed so the batches stay independent.

## Prefer the vectorized simulators

The manifold classes expose `euler_maruyama_step` for one particle at a time,
which is useful for
[understanding the scheme](../tutorials/04-manifolds.md) or interleaving your
own logic. It is not how you should run a large simulation. The simulators do
the same arithmetic with array operations over all `N` particles at once:

```python
import time

import numpy as np
import wanderwalk as ww

np.random.seed(0)
start = time.perf_counter()
ww.sphere_simulator(T=500, N=1000, dt=0.01, noise_type="isotropic")
vectorized = time.perf_counter() - start

sphere = ww.Sphere()
np.random.seed(0)
start = time.perf_counter()
for _ in range(1000):
    point = np.array([1.0, 0.0, 0.0])
    for _ in range(500):
        point = sphere.euler_maruyama_step(point, dt=0.01)
per_particle = time.perf_counter() - start

print(f"speedup: {per_particle / vectorized:.0f}x")
```

The gap on the machine these docs were built on was about 47x, and it widens
as `N` grows, because the Python interpreter overhead per step is paid once
per particle in the loop and once per time step in the simulator.

!!! note "Why the numbers above are not in a `text` block"

    Timings depend on the machine. Every other output in this documentation
    is checked against a real run, and a timing would fail that check on
    anyone else's hardware.

## What next

- [Driving the manifolds directly](../tutorials/04-manifolds.md), for the
  single-particle API.
- [The interactive app](streamlit-app.md), which exposes `dt`, `T`, and `N`
  as sliders so you can watch the effect of changing them.
