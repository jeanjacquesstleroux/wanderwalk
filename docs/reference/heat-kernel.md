# Heat kernel

Empirical and analytic heat kernel on the unit sphere, for comparing a
simulated distribution against the exact answer.

This module needs SciPy, which the numpy-only core install does not pull in,
so it is deliberately not re-exported at the top level. `ww.heat_kernel` will
not resolve. Import it by path:

```python
from wanderwalk.heat_kernel import estimate_heat_kernel
```

See the [heat kernel tutorial](../tutorials/06-heat-kernel.md) for a worked
comparison, and note the generator convention discussed there: this project
uses `(1/2) Laplacian`, so the spectral expansion carries `exp(-l(l+1)t/2)`.

::: wanderwalk.heat_kernel
    options:
      show_root_heading: false
      show_root_toc_entry: false
