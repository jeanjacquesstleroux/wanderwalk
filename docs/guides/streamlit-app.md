# The interactive app

wanderwalk ships a Streamlit app that runs the same simulators behind a set
of sliders, and animates a single particle wandering across the surface. It
is the fastest way to build intuition for what `dt`, `T`, and the starting
point actually do.

## Installing and launching

The app needs Streamlit and Plotly, which the core install does not include.
They come with the `app` extra:

```bash
pip install "wanderwalk[app]"
```

That installs a console script. Run it from anywhere:

```bash
wanderwalk-app
```

Streamlit opens the app in your browser. Any arguments you pass are forwarded
to `streamlit run`, so this works:

```bash
wanderwalk-app --server.port 8080
```

If the extra is missing, the launcher says so rather than failing with an
import error:

```text
wanderwalk-app needs streamlit and plotly, which the core install does not
include.
Install the app extra with:

    pip install wanderwalk[app]
```

Importing `wanderwalk` never pulls in Streamlit or Plotly. Only running the
app does.

## The sidebar

Choosing a manifold changes which controls appear below it.

Shared by all three surfaces:

| Control | Range | Default |
| --- | --- | --- |
| Number of particles, `N` | 1 to 1000 | 500 |
| Number of steps, `T` | 10 to 5000 | 1000 |
| Time step, `dt` | 0.001 to 0.1 | 0.01 |
| Concentration parameter, `k` | 1 to 100 | 20 |
| Noise type | Isotropic or Anisotropic | Isotropic |

`k` controls the density heatmap only, not the simulation. See
[density estimation](../tutorials/05-density.md#choosing-k) for what it does.

Then, per surface:

=== "Sphere"

    | Control | Range | Default |
    | --- | --- | --- |
    | Starting latitude | -90 to 90 degrees | 0 |
    | Starting longitude | -180 to 180 degrees | 0 |

=== "Torus"

    | Control | Range | Default |
    | --- | --- | --- |
    | Major radius `R` | 1.0 to 10.0 | 3.0 |
    | Minor radius `r` | 0.1 to `R - 0.1` | 1.0 |
    | Starting toroidal angle `u` | 0 to 360 degrees | 0 |
    | Starting poloidal angle `v` | 0 to 360 degrees | 0 |

    The upper bound on `r` tracks `R`, so the tube can never be so fat that
    the torus self-intersects.

=== "Poincare disk"

    | Control | Range | Default |
    | --- | --- | --- |
    | Starting radius | 0.0 to 0.95 | 0.0 |
    | Starting angle | 0 to 360 degrees | 0 |

    The radius stops at 0.95 rather than 1.0, since the boundary circle is
    infinitely far away and not part of the space.

Every control has a `?` button next to it that opens a short explanation,
including the equation the parameter appears in where there is one.

!!! note "Noise type on the Poincare disk"

    The noise type selector is shown for all three surfaces, but the
    hyperbolic simulator has no anisotropic mode, so the setting has no
    effect there. See
    [the hyperbolic tutorial](../tutorials/03-hyperbolic.md) for why.

## What you get back

Before you press anything, the app shows the bare surface with your starting
point marked, so you can position it before committing to a run.

Pressing the Run Simulation button produces three things:

1. An animated trajectory following one particle, the first of the `N`, as it
   wanders across the surface. This is the part worth watching.
2. `Final Particle Distribution`, a scatter of where all `N` particles
   ended up.
3. `Density Heatmap`, the same final positions passed through
   `ww.sphere_kde` or `ww.disk_kde`.

The last two are on tabs beneath the animation.

## Things worth trying

- Set `dt` to its maximum of 0.1 on the Poincare disk and watch the particle
  lurch across the whole disk in a handful of steps. Then drop it to 0.001.
  This is the [step-size convergence
  issue](reproducibility.md#choosing-dt) made visible.
- Pick the sphere with anisotropic noise. The particle is confined to a
  single great circle no matter how long you run it.
- Pick the torus with anisotropic noise and a starting poloidal angle of 90
  degrees. The particle circles the torus while sliding steadily toward the
  outer equator, which is the [geodesic curvature
  drift](../tutorials/02-torus.md#anisotropic-noise-and-the-two-equators).
- Set a torus with `R = 10` and `r = 0.1` and see how much longer the
  particles take to wrap around.

## Running it from source

If you have the repository cloned, the launcher is a thin wrapper around
`streamlit run` and you can call Streamlit yourself:

```bash
streamlit run src/wanderwalk/app/streamlit_app.py
```

That is occasionally useful when editing the app, since it avoids
reinstalling the console script.

## What next

- [Reproducibility and performance](reproducibility.md), for the reasoning
  behind the parameter choices the sliders expose.
- [Getting started](../getting-started.md), to do the same thing in code.
