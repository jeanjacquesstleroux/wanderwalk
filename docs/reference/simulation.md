# Simulation

Vectorized Euler-Maruyama simulators. Each advances `N` independent particles
for `T` time steps at once and returns the full trajectory, indexed
`[time, particle, coordinate]`.

All three are re-exported at the top level, so under the conventional alias
they are `ww.sphere_simulator`, `ww.torus_simulator`, and
`ww.hyperbolic_simulator`.

::: wanderwalk.simulation.simulator
    options:
      show_root_heading: false
      show_root_toc_entry: false
