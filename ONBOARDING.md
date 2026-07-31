# Brownian Motion on Manifolds

## Onboarding Document

---

This document serves as a gentle introduction to the project, giving motivation, intuition, and some detailed explainations.

---

## 1. Motivation

In 1827, the botanist Robert Brown looked through a microscope at pollen grains suspended in water and noticed they moved in an erratic manner, for the water molecules were constantly colliding with them from all directions. Each collision was too small and too fast to track, but their collective, random effect produced a visible wandering motion. This phenomenon, now called Brownian motion, became a remarkable development throughout 20th-century mathematics. Albert Einstein used it to estimate the size of atoms, and Norbert Wiener gave it a rigorous mathematical foundation. Today it is the basis of the mathematics behind topics from financial modeling and machine learning to heat flow and the geometry of curved spaces.

The central question this project asks is what happens when the space itself is curved?

If a particle wanders randomly on the surface of a sphere, constrained always to stay on that surface and being unable to leave it, its behavior differs from, say, wandering in a flat plane. The sphere's curvature bends and redirects the motion. On a flat plane, a particle that starts at the origin will, on average, move farther and farther away and never return. On a sphere, there is no notion of "far away" in the same sense. The sphere closes back on itself, and over a long time the particle will spread out and fill the surface uniformly. On the hyperbolic plane, a surface with negative curvature, the particle drifts toward the boundary and essentially doesn't return to where it started.

Brownian motion on curved spaces is the foundation of the mathematics underlying:

- Modern generative AI. Diffusion models, the technology behind image generators, are reverse-time diffusion processes, and understanding why they work requires the same mathematics used to study diffusion on manifolds.

- Geometric analysis. The heat equation on a Riemannian manifold, whose solutions are the probability densities of Brownian motion, encodes information about the manifold's shape. Spectral geometers study the manifold by studying how heat spreads across it.

- Statistical physics. Diffusion processes model how particles, energy, and information propagate through physical systems with complex geometries.

This project is a laboratory for exploring these principles, culminating with interactive visualizations that let you watch the diffusion process unfold in real time.

---

## 2. Background

### Brownian Motion in Flat Space

The simplest version of Brownian motion starts with a random walk. Imagine standing at the origin of a number line. At each step, you flip a coin: heads, you move one unit to the right, and tails means one unit to the left. After many steps, your position is the sum of many independent coin flips. The Central Limit Theorem tells us that this sum, when properly scaled, converges to a Gaussian (bell-curve) distribution. Brownian motion is the continuous-time limit of this process as the step size shrinks to zero and the steps become infinitely frequent.

**Step by step.** Start with the random walk. After $n$ coin flips your position is the sum of the individual steps,

$$
S_n = X_1 + X_2 + \cdots + X_n, \qquad X_i = \begin{cases} +1 & \text{with probability } \tfrac12 \\ -1 & \text{with probability } \tfrac12. \end{cases}
$$

Each flip has mean $\mathbb{E}[X_i] = 0$ and variance $\mathrm{Var}(X_i) = 1$. Since the flips are independent, their variances add:

$$
\mathbb{E}[S_n] = 0, \qquad \mathrm{Var}(S_n) = n.
$$

So the typical distance from the origin after $n$ steps grows like $\sqrt{n}$, not like $n$. That square-root growth is the fingerprint of diffusion. To pass to continuous time, take a step of size $\sqrt{\Delta t}$ every $\Delta t$ units of time, so after time $t$ there have been $n = t / \Delta t$ steps. The variance at time $t$ is then

$$
\mathrm{Var} = n \cdot \big(\sqrt{\Delta t}\big)^2 = \frac{t}{\Delta t} \cdot \Delta t = t,
$$

which stays finite as $\Delta t \to 0$. The Central Limit Theorem turns the sum into a Gaussian, and the limit is Brownian motion $B_t$:

$$
B_0 = 0, \qquad B_t \sim \mathcal{N}(0, t), \qquad B_{t+s} - B_t \sim \mathcal{N}(0, s) \ \text{ independent of the past}.
$$

In $d$ dimensions each coordinate is an independent copy, so the expected squared distance is $\mathbb{E}\big[\lVert B_t \rVert^2\big] = d\,t$.

A few properties of Brownian motion in flat space are worth noting as they guide the intuition later:

- Brownian paths are continuous but they are nowhere differentiable.

- Where the particle goes next depends only on where it is now, not on how it got there.

- (*Connection to the heat equation*) If you release a cloud of particles at a single point and let them all diffuse independently, their probability density at a later time satisfies the heat equation. Brownian motion is, in this sense, a probabilistic model of heat flow.

**In symbols.** Write $p(t, x)$ for the probability density of the particle's position at time $t$. It obeys the heat equation

$$
\frac{\partial p}{\partial t} = \frac{1}{2}\,\Delta p, \qquad \Delta p = \sum_{i=1}^d \frac{\partial^2 p}{\partial x_i^2},
$$

where the factor $\tfrac12$ is the same one that reappears later as "half the Laplace-Beltrami operator." Starting from a point source at the origin, the solution is the Gaussian

$$
p(t, x) = \frac{1}{(2\pi t)^{d/2}} \exp\!\left(-\frac{\lVert x \rVert^2}{2t}\right).
$$

You can check it in one dimension by differentiating. With $p = (2\pi t)^{-1/2} e^{-x^2/(2t)}$,

$$
\frac{\partial p}{\partial t} = p\left(\frac{x^2}{2t^2} - \frac{1}{2t}\right), \qquad \frac{1}{2}\frac{\partial^2 p}{\partial x^2} = p\left(\frac{x^2}{2t^2} - \frac{1}{2t}\right),
$$

and the two sides agree, so the Gaussian really does solve the heat equation. Its variance is $t$, matching $\mathrm{Var}(B_t) = t$ from above.

### What Is a Manifold?

A manifold is a space that looks flat when you zoom in close enough, even if it is globally curved. The surface of the Earth is a typical example. Stand anywhere on the Earth's surface and look at a small patch around you; it looks like a flat plane. But the Earth as a whole is a sphere, and a map of the entire surface cannot be drawn on flat paper without distorting it somewhere, which is exactly why every world map lies to you about something (whether it's area, shape, or distance, some countries appear much smaller/larger than they are!).

The manifolds that appear in this project are:

- The sphere, S². The set of all points in three-dimensional space at distance exactly 1 from the origin. This is merely the surface of a ball, not the entire ball itself. It is a two-dimensional surface embedded in three-dimensional space. Its geometry is positively curved everywhere.

- The torus, T². The surface of a donut shape. Topologically, it's equivalent to a square with opposite edges identified -- wrap the left edge around to meet the right edge, then the top to meet the bottom (try it with a napkin!). Unlike the sphere, the torus has zero average curvature (it is locally flat almost everywhere), however its global topology is still non-trivial.

- The hyperbolic plane, H². A surface of constant negative curvature that cannot be embedded in three-dimensional space without distortion. It is represented in this project using the Poincaré disk, which is a unit disk in the plane where distances near the boundary are much larger than they appear. 

**In symbols.** Each surface is a set of points together with a rule for measuring the length of a small step.

The sphere $S^2$ is the unit sphere in $\mathbb{R}^3$,

$$
S^2 = \{(x, y, z) \in \mathbb{R}^3 : x^2 + y^2 + z^2 = 1\}.
$$

The torus $T^2$ is built from a large radius $R$ and a tube radius $r$, using an angle $u$ around the central axis and an angle $v$ around the tube,

$$
(x, y, z) = \big((R + r\cos v)\cos u,\ (R + r\cos v)\sin u,\ r\sin v\big).
$$

The hyperbolic plane $H^2$ lives in the Poincaré disk. The points are the open unit disk, but the length of a small step $(dx, dy)$ is stretched by a factor that grows near the edge,

$$
D = \{(x, y) : x^2 + y^2 < 1\}, \qquad ds^2 = \frac{4\,(dx^2 + dy^2)}{(1 - x^2 - y^2)^2}.
$$

On the flat plane the squared step length is just $ds^2 = dx^2 + dy^2$. The extra factor here runs off to infinity as $x^2 + y^2 \to 1$, which is why the boundary is infinitely far away even though it looks close.

The tangent space at a point is the set of allowed directions of motion. For the sphere it is every vector at a right angle to the position vector,

$$
T_x S^2 = \{v \in \mathbb{R}^3 : v \cdot x = 0\}.
$$

Despite manifolds' global complexity, every point has a tangent space, or a flat plane that best approximates the surface at that point. The tangent plane to a sphere at any point is an ordinary flat plane touching the sphere at that point. This local flatness is what allows one to use the familiar tools of linear algebra and calculus.

### Brownian Motion on a Manifold

Brownian motion on a manifold is defined to be the continuous random process that, if you zoom in to any small region, looks exactly like flat Brownian motion. More precisely, it is the diffusion process whose generator (aka the operator describing how expected values of smooth

functions evolve over time) is half the Laplace-Beltrami operator of the manifold.

The Laplace-Beltrami operator is the manifold's version of the ordinary Laplacian (the sum of second derivatives). On a flat plane, the Laplacian of a function at a point measures how much the function's value at that point differs from its average over a small disk around the point. The Laplace-Beltrami operator does the same thing, but using the intrinsic geometry of the manifold. On the sphere, this operator has a well-known spectrum -- its eigenfunctions are the spherical harmonics -- and this spectrum encodes information about the sphere in the same way that, say, the frequencies of a drum encode information about the drum's shape.

**In symbols.** On the flat plane the Laplacian is the sum of second derivatives,

$$
\Delta f = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2}.
$$

On a manifold the metric $g$ is the matrix that says how to measure lengths and angles in each coordinate patch. Writing $g^{ij}$ for the inverse of that matrix and $|g|$ for its determinant, the Laplace-Beltrami operator is

$$
\Delta_g f = \frac{1}{\sqrt{|g|}} \sum_{i, j} \frac{\partial}{\partial x^i}\!\left(\sqrt{|g|}\, g^{ij}\, \frac{\partial f}{\partial x^j}\right).
$$

When $g$ is the identity (flat space) the square roots cancel and this collapses back to the plain $\Delta$ above. Brownian motion on the manifold is the diffusion whose generator is $\tfrac12 \Delta_g$, so its density solves the matching heat equation

$$
\frac{\partial p}{\partial t} = \frac{1}{2}\,\Delta_g\, p.
$$

The heat kernel, written p(t, x, y), describes the probability density of finding a Brownian particle at location y at time t, given that it started at location x at time zero. It satisfies the heat equation with respect to the Laplace-Beltrami operator in both the x and y variables. On a flat plane, the heat kernel is the Gaussian distribution with variance t. On the sphere, it is an infinite series involving spherical harmonics, but its qualitative behavior is easy to describe: at short times, it models the flat Gaussian, while at long times, it spreads out and converges to the uniform distribution on the sphere (meaning the particle is equally likely to be anywhere).

**In symbols.** The heat kernel is the solution that starts as a point source,

$$
\frac{\partial}{\partial t} p(t, x, y) = \frac{1}{2}\Delta_{g, y}\, p(t, x, y), \qquad p(0, x, y) = \delta_x(y),
$$

and it can always be written as a sum over the eigenfunctions $\phi_k$ of the Laplace-Beltrami operator (the manifold's analogue of the pure tones of a drum), which satisfy $-\Delta_g \phi_k = \lambda_k \phi_k$ with $0 = \lambda_0 \le \lambda_1 \le \lambda_2 \le \cdots$,

$$
p(t, x, y) = \sum_k e^{-\lambda_k t / 2}\, \phi_k(x)\, \phi_k(y).
$$

The $\lambda_0 = 0$ term has a constant eigenfunction and is exactly the uniform distribution the sphere and torus settle into. Every other term decays like $e^{-\lambda_k t / 2}$, so the slowest approach to uniform is set by the smallest nonzero eigenvalue $\lambda_1$.

### Stochastic Differential Equations on Manifolds

A stochastic differential equation (SDE) describes how a random process evolves over infinitesimally small time steps. In flat space, Brownian motion satisfies the simplest possible SDE, meaning the change in position over a small time interval is a small Gaussian random variable. On a manifold, we need to specify that each small random step lives in the tangent space at the current point. The particle can only move along the surface, not through it or away from it.

**In symbols.** In flat space Brownian motion solves the simplest SDE,

$$
dX_t = dW_t,
$$

which just says the change over a small time step has variance $dt$ in each coordinate. A general diffusion written in coordinates has a drift part $b$ and a noise part $\sigma$,

$$
dX^i_t = b^i(X_t)\, dt + \sum_k \sigma^i_{\ k}(X_t)\, dW^k_t.
$$

For this to be Brownian motion on the manifold (generator $\tfrac12 \Delta_g$), the noise has to reproduce the inverse metric, and the drift is then fixed by the geometry,

$$
\sigma \sigma^\top = g^{-1}, \qquad b^i = \frac{1}{2\sqrt{|g|}} \sum_j \frac{\partial}{\partial x^j}\!\left(\sqrt{|g|}\, g^{ij}\right).
$$

The first equation says a random tangent step must be stretched to match the manifold's own way of measuring length. The second says the drift is not a free choice: it is whatever the geometry forces it to be.

Stochastic integrals can be defined in two ways, the Itô convention and the Stratonovich convention. In flat space the difference is minor. On a manifold, though, the Itô convention produces correction terms (called Itô-Stratonovich corrections) dependent on how you specify local coordinates. This means that an Itô SDE written in one coordinate system looks different from the same process written in another coordinate system, which can be a problem if you want to define something that lives on the manifold instead of a coordinate chart. The Stratonovich convention transforms calculus under coordinate changes and thus defines a coordinate-free object. For this reason, Brownian motion on a Riemannian manifold is most naturally expressed as a Stratonovich SDE and hence is the formulation used in this project.

**In symbols.** The two conventions differ by a correction term. Writing $\sigma \circ dW$ for the Stratonovich integral and $\sigma\, dW$ for the Itô integral,

$$
\sigma^i_{\ k}(X) \circ dW^k = \sigma^i_{\ k}(X)\, dW^k + \frac{1}{2} \sum_{j, k} \sigma^j_{\ k}\, \frac{\partial \sigma^i_{\ k}}{\partial x^j}\, dt.
$$

The extra $dt$ piece is the Itô-Stratonovich correction. It is built from the coordinates, which is why the Itô form of one and the same process looks different in different charts, while the Stratonovich form obeys the ordinary chain rule and reads the same in every chart. The full worked example of this correction for the Poincaré disk is in `docs/writeups/2-poincare-disk-derivation.md`.

### The Projection Method

We use a technique called the projection method. The idea has three steps:

1. Propose a step. Generate a small random vector in the ambient space (ordinary three-dimensional Euclidean space) that lies in the tangent plane at the current point. For the sphere, this means generating a random (Gaussian) vector and subtracting its component in the radial direction, leaving only the component tangent to the surface.

2. Take the step. Add the tangent vector scaled by the square root of the time step to the current position. This is the Euler-Maruyama update (the discrete-time approximation to the SDE).

3. Project back to the surface. The resulting point will not lie exactly on the manifold (it will be slightly off the surface due to curvature). Project it back. For the sphere, this is normalization: divide the new point by its Euclidean norm. For the torus, this is finding the nearest point on the torus surface.

The error introduced in step 3 is the distance we had to travel to return to the surface. It is proportional to the square of the step size. Since we are taking steps of size proportional to the square root of the time increment, this error is proportional to the time increment itself, which is the same order of error as the Euler-Maruyama approximation. 

**Step by step.** Write $\Delta t$ for the time step, $Z \sim \mathcal{N}(0, I)$ for a standard Gaussian vector in the ambient space, $P_x$ for the projection onto the tangent space at $x$, and $\Pi_M$ for the projection back onto the surface. One Euler-Maruyama step is

$$
X_{n+1} = \Pi_M\!\big(X_n + \sqrt{\Delta t}\; P_{X_n} Z\big).
$$

For the unit sphere both projections are explicit. The tangent projection removes the radial part,

$$
P_x v = v - (v \cdot x)\, x,
$$

and the projection back to the surface is just normalization,

$$
\Pi_{S^2}(x) = \frac{x}{\lVert x \rVert}.
$$

Here is why the step-3 error has the same size as $\Delta t$. Suppose $x$ sits on the unit sphere and we move by a tangent vector of length $\epsilon$, that is $x \mapsto x + \epsilon u$ with $u$ a unit tangent vector, so $u \cdot x = 0$. The new length is

$$
\lVert x + \epsilon u \rVert = \sqrt{\lVert x \rVert^2 + \epsilon^2} = \sqrt{1 + \epsilon^2} \approx 1 + \frac{\epsilon^2}{2}.
$$

So the point lands a distance of about $\epsilon^2 / 2$ outside the sphere, and that is how far step 3 has to pull it back. Our steps have length $\epsilon \approx \sqrt{\Delta t}$, so the correction is about

$$
\frac{\epsilon^2}{2} = \frac{\Delta t}{2},
$$

the same order as the Euler-Maruyama error itself. Shrinking $\Delta t$ shrinks both together.

### The Heat Kernel

A particularly compelling visualization in this project comes from empirically estimating the heat kernel. The procedure is the following: fix a starting point x on the manifold (say, the north pole of the sphere). Run a large number of independent simulated paths all starting at x. At several fixed times t, record the positions of all particles. Estimate the probability density of those positions using kernel density estimation. This empirical density is an approximation to the heat kernel p(t, x, ·). The visualization shows the density spreading from the starting point, thinning as it expands, and eventually reflecting off the "back" of the sphere and filling it uniformly. On the torus, the density wraps around the edges and interferes with itself. On the hyperbolic plane, it spreads and concentrates toward the boundary without ever returning. 

**In symbols.** With $N$ simulated particles ending at positions $y_1, \dots, y_N$, the kernel density estimate of the heat kernel at a point $y$ is an average of bumps centered at each particle,

$$
\hat{p}(t, x, y) = \frac{1}{N} \sum_{i=1}^N K_h\big(d(y, y_i)\big),
$$

where $d(\cdot, \cdot)$ is distance measured along the surface and $K_h$ is a bump of width $h$, for example a Gaussian $K_h(s) \propto e^{-s^2 / (2h^2)}$. As $N$ grows and $h$ shrinks, $\hat{p}$ approaches the true heat kernel $p(t, x, \cdot)$.

---

## 4. The Three Surfaces in Detail

### The Sphere

The sphere is the natural first surface because its geometry is familiar and its curvature is

uniform; every point on the sphere looks like every other point. The behavior of Brownian motion on the sphere is well-understood theoretically: it is recurrent (the particle returns arbitrarily close to its starting point infinitely often), and the heat kernel converges to the uniform distribution at a rate governed by the first nontrivial eigenvalue of the Laplace-Beltrami operator.

The sphere also provides the clearest opportunity for validation: the exact heat kernel on the

sphere is known, expressed as a series involving Legendre polynomials. Comparing the empirical

density from simulation to the exact formula at several times gives a concrete accuracy check.

**In symbols.** The exact heat kernel on the unit sphere is a series in Legendre polynomials $P_\ell$, evaluated at the dot product $x \cdot y$ (which records the angle between the start $x$ and the point $y$),

$$
p(t, x, y) = \sum_{\ell = 0}^{\infty} \frac{2\ell + 1}{4\pi}\, e^{-\ell(\ell + 1)\, t / 2}\, P_\ell(x \cdot y).
$$

The eigenvalues of the Laplace-Beltrami operator are $\lambda_\ell = \ell(\ell + 1)$, so $\lambda_0 = 0,\ \lambda_1 = 2,\ \lambda_2 = 6, \dots$. The $\ell = 0$ term is the constant $\tfrac{1}{4\pi}$, the uniform density on the sphere (whose surface area is $4\pi$). Every later term decays in time, and the slowest is $\ell = 1$, fading like $e^{-\lambda_1 t / 2} = e^{-t}$. That single number, the first nonzero eigenvalue, sets how fast the particle cloud becomes uniform.

### The Torus

The torus introduces a new geometric feature: it is flat (its Gaussian curvature is zero almost

everywhere), but its global topology is non-trivial. Brownian motion on a flat torus behaves

locally exactly like Brownian motion on a flat plane -- but the torus wraps around, so the

particle cannot escape. The invariant distribution is again uniform. The heat kernel on the

torus has a particularly elegant form -- it is a sum of flat Gaussians placed at the images of

the starting point under the torus's translation symmetry -- which connects the simulation

directly to the theory of theta functions and Fourier analysis on groups.

**In symbols.** It helps to keep apart two related objects that both go by "the torus."

The donut surface sitting in $\mathbb{R}^3$ (the one the simulator actually steps on) has a Gaussian curvature that changes around the tube,

$$
K(u, v) = \frac{\cos v}{r\,(R + r\cos v)}.
$$

It is positive on the outer rim ($v = 0$), negative on the inner rim ($v = \pi$), and exactly zero along the top and bottom circles ($v = \pm\tfrac{\pi}{2}$). Added up over the whole surface it comes to zero,

$$
\int_{T^2} K \, dA = 2\pi\, \chi(T^2) = 0,
$$

by the Gauss-Bonnet theorem, since the torus has Euler characteristic $\chi = 0$. This vanishing total is the sense in which the curvature averages out.

The idealized flat torus is the square $[0, 1] \times [0, 1]$ with opposite edges glued, and its curvature is exactly zero everywhere. Its heat kernel is a sum of flat Gaussians placed at every whole-number shift of the starting point (the method of images), which is where the link to theta functions comes from,

$$
p(t, x, y) = \sum_{n \in \mathbb{Z}^2} \frac{1}{2\pi t}\, \exp\!\left(-\frac{\lVert x - y - n \rVert^2}{2t}\right).
$$

Each term is a copy of the particle reentering from the opposite edge.

The torus is also computationally instructive because periodic boundary conditions are a staple technique in physics simulations. Implementing them correctly requires careful modular arithmetic.

### The Hyperbolic Plane (Our Stretch Goal)

The hyperbolic plane is the most striking surface in the project. Its constant

negative curvature has a counterintuitive consequence: there is so much room in the hyperbolic plane that a random walker is transient. The particle drifts to infinity and never returns.

In the Poincaré disk representation, where the entire infinite hyperbolic plane is mapped to the interior of a unit disk, this means the particle's path converges to a point on the boundary circle, chosen at random. This boundary behavior is called the Poisson boundary of the hyperbolic plane.

Unlike the sphere and torus, where the particle cloud eventually fills the space uniformly, the cloud on the hyperbolic plane concentrates toward the boundary circle and never equilibrates.

**In symbols.** In the Poincaré disk the distance from the center out to Euclidean radius $r$ (with $0 \le r < 1$) is not $r$ but

$$
\rho = 2\,\operatorname{artanh}(r) = \ln\!\left(\frac{1 + r}{1 - r}\right),
$$

which runs off to infinity as $r \to 1$. That is why the boundary circle is infinitely far away and the walker never reaches it in finite time. The radial part of the motion follows a one-dimensional equation,

$$
d\rho_t = d\beta_t + \frac{1}{2}\coth(\rho_t)\, dt,
$$

where $\beta_t$ is an ordinary one-dimensional Brownian motion. For large $\rho$ the factor $\coth(\rho_t)$ is close to $1$, so on average $\rho_t$ grows like $t / 2$. A positive average growth that never turns around is exactly what transience means: the distance from the start keeps increasing. This equation is derived in full, from this project's conventions, in `docs/writeups/2-poincare-disk-derivation.md`.

---

## 5. Implementation Strategy

The project is organized as a Python library with a testable structure. The manifold geometry (how points are represented, how tangent vectors are computed, how the projection step works) is separate from the simulation process (which only knows that it needs a "step" and a "project" operation), which is separate from the visualization layer. Thus, adding a new surface requires implementing only the geometry module for that surface, with no changes to the simulator or the visualizer. It also makes the code testable since each module has clear inputs and outputs that can be verified

independently.

### Performance

The inner loop of a stochastic simulation -- stepping thousands of particles forward one time increment at a time -- is intensive if written naively in Python. The solution to this vectorization. Instead of iterating over particles one by one, we represent all particle positions as one NumPy array and perform operations simultaneously. NumPy's array operations compile to optimized machine code and can be thousands of times faster than an equivalent Python loop. 

### The App

The Streamlit application provides:

- A surface selector (sphere, torus, or hyperbolic plane).

- A time slider that advances the simulation and re-renders the particle distribution.

- A temperature or diffusivity parameter that controls the step size.

- A starting-point selector for the heat kernel visualization.

- An animated mode that renders the diffusion so the viewer can watch the process occur in real time.

The goal of making an app is to make the mathematics tangible. A viewer who hasn't heard of a Laplace-Beltrami operator can nevertheless gain an accurate intuition for what diffusion on curved space means.

---

## 6. Deliverables

- A Python library with implementations of Brownian motion on the sphere and torus, a vectorized Euler-Maruyama simulator, and an empirical heat kernel estimator, all with full docstrings, unit tests, and a one-command setup.

- Jupyter notebooks exported to HTML for easy viewing without running any code. Each notebook is designed to be readable as a document.

- A Streamlit application with a live animated visualization of the diffusion process unfolding step by step across the selected surface, a heat kernel panel, and interactive controls for all simulation parameters.

- Technical blog posts written accessibly for a reader with one year of college mathematics, with the key visualizations embedded inline. These cover mathematical foundations, the geometry of each surface, the Stratonovich SDE formulation, the projection method with error analysis, the Laplace-Beltrami operator, and the heat kernel. Find the blog posts here [link inserted when done]

- A LinkedIn post, presentation, and demo of the Streamlit application showing the diffusion process in real time. Find Danielle and JJ's links here [link inserted when done]

---

## 7. Broader Significance

The project also positions naturally as a computational foundation for future work. A follow-on project could study diffusion processes with drift (stochastic gradient flows on a manifold), or the spectral geometry of the Laplace-Beltrami operator, or the connection to sampling algorithms in high-dimensional statistics.

### Connection to Machine Learning

A diffusion model (DDPM, score-based generative model) defines a forward process that gradually adds Gaussian noise to data until the data distribution becomes a standard Gaussian, and then learns to reverse this process. The forward process is a stochastic differential equation, specifically an Ornstein-Uhlenbeck process, and the reversal of that process is Anderson's time-reversal theorem for diffusions, a result in stochastic analysis. The score function the neural network learns to approximate is the logarithmic derivative of the heat kernel with respect to the spatial variable. Every concept in this project -- the heat kernel, the generator, the forward SDE -- appears  in the theory of score-based generative models. Understanding the geometry of diffusion processes significantly helps one understand why these models work.

**In symbols.** The forward process that adds noise is an Ornstein-Uhlenbeck SDE,

$$
dX_t = -\theta X_t\, dt + \sigma\, dW_t,
$$

whose drift $-\theta X_t$ pulls toward the origin while the noise $\sigma\, dW_t$ spreads the distribution out, so that after enough time the data has been turned into a standard Gaussian. Anderson's time-reversal theorem says that running this process backward is again a diffusion,

$$
dX_t = \big[-\theta X_t - \sigma^2\, \nabla_x \log p_t(X_t)\big]\, dt + \sigma\, d\bar{W}_t,
$$

where $\bar{W}_t$ is a Brownian motion in reverse time. The only unknown piece is the score,

$$
s_t(x) = \nabla_x \log p_t(x),
$$

the gradient of the log density, which is the same log-derivative of the heat kernel that appears throughout this project. The network is trained to approximate $s_t(x)$, and once it can, running the reverse SDE turns fresh noise back into data.

### Connection to Quantitative Finance

Geometric Brownian motion, the standard model for asset prices in quantitative finance, is the simplest stochastic differential equation in flat space. The mathematical tools developed in this project, including Stratonovich calculus, the diffusion generator, and numerical SDE integration, are just generalized versions of the same tools. A student who has built an SDE simulator on a Riemannian manifold has, implicitly, built and understood the majority of what is needed to work with stochastic volatility models, interest rate models, and the numerical methods used to price exotics.

**Step by step.** Geometric Brownian motion models an asset price $S_t$ with the SDE

$$
dS_t = \mu S_t\, dt + \sigma S_t\, dW_t,
$$

where $\mu$ is the average growth rate and $\sigma$ is the volatility. To solve it, apply Itô's formula to $f(S) = \ln S$. Itô's formula carries an extra second-derivative term that ordinary calculus does not,

$$
d(\ln S_t) = \frac{1}{S_t}\, dS_t - \frac{1}{2}\, \frac{1}{S_t^2}\, (dS_t)^2.
$$

Using $dS_t = \mu S_t\, dt + \sigma S_t\, dW_t$ together with the rule $(dW_t)^2 = dt$ (and dropping $dt^2$ and $dt\, dW_t$, which are smaller),

$$
(dS_t)^2 = \sigma^2 S_t^2\, dt,
$$

so the $S_t$ factors cancel and

$$
d(\ln S_t) = \left(\mu - \frac{1}{2}\sigma^2\right) dt + \sigma\, dW_t.
$$

The right-hand side no longer contains $S_t$, so we integrate from $0$ to $t$ and exponentiate,

$$
S_t = S_0 \exp\!\left(\left(\mu - \tfrac{1}{2}\sigma^2\right) t + \sigma W_t\right).
$$

The extra $-\tfrac12 \sigma^2$ is the same kind of Itô correction seen elsewhere in this project. Here it is what separates the average growth rate from the rate you actually see along a single price path.
