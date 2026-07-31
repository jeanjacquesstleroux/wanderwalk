# The Poincaré Disk: SDE Derivation
### For: Brownian Motion on Manifolds Project
### Purpose: derive, from this project's own stated conventions, the exact stochastic differential equation governing Brownian motion on $H^2$ in the Poincaré disk model -- so that every formula used in `src/manifolds/hyperbolic.py` traces back to a step here, rather than to a remembered or copied result.

---

## 0. Why this needs its own derivation

Sphere ($S^2$) and Torus ($T^2$) are embedded in $\mathbb{R}^3$. Their Brownian motion is built with the *projection method*: propose an ambient step, add it, project back onto the surface. That method relies on the surface being isometrically embedded so ambient Euclidean lengths of tangent vectors agree with the surface's own metric.

$H^2$ has no isometric embedding in $\mathbb{R}^3$ (Hilbert's theorem), so the projection method does not apply. It must be handled intrinsically: points are $(x, y)$ in the open unit disk $D = \{(x,y) : x^2 + y^2 < 1\}$, carrying its own metric that is *not* the flat Euclidean one. Every formula below is derived directly from that metric and from this project's own stated generator convention (ONBOARDING.md §"Brownian Motion on a Manifold": *"the diffusion process whose generator is half the Laplace-Beltrami operator"*).

---

## 1. The metric

From `docs/writeups/1-curriculum-checklist.md` §"The Poincaré Disk $H^2$":

$$
g_{ij}(x,y) = \lambda(x,y)^2 \delta_{ij}, \qquad \lambda(x,y) = \frac{2}{1-x^2-y^2} = \frac{2}{1-r^2}, \qquad r^2 = x^2+y^2
$$

so $ds^2 = \lambda^2 (dx^2 + dy^2)$. This is a *conformal* metric: at every point it is a positive scalar multiple of the flat Euclidean metric, and that scalar blows up as $r \to 1$. Gaussian curvature is $K = -1$ everywhere.

Because $g_{ij} = \lambda^2\delta_{ij}$ is diagonal, $g^{ij} = \lambda^{-2}\delta^{ij}$ (inverse), and $\det(g) = \lambda^4$, so $\sqrt{|g|} = \lambda^2$.

---

## 2. The Itô SDE has zero drift, a general fact about 2D conformal coordinates

**Setup.** For an Itô SDE $dX^i = b^i(X)\,dt + \sigma^i_{\ k}(X)\,dW^k$ to have generator $L = \tfrac12\Delta_g$ (this project's convention), standard theory for diffusions on Riemannian manifolds requires:

$$
\sigma \sigma^\top = g^{-1} \qquad \text{(matches the second-order/diffusion part)}
$$

$$
b^i = \frac{1}{2\sqrt{|g|}}\, \partial_j\!\left(\sqrt{|g|}\, g^{ij}\right) \qquad \text{(matches the first-order/drift part)}
$$

(This is the same relation used implicitly for $S^2$/$T^2$ -- see `docs/writeups/1-curriculum-checklist.md` §10, where the sphere's Itô form has drift $-X^i\,dt$ because $\sqrt{|g|}\,g^{ij}$ is *not* constant there.)

For our metric, $\sqrt{|g|}\,g^{ij} = \lambda^2 \cdot \lambda^{-2}\delta^{ij} = \delta^{ij}$ -- the Kronecker delta, a genuine constant (not merely constant along some direction; identically 0 or 1 everywhere, for *any* choice of conformal factor $\lambda(x,y)$, not just this one). Its partial derivative is therefore exactly zero:

$$
\partial_j\!\left(\sqrt{|g|}\,g^{ij}\right) = \partial_j\!\left(\delta^{ij}\right) = 0 \quad \text{for all } i \qquad \Longrightarrow \qquad b^i = 0
$$

**In isothermal (conformal) coordinates, the Itô SDE for Brownian motion is always driftless, regardless of the conformal factor.** Planar Brownian motion is conformally invariant up to a time change, mentioned here only as intuition; the computation above is self-contained. Since $\sigma\sigma^\top = g^{-1} = \lambda^{-2} I$, one valid choice of square root is $\sigma = \lambda^{-1} I$ (a scalar multiple of the identity because $\lambda^{-1}I \cdot (\lambda^{-1}I)^\top = \lambda^{-2}I$). With $b = 0$:

$$
dX_t = \lambda(X_t)^{-1}\, dW_t = \frac{1-|X_t|^2}{2}\, dW_t \tag{*}
$$

where $W_t$ is standard 2D Brownian motion. This is the governing Itô SDE for BM on $H^2$ in these coordinates, under this project's $\tfrac12\Delta_g$ convention.

**Itô vs. Stratonovich.** It is often said that Brownian motion has a driftless Stratonovich form, $dX = \sigma(X) \circ dW$ with no separate drift term. That statement holds on the orthonormal frame bundle (the Eells-Elworthy-Malliavin construction), where the horizontal SDE is genuinely driftless and projects down to BM on the manifold. It does *not* carry over to a single coordinate chart with the diagonal choice $\sigma = \lambda^{-1}I$ used here. In these disk coordinates it is the *Itô* form (*) that is driftless, while the equivalent Stratonovich form of the same process has a nonzero drift.

Converting (*) to Stratonovich subtracts $\tfrac12 c$ from the (zero) Itô drift, where

$$
c^i = \sum_{j,k} \sigma^k_{\ j}\, \partial_k \sigma^i_{\ j} = \lambda^{-1}\partial_i \lambda^{-1} = -\frac{1-|x|^2}{2}\, x^i .
$$

This is zero only at the origin, so the Stratonovich drift $b^i_{\text{Strat}} = -\tfrac12 c^i = \tfrac{1-|x|^2}{4}\, x^i$ is nonzero across the rest of the disk. Put differently, writing $dX = \sigma \circ dW$ with no drift term would simulate BM plus a spurious inward drift, not BM.

This does not affect the implementation. The code integrates the Itô form (*) with Euler-Maruyama, and (*) has zero drift, so there is no drift term to add. The contrast with $S^2$ and $T^2$ is that their Itô picture has a nonzero drift, and the projection step in the embedded construction is what produces it; here the Itô drift is zero from the start, so there is nothing for a projection step to produce.

---

## 3. Practical consequence: `sample_tangent_noise`

Equation (*) says, in a sense, draw $Z \sim N(0, I_2)$, scale by $\lambda(x)^{-1} = (1-|x|^2)/2$:

$$
\texttt{sample\_tangent\_noise}(x) = \frac{1-|x|^2}{2} \cdot Z, \qquad Z \sim N(0, I_2)
$$

This is *not* a projection because there is nothing to project away from in intrinsic 2D coordinates. Rather it is a *rescaling* of an isotropic Gaussian. Getting this scaling right is the most important correctness detail in the implementation. Omitting the $(1-|x|^2)/2$ factor simulates the wrong process of flat 2D Brownian motion running inside a disk, instead of hyperbolic Brownian motion.

Euler–Maruyama step, same three-line shape as Sphere/Torus:

```
noise = sample_tangent_noise(x)
x_new = x + sqrt(dt) * noise
x_new = project_to_manifold(x_new) 
```

---

## 4. The radial process

Define $r_t = |X_t|$ and $\rho_t = 2\,\mathrm{artanh}(r_t) = \ln\!\left(\frac{1+r_t}{1-r_t}\right)$. $\rho$ is the standard Poincaré-disk geodesic distance from the origin (the integral $\int_0^r \lambda(s)\,ds = \int_0^r \frac{2}{1-s^2}\,ds = 2\,\mathrm{artanh}(r)$, i.e. it is arc length along a radius measured with the metric from §1). This section derives the SDE for $\rho_t$ directly from (*), via two applications of Itô's lemma.

### Step 1: from $X = (X^1, X^2)$ to $r = |X|$

$r = \sqrt{(X^1)^2 + (X^2)^2}$. Standard partial derivatives:

$$
\frac{\partial r}{\partial x} = \frac{x}{r}, \qquad \frac{\partial r}{\partial y} = \frac{y}{r}
$$

$$
\frac{\partial^2 r}{\partial x^2} = \frac{y^2}{r^3}, \qquad \frac{\partial^2 r}{\partial y^2} = \frac{x^2}{r^3} \qquad \Longrightarrow \qquad \Delta r \ (\text{flat}) = \frac{x^2+y^2}{r^3} = \frac{1}{r}
$$

From (*), $dX^1 = \lambda^{-1}dW^1$, $dX^2 = \lambda^{-1}dW^2$ (independent), so $(dX^1)^2 = (dX^2)^2 = \lambda^{-2}dt$, $dX^1 dX^2 = 0$. Itô's lemma:

$$
dr = \frac{x}{r}dX^1 + \frac{y}{r}dX^2 + \frac{1}{2}\!\left[\frac{y^2}{r^3}+\frac{x^2}{r^3}\right]\lambda^{-2}\,dt = \lambda^{-1}\!\left[\frac{x}{r}dW^1 + \frac{y}{r}dW^2\right] + \frac{1}{2}\lambda^{-2}\frac{1}{r}\,dt
$$

$(x/r, y/r)$ is a unit vector, so $\frac{x}{r}dW^1 + \frac{y}{r}dW^2$ is itself a standard 1D Brownian motion, call it $d\beta_t$ (the radial projection of a 2D Brownian motion is a 1D Brownian motion, or the standard fact used to derive Bessel processes from planar BM). Substituting $\lambda^{-1} = (1-r^2)/2$:

$$
dr = \frac{1-r^2}{2}\, d\beta_t + \frac{(1-r^2)^2}{8r}\, dt \tag{$\dagger$}
$$

### Step 2: from $r$ to $\rho = 2\,\mathrm{artanh}(r) = \ln\!\left(\frac{1+r}{1-r}\right)$

$$
\frac{d\rho}{dr} = \frac{2}{1-r^2} = \lambda(r), \qquad \frac{d^2\rho}{dr^2} = \frac{4r}{(1-r^2)^2}
$$

$(dr)^2 = \left(\frac{1-r^2}{2}\right)^2 dt$ (quadratic variation only sees the diffusion term). Itô's lemma again:

$$
d\rho = \lambda(r)\, dr + \frac{1}{2}\cdot\frac{4r}{(1-r^2)^2}\cdot\frac{(1-r^2)^2}{4}\, dt
$$

Substitute $(\dagger)$ for $dr$:

$$
d\rho = \lambda(r)\cdot\frac{1-r^2}{2}\, d\beta_t + \lambda(r)\cdot\frac{(1-r^2)^2}{8r}\, dt + \frac{r}{2}\, dt
$$

$\lambda(r)\cdot\frac{1-r^2}{2} = 1$ exactly (the diffusion coefficient in $\rho$ is unit -- as it must be, since $\rho$ is an arc-length coordinate). $\lambda(r)\cdot\frac{(1-r^2)^2}{8r} = \frac{1-r^2}{4r}$. So:

$$
d\rho = d\beta_t + \left[\frac{1-r^2}{4r} + \frac{r}{2}\right] dt = d\beta_t + \frac{(1-r^2)+2r^2}{4r}\, dt = d\beta_t + \frac{1+r^2}{4r}\, dt
$$

### Step 3: express the drift in terms of $\rho$

With $r = \tanh(\rho/2)$ (inverting $\rho = 2\,\mathrm{artanh}(r)$), the standard hyperbolic half-angle identity gives:

$$
\coth(\rho) = \frac{1+\tanh^2(\rho/2)}{2\tanh(\rho/2)} = \frac{1+r^2}{2r}
$$

so $\frac{1+r^2}{4r} = \frac{1}{2}\coth(\rho)$. Therefore:

$$
d\rho_t = d\beta_t + \frac{1}{2}\coth(\rho_t)\, dt \tag{**}
$$

This says the radial process is a 1D diffusion with unit diffusion coefficient and drift $\frac12\coth(\rho)$.

---

## 5. Two checks on (**)


**(a) Large-$\rho$ limit.** As $\rho \to \infty$, $\coth(\rho) \to 1$, so $d\rho \approx d\beta_t + \frac12 dt$. This predicts $E[\rho_t] \sim t/2$ for large $t$, hence BM on $H^2$ is transient (as ONBOARDING.md), and (**) reinforces the geodesic distance from the origin grows linearly in $t$, at rate exactly $1/2$ under this project's $\frac12\Delta_g$ convention.

**(b) Small-$\rho$ limit -- must match a Bessel(2) process.** As $\rho \to 0$, $\coth(\rho) \to 1/\rho$, so $d\rho \approx d\beta_t + \frac{1}{2\rho}\, dt$. The radial part of *ordinary flat* $n$-dimensional Brownian motion is a Bessel($n$) process, $d\rho = d\beta + \frac{n-1}{2\rho}\, dt$. For $n = 2$ this is $d\rho = d\beta + \frac{1}{2\rho}\,dt$, matching (**)'s small-$\rho$ limit exactly. Near any point, any smooth 2D Riemannian manifold looks like flat $\mathbb{R}^2$, so its radial BM process must reduce to Bessel(2) near the origin.

---

The true continuous-time process $X_t$ satisfies $|X_t| < 1$ for all finite $t$, almost surely... $\rho_t \to \infty$. A discrete Euler–Maruyama step, however, can overshoot past $|x| = 1$ (where $\lambda$ and hence $(1-|x|^2)^{-1}$ quantities become undefined/negative).

`project_to_manifold` for this manifold therefore does *not* play the same role it plays for Sphere/Torus. If a step produces $|x| \ge 1 - \varepsilon$ for small $\varepsilon$, rescale to $1 - \varepsilon$..

---

## 7. $\coth(\rho)$ vs. $\frac12\coth(\rho)$

Some of our references on hyperbolic Brownian motion state the radial SDE as $d\rho = d\beta + \coth(\rho)\, dt$ (no factor of $\frac12$). This reflects a different but common generator convention ($\Delta_g$ rather than $\frac12\Delta_g$). Repeating §2's construction with generator $L = \Delta_g$ instead of $\frac12\Delta_g$ requires $\sigma\sigma^\top = 2g^{-1}$ and doubles the drift formula too, which propagates through §4 as an overall rescaling that removes the $\frac12$ from (**). Since this project's ONBOARDING.md commits explicitly to generator $\frac12\Delta_g$, equation (**) (with the $\frac12$ term) is more consistent with this codebase.

---

## 8. Secondary validation: the heat kernel (verify before use)

A closed-form heat kernel for $H^2$ (curvature $-1$) is of the general form (McKean):

$$
p(t, \rho) \;\propto\; e^{-t/8} \int_\rho^\infty \frac{b\cdot e^{-b^2/(2t)}}{\sqrt{\cosh b - \cosh \rho}}\, db
$$

This is an analogue of the Legendre-series heat kernel used to validate the Sphere in Notebook-02. It is listed here as a secondary check, because (unlike (**), which is fully re-derived above from this project's own stated conventions) reproducing McKean's formula correctly requires getting an exact normalization constant and a generator-convention time-rescaling ($t \to t/2$, by the same $\frac12\Delta_g$ vs. $\Delta_g$ issue as §7) right.If sourced and verified, it becomes a strong additional checki, otherwise the radial-SDE in §4–5 stands on its own as a self-contained validation measure.

---

## 9. Summary of formulas used in `src/manifolds/hyperbolic.py`

| Quantity | Formula | Source |
|---|---|---|
| Conformal factor | $\lambda(x,y) = \dfrac{2}{1-x^2-y^2}$ | §1 (curriculum doc) |
| Tangent projection | `project_to_tangent(x, v)` $= v$ | intrinsic 2D, no ambient subspace -- see code docstring |
| Tangent noise | `sample_tangent_noise(x)` $= \dfrac{1-\lvert x\rvert^2}{2}\cdot Z$, $Z\sim N(0,I_2)$ | §3, from (*) |
| Manifold "projection" | radial clamp to $1-\varepsilon$ if $\lvert x\rvert \ge 1-\varepsilon$ | §6 -- numerical safeguard only |
| Geodesic distance from origin | $\rho(x) = 2\,\mathrm{artanh}(\lvert x\rvert) = \ln\!\left(\dfrac{1+\lvert x\rvert}{1-\lvert x\rvert}\right)$ | §4 |
| Geodesic distance (general) | $d(z,w) = \mathrm{arccosh}\!\left(1 + \dfrac{2\lvert z-w\rvert^2}{(1-\lvert z\rvert^2)(1-\lvert w\rvert^2)}\right)$ | standard Poincaré-disk formula |
| Radial SDE (validation target) | $d\rho_t = d\beta_t + \dfrac12\coth(\rho_t)\, dt$ | §4, (**) |
