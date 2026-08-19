# Visualization

Kernel density estimation for particle distributions, one estimator per
geometry, plus a histogram for the hyperbolic boundary. All three are
re-exported at the top level as `ww.sphere_kde`, `ww.disk_kde`, and
`ww.boundary_angle_histogram`.

See the [density estimation tutorial](../tutorials/05-density.md) for worked
examples and guidance on choosing `k`.

## Sphere

::: wanderwalk.visualization.kde
    options:
      show_root_heading: false
      show_root_toc_entry: false

## Poincare disk

::: wanderwalk.visualization.hyperbolic_kde
    options:
      show_root_heading: false
      show_root_toc_entry: false
