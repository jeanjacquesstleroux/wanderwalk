# Project Curriculum: A Guide to Some Topics to Help Follow Along
---

## How to Use This Document

Each section corresponds to one paper/set of notes. For every topic listed, your task is threefold:
1. **Understand it yourself** to the point you can derive the key results from scratch
2. **Write an explanation** that a calculus-fluent freshman can follow, using concrete examples before abstract definitions
3. **Verify your understanding at the checkpoints** so that you can read the notebooks with clear understanding.
---

## Part 1: Curves and Surfaces in $\mathbb{R}^3$

**Goal:** Establish the proper formulations of geometric objects we are working with.

---

### Section 0: Prerequisites -- Linear Algebra

**Inner Products and Projections**
- [] Define the dot product on $\mathbb{R}^n$ as a bilinear, symmetric, positive definite form. State all three properties precisely.
- [] Define the norm induced by the dot product: $|v| = \sqrt{v \cdot v}$
- [] Define the angle between two vectors via $\cos \theta = (u \cdot v)/(|u||v|)$. Derive this from the law of cosines.
- [] State and prove: two vectors are orthogonal iff their dot product is zero
- [] Define orthogonal projection of $u$ onto $v$: $\operatorname{proj}_v(u) = (u \cdot v / v \cdot v)\, v$
- [] Define the component of $u$ orthogonal to $v$: $u_\perp = u - \operatorname{proj}_v(u)$
- [] Key result: Write the projection onto a subspace $W$ with orthonormal basis $\{e_1, \ldots, e_k\}$: $P_W(u) = \sum (u \cdot e_i) e_i$. Derive $P_{W^\perp}(u) = u - P_W(u)$. This is the formula $P_x v = v - (v \cdot x)x$ used in BM projection when $x$ is the unit normal.
- [] Define orthogonal complement $W^\perp$ and prove $\mathbb{R}^n = W \oplus W^\perp$

**Matrices as Linear Maps**
- [] State: every linear map $T: \mathbb{R}^n \to \mathbb{R}^m$ has a matrix representation $[T]$ depending on the choice of basis
- [ ] Define symmetric matrix ($A = A^\top$) and state the spectral theorem: every symmetric matrix has real eigenvalues and an orthonormal basis of eigenvectors
- [ ] Define positive definite matrix: $A$ is positive definite iff $v^\top A v > 0$ for all $v \neq 0$. Equivalently, all eigenvalues are positive.
- [ ] Define a change-of-basis matrix $P$ and how components of a vector transform: if $v = \sum v^i e_i$ in basis $\{e_i\}$ and $\{\tilde{e}_j\}$ is a new basis, how do the components $v^i$ change? (Contravariant transformation rule)
- [ ] State how matrix representations of linear maps change under change of basis: $[T]_{\text{new}} = P^{-1} [T]_{\text{old}} P$. This is why eigenvalues are basis-independent.

**Quadratic Forms**
- [ ] Define a quadratic form $Q(v) = v^\top A v$ for symmetric $A$
- [ ] Note: the first fundamental form (metric tensor) will be a quadratic form -- it assigns a positive number to every tangent vector, measuring its squared length

---

### Section 1: Prerequisites -- Multivariable Calculus

**Partial Derivatives and the Jacobian**
- [ ] Define partial derivative $\partial f/\partial x_i$ as the directional derivative along the standard basis vector $e_i$
- [ ] Define the gradient $\nabla f = (\partial f/\partial x_1, \ldots, \partial f/\partial x_n)$ as the vector of all partial derivatives
- [ ] Define the directional derivative $D_v f = \lim_{t \to 0} [f(x + tv) - f(x)]/t$. Prove $D_v f = \nabla f \cdot v$ when $f$ is differentiable. This is the chain rule in disguise.
- [ ] Define the Jacobian matrix $Df|_x \in \mathbb{R}^{m \times n}$ for a map $f: \mathbb{R}^n \to \mathbb{R}^m$ as the matrix of all partial derivatives $[Df]_{ij} = \partial f_i/\partial x_j$. $Df|_x$ is the best linear approximation to $f$ near $x$.
- [ ] State the chain rule for compositions: if $h = f \circ g$, then $Dh|_x = Df|_{g(x)} \cdot$

**Change of Variables in Integrals**
- [ ] State the substitution formula for a change of variables $\varphi: U \subset \mathbb{R}^2 \to V \subset \mathbb{R}^2$: $\iint_V f(x,y)\, dx\, dy = \iint_U f(\varphi(u,v)) |\det D\varphi(u,v)|\, du\, dv$
- [ ] Compute this explicitly for polar coordinates: $\varphi(r,\theta) = (r \cos \theta, r \sin \theta)$. Show $|\det D\varphi| = r$. Verify the formula for the area of a disk.
- [ ] **Key note for later**: the area element on a surface will look like $|\varphi_u \times \varphi_v|\, du\, dv$, a generalization of this determinant formula.

**Second Derivatives**
- [ ] Define the Hessian $Hf$ as the matrix of second partial derivatives: $[Hf]_{ij} = \partial^2 f/\partial x_i \partial x_j$
- [ ] State Clairaut's theorem: mixed partials commute if $f$ is $C^2$, i.e., $\partial^2 f/\partial x_i \partial x_j = \partial^2 f/\partial x_j \partial x_i$, so $Hf$ is symmetric
- [ ] Write the second-order Taylor expansion: $f(x+h) \approx f(x) + \nabla f \cdot h + \tfrac{1}{2} h^\top Hf\, h + O(|h|^3)$
- [ ] Define the Laplacian $\Delta f = \nabla^2 f = \sum_i \partial^2 f/\partial x_i^2 = \operatorname{trace}(Hf)$. Compute $\Delta f$ for $f(x,y) = x^2 + y^2$, $f(x,y,z) = 1/|x|$.

---

### Section 2: Parametric Curves in $\mathbb{R}^3$

**Parametrization and Velocity**
- [ ] Define a parametric curve $\gamma: I \subset \mathbb{R} \to \mathbb{R}^3$ as a smooth map. The image $\gamma(I) \subset \mathbb{R}^3$ is the curve.
- [ ] Define the velocity vector $\gamma'(t) = d\gamma/dt$. Interpret geometrically as the tangent direction to the curve at $\gamma(t)$. Its magnitude $|\gamma'(t)|$ is the speed.
- [ ] Define a regular curve: $\gamma'(t) \neq 0$ for all $t$. Explain why this is needed (without it, the parametrization can have cusps or the tangent direction is undefined).
- [ ] Define arc length: $L(\gamma) = \int_a^b |\gamma'(t)|\, dt$. Show this is independent of reparametrization (compute for $\gamma(t)$ and $\gamma(\varphi(s))$ where $\varphi$ is a reparametrization).
- [ ] Define arc-length parametrization (unit speed): $|\gamma'(t)| = 1$ for all $t$. Show every regular curve can be reparametrized by arc length.

**Curvature of a Curve**
- [ ] Define the unit tangent vector $T(t) = \gamma'(t)/|\gamma'(t)|$
- [ ] Define curvature $\kappa = |dT/ds|$ where $s$ is arc length. Interpret as how fast the tangent direction turns per unit length traveled
- [ ] Compute curvature for a circle of radius $R$: show $\kappa = 1/R$ (larger circle $\to$ smaller curvature $\to$ "flatter"). This is the prototype intuition for surface curvature.
- [ ] Define the principal normal vector $N = (dT/ds)/\kappa$. It points toward the center of curvature.
- [ ] State the Frenet-Serret formula: $dT/ds = \kappa N$. This is a preview of the covariant derivative.
- [ ] **Key note for later**: The curvature of the surface will constrain how Brownian paths can behave. On $S^2$, each geodesic corresponds to a great circle with the same curvature as a circle of radius $R$.

---

### Section 3: Regular Surfaces in $\mathbb{R}^3$

**Parametrized Surfaces**
- [ ] Define a parametrized surface chart (less formally): $\varphi: U \subset \mathbb{R}^2 \to \mathbb{R}^3$, a smooth map.
- [ ] Define the partial derivatives (tangent vectors): $\varphi_u = \partial\varphi/\partial u$, $\varphi_v = \partial\varphi/\partial v$. These are vectors in $\mathbb{R}^3$.
- [ ] Interpret $\varphi_u$ and $\varphi_v$: they span the tangent plane at $\varphi(u,v)$.
- [ ] Define a regular point: a point where $\varphi_u \times \varphi_v \neq 0$. The cross product being nonzero means the tangent vectors are linearly independent s.t. the tangent plane is well-defined.
- [ ] Define a regular surface: a surface that can be covered by patches that are all regular everywhere.

**Concrete Computations: Sphere $S^2$**
- [ ] Parametrize $S^2 = \{(x,y,z) \in \mathbb{R}^3 : x^2 + y^2 + z^2 = 1\}$ using spherical coordinates: $\varphi(\theta,\varphi) = (\sin \theta \cos \varphi, \sin \theta \sin \varphi, \cos \theta)$ for $\theta \in (0,\pi)$, $\varphi \in (0,2\pi)$
- [ ] Compute $\varphi_\theta$, $\varphi_\varphi$, and compute $\varphi_\theta \times \varphi_\varphi$. Show the vector product is nonzero for $\theta \in (0,\pi)$ (i.e., away from poles). Conclude $S^2$ is a regular surface.

**Concrete Computations: Torus $T^2$**
- [ ] Parametrize $T^2$ with parameters $(u,v)$, $u \in [0,2\pi)$, $v \in [0,2\pi)$, with $R$ = major radius (distance from z-axis to tube center), $r$ = minor radius (tube radius): $\varphi(u,v) = ((R + r \cos v) \cos u, (R + r \cos v) \sin u, r \sin v)$
- [ ] Compute $\varphi_u$, $\varphi_v$, and compute $\varphi_u \times \varphi_v$. Show the vector product's magnitude is $r(R + r \cos v)$. Oberserve this is not constant. The outer equator ($v=0$) has magnitude $r(R+r)$, the inner equator ($v=\pi$) has magnitude $r(R-r)$.
- [ ] Show $T^2$ is a regular surface (assuming $R > r$).

**The Tangent Plane**
- [ ] Define the tangent plane at a point $p = \varphi(u_0, v_0)$: $T_p S = \operatorname{span}\{\varphi_u(u_0,v_0), \varphi_v(u_0,v_0)\} \subset \mathbb{R}^3$
- [ ] Note: the tangent plane is a 2D linear subspace of $\mathbb{R}^3$ (technically an affine subspace of $\mathbb{R}^3$, centered at $p$)
- [ ] Define the unit normal $N = (\varphi_u \times \varphi_v)/|\varphi_u \times \varphi_v|$. Show $N$ is perpendicular to both tangent vectors.
- [ ] Define the tangent space $T_p S = \{v \in \mathbb{R}^3 : v \cdot N(p) = 0\}$. This is the set of all vectors tangent to the surface at $p$, and a 2-dimensional subspace of $\mathbb{R}^3$.
- [ ] Note: The projection formula $P_x v = v - (v \cdot N(x)) N(x)$ is exactly the orthogonal projection from $\mathbb{R}^3$ onto $T_x S$. For $S^2$, $N(x) = x$, recovering $P_x v = v - (v \cdot x)x$.

**Checkpoint: Before proceeding, you should be comfortable with these topics**
- [ ] Write the parametrization of $S^2$ and $T^2$. Compute $\varphi_u$, $\varphi_v$ for each.
- [ ] Compute the unit normal $N(x)$ for the sphere at an arbitrary point. Verify $N(x) = x$.
- [ ] Write the projection formula $T_x S^2 \to T_x S^2$ and explain what it does geometrically.
- [ ] Why is the tangent plane only defined at regular points?

---

## Part 2: The First Fundamental Form -- Measuring Geometry on a Surface

**Goal:** Understand how to measure lengths, angles, and areas intrinsically on a surface.

---

### Section 4: The First Fundamental Form

**Definition and Motivation**
- [ ] Motivate: on a surface, how do we measure the length of a curve $\gamma(t) = \varphi(u(t), v(t))$? Compute $\gamma'(t) = \varphi_u u' + \varphi_v v'$. Then $|\gamma'|^2 = (\varphi_u u' + \varphi_v v') \cdot (\varphi_u u' + \varphi_v v') = (\varphi_u \cdot \varphi_u)(u')^2 + 2(\varphi_u \cdot \varphi_v) u'v' + (\varphi_v \cdot \varphi_v)(v')^2$
- [ ] Define the coefficients of the first fundamental form: $E = \varphi_u \cdot \varphi_u$, $F = \varphi_u \cdot \varphi_v$, $G = \varphi_v \cdot \varphi_v$
- [ ] Write the metric tensor as a $2 \times 2$ matrix: $g = [[E, F], [F, G]]$. Conclude $g$ is symmetric and positive definite since the surface is regular.
- [ ] Rewrite arc length: $L = \int \sqrt{E u'^2 + 2F u'v' + G v'^2}\, dt$. This is the arc length formula in terms of surface parameters.
- [ ] Define the area element: $dA = |\varphi_u \times \varphi_v|\, du\, dv = \sqrt{EG - F^2}\, du\, dv$. (Derive this: $|\varphi_u \times \varphi_v|^2 = |\varphi_u|^2|\varphi_v|^2 - (\varphi_u \cdot \varphi_v)^2 = EG - F^2$.)
- [ ] **Key note for later**: all of these measurements -- length, angle, area -- depend only on the functions $E, F, G$, not on the ambient $\mathbb{R}^3$.

**Concrete Computations: $S^2$**
- [ ] With spherical parametrization $\varphi(\theta,\varphi)$: compute $E, F, G$
  - $E = \varphi_\theta \cdot \varphi_\theta = 1$
  - $F = \varphi_\theta \cdot \varphi_\varphi = 0$
  - $G = \varphi_\varphi \cdot \varphi_\varphi = \sin^2\theta$
- [ ] Write the metric: $ds^2 = d\theta^2 + \sin^2\theta\, d\varphi^2$. This is the standard round metric on $S^2$.
- [ ] Compute the area element: $dA = \sin \theta\, d\theta\, d\varphi$. Verify: $\iint dA = 4\pi$ (total area of unit sphere).
- [ ] Compute arc length of a great circle: parametrize as $\theta \mapsto (\theta, 0)$, length $= \int_0^\pi d\theta = \pi$. Correct.

**Concrete Computations: $T^2$**
- [ ] With torus parametrization $\varphi(u,v)$: compute $E, F, G$
  - $E = \varphi_u \cdot \varphi_u = (R + r \cos v)^2$
  - $F = \varphi_u \cdot \varphi_v = 0$
  - $G = \varphi_v \cdot \varphi_v = r^2$
- [ ] Write the metric: $ds^2 = (R + r \cos v)^2 du^2 + r^2 dv^2$
- [ ] Compute the area element: $dA = r(R + r \cos v)\, du\, dv$. This is the same expression that appears in the invariant measure calculation.
- [ ] Compute the total area of $T^2$: $\int_0^{2\pi}\int_0^{2\pi} r(R + r \cos v)\, du\, dv = 4\pi^2 Rr$

**The Metric Tensor in Index Notation**
- [ ] Introduce Einstein summation convention: repeated upper and lower indices are summed. Write $g_{ij}$ for the metric tensor components ($i,j \in \{1,2\}$).
- [ ] Define the inverse metric $g^{ij}$: the matrix inverse of $g_{ij}$. For the diagonal cases ($F=0$): $g^{uu} = 1/E$, $g^{vv} = 1/G$.
- [ ] State: the metric $g_{ij}$ allows us to lower indices (convert vectors to covectors). The inverse $g^{ij}$ raises indices. This will be needed for the Laplace-Beltrami formula.
- [ ] **Why this notation matters**: the Laplace-Beltrami operator is written $\Delta_g f = (1/\sqrt{|g|}) \partial_i(\sqrt{|g|}\, g^{ij} \partial_j f)$.

**Isometries**
- [ ] Define an isometry between surfaces $S$ and $\tilde{S}$: a diffeomorphism $f: S \to \tilde{S}$ that preserves the first fundamental form (lengths and angles).
- [ ] State: the flat torus $\mathbb{R}^2/\mathbb{Z}^2$ is isometric to itself, but NOT isometric to the embedded torus $T^2$ in $\mathbb{R}^3$. They have the same topology but different geometries. 
- [ ] Concrete example: show that unrolling a cylinder onto a flat strip is an isometry (the metric on the cylinder is $ds^2 = dz^2 + d\theta^2$, same as the flat metric in Cartesian coordinates after unrolling). The cylinder and the plane are locally isometric but globally different.

---

### Section 5: The Second Fundamental Form and Curvature

The first fundamental form measures intrinsic geometry (lengths, angles). But how "curved" is the surface? A cylinder has $E=G=1$, $F=0$ just like the plane -- they are locally isometric -- yet a cylinder is clearly curved in $\mathbb{R}^3$. The second fundamental form captures this extrinsic curvature.
- [ ] Define the second derivatives of $\varphi$: $\varphi_{uu}, \varphi_{uv}, \varphi_{vv}$ (compute these for practice on $S^2$ and $T^2$)
- [ ] Note: $\varphi_{uu}$ is not necessarily tangent to the surface. Decompose it: $\varphi_{uu}$ = (tangential component) + (normal component). The normal component is $LN$ where $L = \varphi_{uu} \cdot N$.
- [ ] Define the coefficients of the second fundamental form: $L = \varphi_{uu} \cdot N$, $M = \varphi_{uv} \cdot N$, $N_{\text{coeff}} = \varphi_{vv} \cdot N$ (note: overloaded notation -- use e, f, g or L, M, N carefully in your notes)
- [ ] Write the second fundamental form matrix: $II = [[L, M], [M, N_{\text{coeff}}]]$

**Principal Curvatures**
- [ ] Define the shape operator (Weingarten map) $W: T_pS \to T_pS$ by $W = g^{-1} \cdot II$ (matrix product of inverse metric with second fundamental form). It measures how the normal $N$ changes as you move along the surface.
- [ ] Define principal curvatures $k_1, k_2$: the eigenvalues of $W$. The corresponding eigenvectors are the principal directions.
- [ ] Define Gaussian curvature $K = k_1 k_2 = \det(II)/\det(g)$. This is the product of the two principal curvatures.
- [ ] Define mean curvature $H = (k_1 + k_2)/2 = \operatorname{trace}(W)/2$. This is the average of the two principal curvatures.

**Concrete Computations: $S^2$**
- [ ] Compute $II$ for $S^2$: show $L = 1$, $M = 0$, $N_{\text{coeff}} = \sin^2\theta$ (using the computed normal $N = -\varphi$, the inward normal for the unit sphere)
- [ ] Compute $k_1 = k_2 = 1$. $S^2$ is a sphere with both principal curvatures equal to $1/R$ (for unit sphere, $R=1$).
- [ ] $K = 1$, $H = 1$. $S^2$ has constant positive Gaussian curvature.

**Concrete Computations: $T^2$**
- [ ] Compute $N$ (the unit normal) for the torus: $N(u,v) = (\cos v \cos u, \cos v \sin u, \sin v)$. Show this directly from the cross product calculation.
- [ ] Compute $L$, $M$, $N_{\text{coeff}}$ for the torus
- [ ] Compute the principal curvatures: $k_1 = \cos v / (R + r \cos v)$, $k_2 = 1/r$
- [ ] Compute Gaussian curvature: $K = \cos v / (r(R + r \cos v))$
- [ ] **Key observation**: $K > 0$ when $\cos v > 0$ (outer half of the torus), $K = 0$ on the top/bottom circles ($v = \pi/2, 3\pi/2$), $K < 0$ when $\cos v < 0$ (inner half). The torus has regions of all three signs of curvature. Draw this.
- [ ] Compute mean curvature: $H = (R + 2r \cos v)/(2r(R + r \cos v))$

**Theorema Egregium (Statement Only)**
- [ ] State Gauss's Theorema Egregium: the Gaussian curvature $K$ is an intrinsic invariant -- it can be computed from the first fundamental form alone, without reference to the ambient $\mathbb{R}^3$. This is non-obvious: $K = k_1 k_2$ is defined extrinsically via the shape operator, but Gauss showed it depends only on $g_{ij}$.
- [ ] State the formula (Brioschi formula): $K =$ [expression in $E$, $F$, $G$ and their derivatives -- look this up in Pressley]. You do not need to derive it, but you should state it.
- [ ] Corollary: a flat map of the sphere cannot preserve distances (any map from $S^2$ to $\mathbb{R}^2$ must distort lengths). This is why no world map is perfectly accurate.
- [ ] **Project connection**: Gaussian curvature will appear in the Gauss-Bonnet theorem and influences the spectral theory of the Laplace-Beltrami operator.

**Checkpoint before proceeding**
- [ ] State the first and second fundamental forms for $S^2$ and $T^2$. What do their components measure?
- [ ] State the Gaussian curvature of $S^2$. Explain in words: what does $K=1$ mean geometrically?
- [ ] For the torus, identify the regions of positive, zero, and negative curvature. Draw it.
- [ ] Explain in one sentence why the cylinder and the plane are locally isometric but $S^2$ and the plane are not.

---

## Paper 3: Geodesics and the Covariant Derivative

**Goal:** Understand geodesics (straight paths on a surface) and the covariant derivative (the notion of differentiation on a surface). These two concepts are the geometric foundation of BM on manifolds.

---

### Section 6: Geodesics

On $\mathbb{R}^n$, straight lines minimize length between two points. On a surface, what plays the role of a straight line? Two equivalent answers: (1) curves that locally minimize length, (2) curves whose acceleration is always normal to the surface (no tangential acceleration).
- [ ] Define geodesic via the second characterization: $\gamma$ is a geodesic if $\gamma''(t)$ is perpendicular to $T_{\gamma(t)}S$ at every point, i.e., the tangential component of $\gamma''$ is zero.
- [ ] Derive the geodesic equations in terms of surface parameters $(u(t), v(t))$:
  - $u'' + \Gamma^u_{uu}(u')^2 + 2\Gamma^u_{uv}u'v' + \Gamma^u_{vv}(v')^2 = 0$
  - $v'' + \Gamma^v_{uu}(u')^2 + 2\Gamma^v_{uv}u'v' + \Gamma^v_{vv}(v')^2 = 0$
- [ ] The symbols $\Gamma^k_{ij}$ are called Christoffel symbol. Note here that geodesics depend on the first fundamental form alone.

**Christoffel Symbols**
- [ ] Define the Christoffel symbols of the first kind: $[ij, k] = \tfrac{1}{2}(\partial_i g_{jk} + \partial_j g_{ik} - \partial_k g_{ij})$
- [ ] Define the Christoffel symbols of the second kind: $\Gamma^k_{ij} = g^{kl} [ij, l]$ (raise the last index with the inverse metric)
- [ ] Physical interpretation: $\Gamma^k_{ij}$ measures how much the basis vector $\partial_j$ "tilts" in the $e_k$ direction as you move in the $e_i$ direction. They encode all the information about how the coordinate system curves.
- [ ] Compute Christoffel symbols for $S^2$ (spherical coordinates): 
  - The nonzero ones are $\Gamma^\theta_{\varphi\varphi} = -\sin \theta \cos \theta$ and $\Gamma^\varphi_{\theta\varphi} = \Gamma^\varphi_{\varphi\theta} = \cos \theta / \sin \theta$. Verify this computation step by step
- [ ] Compute Christoffel symbols for $T^2$ (write out all nonzero ones):
  - $\Gamma^u_{uv} = \Gamma^u_{vu} = -r \sin v / (R + r \cos v)$, $\Gamma^v_{uu} = \sin v (R + r \cos v) / r$

**Geodesics on Specific Surfaces**
- [ ] Show that great circles satisfy the geodesic equations. Parametrize a great circle and verify.
- [ ] The geodesics of the embedded torus are complicated. State that they exist (by the existence theorem for ODEs applied to the geodesic equations) but do not have simple closed-form expressions in general.
- [ ] Show that Christoffel symbols vanish in Cartesian coordinates, and the geodesic equations reduce to $u'' = v'' = 0$, so geodesics are straight lines. Verify this is consistent with the definition.

**The Exponential Map**
- [ ] Define $\exp_p: T_pS \to S$ by $\exp_p(v) = \gamma(1)$ where $\gamma$ is the geodesic starting at $p$ with velocity $v$
- [ ] State: $\exp_p$ is defined on a neighborhood of 0 in $T_pS$ and is a local diffeomorphism near 0 (by the inverse function theorem and existence/uniqueness of ODE)
- [ ] Interpret geometrically: $\exp_p(v)$ is the point you reach if you walk in direction $v$ for $|v|$ units of arc length along the geodesic
- [ ] **Key note for later**: The formulation of Euler-Maruyama on a manifold uses the exponential map: $X_{n+1} = \exp_{X_n}(\sqrt{\Delta t} \cdot Z_n)$ where $Z_n$ is a tangent vector at $X_n$. The projection scheme we use is an approximation to this that works well for small $\Delta t$.

---

### Section 7: The Covariant Derivative

If $V(t)$ is a vector field along a curve $\gamma(t)$ on a surface, and we want to differentiate $V$, the naive derivative $V'(t) = dV/dt$ is a vector in $\mathbb{R}^3$ that may point off the surface. We need a notion of derivative that stays tangential.
- [ ] Concrete example: take $\gamma(t)$ to be a meridian on $S^2$ (a great circle at fixed $\varphi$). The tangent field $V(t) = \gamma'(t)$ is always tangent to $S^2$. Compute $V'(t)$ in $\mathbb{R}^3$ -- it points toward the center of the sphere, normal to $S^2$. So $V'(t)$ is not a tangent vector. The "intrinsic" rate of change of $V$ along $\gamma$ is zero ($V$ is a geodesic, so it parallel transports its own tangent vector), but the ambient derivative is nonzero.
- [ ] Define the covariant derivative: $\nabla_{\gamma'(t)} V = (V'(t))_T = V'(t) - (V'(t) \cdot N) N$, the projection of $V'(t)$ onto the tangent plane. This is the tangential component of $V'(t)$.

**Parallel Transport**
- [ ] State that a vector field $V(t)$ along $\gamma(t)$ is parallel if $\nabla_{\gamma'(t)} V = 0$, i.e., the covariant derivative is identically zero along the curve. The vector is "not rotating intrinsically as you move along $\gamma$.
- [ ] An example: transport a tangent vector on $S^2$ along a spherical triangle ($1/8$ of the sphere). When you return to the start, the vector has rotated by $\pi/2$.
- [ ] State parallel transport preserves the inner product between vectors. If $V, W$ are both parallel along $\gamma$, then $d/dt (V \cdot W) = 0$.
- [ ] **Key note for later**: The parallel transport equation in coordinates is $dV^k/dt + \Gamma^k_{ij} (dx^i/dt) V^j = 0$. The Christoffel symbols measure the "correction" needed to keep a vector parallel.

**The Covariant Derivative for Vector Fields**
- [ ] Define the Levi-Civita connection $\nabla_X Y$ for vector fields $X, Y$ on $S$: it is the unique connection that (1) is compatible with the metric (preserves inner products under parallel transport) and (2) is torsion-free ($\nabla_X Y - \nabla_Y X = [X,Y]$). These two conditions uniquely determine all the Christoffel symbols $\Gamma^k_{ij}$.
- [ ] In coordinates, $\nabla_{\partial_i} \partial_j = \sum_k \Gamma^k_{ij} \partial_k$. The Christoffel symbols are exactly the components of the covariant derivative of basis vectors.
- [ ] **Project connection**: The covariant derivative is why BM on a manifold requires the Stratonovich formulation. The Itô formula with ordinary derivatives does not transform correctly under isometries. The Stratonovich formula uses the Levi-Civita connection so it does transform correctly.

**The Riemann Curvature Tensor**
- [ ] Define the Riemann curvature tensor as $R(X,Y)Z = \nabla_X \nabla_Y Z - \nabla_Y \nabla_X Z - \nabla_{[X,Y]} Z$. It measures the failure of covariant derivatives to commute.
- [ ] Note that for surfaces in $\mathbb{R}^3$, $R$ is determined entirely by the Gaussian curvature $K$.
- [ ] Note that on a flat plane, parallel transport around any closed loop returns the vector unchanged ($R=0$). On a curved surface, parallel transport around a loop rotates the vector. The rotation angle equals $K$ times the enclosed area (Gauss-Bonnet). This is why holonomy measures curvature.

**Checkpoint before proceeding**
- [ ] Define the covariant derivative $\nabla_{\gamma'} V$ in words and in formula
- [ ] Explain the parallel transport example on $S^2$ (spherical triangle). Why does the vector rotate?
- [ ] Write the geodesic equation using covariant derivatives: $\nabla_{\gamma'} \gamma' = 0$ (the acceleration is zero intrinsically)
- [ ] What are Christoffel symbols measuring? Write the formula for $\Gamma^k_{ij}$ in terms of the metric.
- [ ] Why does the covariant derivative matter for stochastic processes on manifolds?

---

## Paper 4: Abstract Manifolds, the Laplace-Beltrami Operator

**Goal:** Generalize from surfaces in $\mathbb{R}^3$ to abstract Riemannian manifolds. Define the Laplace-Beltrami operator and compute it explicitly on $S^2$ and $T^2$.

---

### Section 8: Smooth Manifolds

The Poincaré hyperbolic disk $H^2$ is not naturally a surface in $\mathbb{R}^3$ with an induced metric. It is defined abstractly as a set with a Riemannian metric imposed on it. To handle $H^2$, we need a more absract framework. For $S^2$ and $T^2$, this framework should produce the same results as the embedded form -- so mastering the embedded case first is the right approach.

- [ ] Define a topological manifold of dimension $n$: a Hausdorff topological space $M$ such that every point has a neighborhood homeomorphic to $\mathbb{R}^n$
- [ ] Define a chart (more formally) $(U, \varphi)$: an open set $U \subset M$ and a homeomorphism $\varphi: U \to \mathbb{R}^n$. The functions $\varphi$ give local coordinates.
- [ ] Define a smooth atlas: a collection of charts $\{(U_\alpha, \varphi_\alpha)\}$ that cover $M$, such that all transition maps $\varphi_\beta \circ \varphi_\alpha^{-1}$ are smooth
- [ ] Define a smooth manifold: a topological manifold with a smooth atlas
- [ ] Define the tangent space $T_pM$ at $p \in M$: the set of equivalence classes of curves through $p$, where two curves are equivalent if they have the same velocity in local coordinates. This abstracts the tangent plane.
- [ ] State: $T_pM$ is an $n$-dimensional real vector space. The tangent bundle $TM = \cup_p T_pM$ is the collection of all tangent spaces.

**Riemannian Metric**
- [ ] Define a Riemannian metric $g$ as an assignment of an inner product $g_p: T_pM \times T_pM \to \mathbb{R}$ to each tangent space $T_pM$, varying smoothly in $p$
- [ ] State in local coordinates $(x^1, \ldots, x^n)$, $g$ is a smooth matrix-valued function $g_{ij}(x)$ that is symmetric and positive definite at every point
- [ ] Define a Riemannian manifold as a smooth manifold with a Riemannian metric
- [ ] For a surface $S \subset \mathbb{R}^3$ with parametrization $\varphi$, the first fundamental form $g_{ij} = \partial_i\varphi \cdot \partial_j\varphi$ is exactly a Riemannian metric in the abstract sense. The abstract framework recovers everything we have done.

**The Poincaré Disk $H^2$**
- [ ] Define $H^2 = \{(x,y) \in \mathbb{R}^2 : x^2 + y^2 < 1\}$ (the open unit disk) with metric: $g_{ij} = (4/(1-r^2)^2) \delta_{ij}$ where $r^2 = x^2 + y^2$
- [ ] This means $ds^2 = 4(dx^2 + dy^2)/(1-r^2)^2$ -- the metric is the Euclidean metric scaled by a position-dependent conformal factor
- [ ] Note: as $r \to 1$ (approaching the boundary), the conformal factor blows up; distances near the boundary are much larger than they appear in the disk. This is why "equivalent" triangles near the boundary look smaller.
- [ ] Compute the area element: $dA = 4\, dx\, dy / (1-r^2)^2$. Show the total area of $H^2$ is infinite.
- [ ] State the Gaussian curvature of $H^2$: $K = -1$ everywhere. $H^2$ is the unique (up to scaling) simply connected surface of constant negative curvature.
- [ ] **Project connection**: BM on $H^2$ does not converge to a uniform distribution as $H^2$ has infinite volume. Instead, BM paths converge to the boundary circle almost surel.y

---

### Section 9: The Laplace-Beltrami Operator

**Motivation**
On $\mathbb{R}^n$, the Laplacian $\Delta f = \sum \partial^2 f/\partial x_i^2$ generates Brownian motion. If we simulate BM in $\mathbb{R}^n$ and test it with a smooth function $f$, the expected rate of change of $f$ along the path is $\tfrac{1}{2}\Delta f$. We need an analog of this fact for a Riemannian manifold.

**Definition**
- [ ] The gradient in $\mathbb{R}^n$ satisfies $\nabla f \cdot v = D_v f$ (directional derivative). On a manifold, define the Riemannian gradient $\operatorname{grad} f$ as the unique tangent vector satisfying $g(\operatorname{grad} f, v) = df(v)$ for all tangent vectors $v$.
- [ ] In coordinates, $(\operatorname{grad} f)^i = g^{ij} \partial_j f$.=
- [ ] Define the divergence of a vector field $X$: $\operatorname{div} X = (1/\sqrt{|g|}) \partial_i(\sqrt{|g|}\, X^i)$. This is the generalization of $\nabla \cdot X$ that accounts for the metric's volume distortion.
- [ ] Define the Laplace-Beltrami operator as $\Delta_g f = \operatorname{div}(\operatorname{grad} f) = (1/\sqrt{|g|}) \partial_i(\sqrt{|g|}\, g^{ij} \partial_j f)$. Show this reduces to the ordinary Laplacian in Cartesian coordinates on $\mathbb{R}^n$: $g_{ij} = \delta_{ij}$, $\sqrt{|g|} = 1$, so $\Delta_g f = \partial_i(\partial^i f) = \sum \partial^2 f/\partial x_i^2$.

**Concrete Computations: $S^2$**
- [ ] With metric $g_{\theta\theta} = 1$, $g_{\varphi\varphi} = \sin^2\theta$, $F=0$: compute $\sqrt{|g|} = \sin \theta$
- [ ] Compute $\operatorname{grad} f$: $(\operatorname{grad} f)^\theta = \partial f/\partial\theta$, $(\operatorname{grad} f)^\varphi = (1/\sin^2\theta) \partial f/\partial\varphi$
- [ ] Compute $\Delta_{S^2} f = (1/\sin \theta) [\partial/\partial\theta(\sin \theta\, \partial f/\partial\theta) + (1/\sin \theta) \partial^2 f/\partial\varphi^2]$
- [ ] Verify for $f(\theta,\varphi) = \cos \theta$ (which is $z$ restricted to $S^2$), compute $\Delta_{S^2} f = -2\cos \theta = -2f$. Conclude that $f = \cos \theta$ is an eigenfunction of $\Delta_{S^2}$ with eigenvalue $-2 = -l(l+1)$ for $l=1$.
- [ ] State the eigenfunctions of $-\Delta_{S^2}$ are the spherical harmonics $Y^m_l$ with eigenvalues $l(l+1)$. They form a complete orthonormal basis for $L^2(S^2)$. This is the spectral theory of the sphere.

**Concrete Computations: $T^2$**
- [ ] With metric $g_{uu} = (R + r \cos v)^2$, $g_{vv} = r^2$, $F=0$: compute $\sqrt{|g|} = r(R + r \cos v)$
- [ ] Compute $\Delta_{T^2} f = [1/(r(R + r \cos v))] \{ \partial/\partial u[(r/(R + r \cos v)) \partial f/\partial u] + \partial/\partial v[((R + r \cos v)/r) \partial f/\partial v] \}$
- [ ] Simplify for u-direction: since $\partial/\partial u[(1/(R+r \cos v)) \partial f/\partial u] = (1/(R+r \cos v)) \partial^2 f/\partial u^2$
- [ ] Simplify for v-direction: this involves a derivative of $(R + r \cos v)$ which produces a $\sin v$ term
- [ ] Write the full expression. Note it is not separable (the v-coefficient of $\partial^2 f/\partial v^2$ depends on $v$), confirming that the embedded torus does not have a clean eigenfunction decomposition.

**The Invariant Measure Connection**
- [ ] State: the Laplace-Beltrami operator is self-adjoint with respect to the Riemannian volume measure $d\mu_g = \sqrt{|g|}\, du\, dv$. This means $\int f \Delta_g h\, d\mu_g = \int (\Delta_g f) h\, d\mu_g$ for smooth $f, h$.
- [ ] State and derive: the Riemannian volume measure $d\mu_g$ is the invariant measure of BM. That is, if $X_0$ has distribution $d\mu_g$ (normalized), then $X_t$ has the same distribution for all t. This follows from the self-adjointness of $\Delta_g$.
- [ ] **For $T^2$**: $d\mu_g = r(R + r \cos v)\, du\, dv$. This is not uniform. Write out the normalized version: the probability density is $p(u,v) = r(R + r \cos v) / (4\pi^2 Rr) = (R + r \cos v)/(4\pi^2 R)$. **This is the theoretical target distribution your simulation must match.**
- [ ] **For $S^2$**: $d\mu_g = \sin \theta\, d\theta\, d\varphi$. Normalized: $p(\theta,\varphi) = \sin \theta / (4\pi)$. Uniform in $\varphi$, biased toward the equator (where $\sin \theta$ is larger). In Cartesian coordinates this is just uniform on the sphere.

**Checkpoint before proceeding**
- [ ] Write the formula for $\Delta_g f$ from memory. Define every symbol in it.
- [ ] Compute $\Delta_{S^2}(\cos \theta)$ and confirm it equals $-2\cos \theta$
- [ ] What is the invariant measure for BM on the embedded $T^2$? Why is it not uniform in $(u,v)$?
- [ ] State the relationship between $\Delta_g$ and the generator of BM on a manifold

---

## Paper 5: Stochastic Processes on Riemannian Manifolds

**Goal:** Connect everything above to our proposed simulation. Understand why the projection scheme works, why Stratonovich is required, and what "Brownian motion on a manifold" means precisely.

---

### Section 10: Itô vs. Stratonovich -- The Coordinate Problem

**Review of Itô Calculus on $\mathbb{R}^n$**
- [ ] State Itô's formula: for $X_t$ satisfying $dX = b\, dt + \sigma\, dW$ and $f$ smooth: $df(X_t) = \partial f/\partial x_i\, dX^i + \tfrac{1}{2} \sigma\sigma^\top_{ij} \partial^2 f/\partial x_i \partial x_j\, dt$. The second-order term is the Itô correction.
- [ ] State Stratonovich's formula: for the same $X_t$, with $\circ$ denoting Stratonovich integral: $df(X_t) = \partial f/\partial x_i \circ dX^i$. No second-order correction. The chain rule holds in its classical form.
- [ ] State the conversion formula: $X \circ dW = X\, dW + \tfrac{1}{2} d[X, W]_t$ where $[X, W]_t$ is the quadratic covariation. For $\sigma(X_t)$: Stratonovich drift = Itô drift + $\tfrac{1}{2} \sigma(X) \sigma'(X)$.

**Why Itô Fails on Manifolds**
- [ ] State the problem: suppose $X_t \in S$ and we change coordinates $y = \varphi(x)$ (a diffeomorphism). The Itô formula for $y(X_t)$ gives: $dy = D\varphi(X)\, dX + \tfrac{1}{2} \operatorname{trace}(D^2\varphi(X) \sigma\sigma^\top)\, dt$. The second term is NOT intrinsic -- it depends on the coordinate change $\varphi$, not just the geometry of $S$.
- [ ] Consequence: if you write an Itô SDE in one coordinate chart and transform it to another chart, you get a different SDE with extra drift terms. This means Itô SDEs are NOT coordinate-invariant -- two observers using different parametrizations would disagree about what process is running.
- [ ] State: the Stratonovich SDE transforms correctly: $dy = D\varphi(X) \circ dX$, with no extra drift terms. Stratonovich SDEs are coordinate-invariant.
- [ ] **Conclusion**: the intrinsic Brownian motion on a manifold must be defined via a Stratonovich SDE. Any Itô representation will have extra drift terms (the Itô-Stratonovich correction) involving the Christoffel symbols.

**The Itô-Stratonovich Correction on $S^2$**
- [ ] State the Itô form of BM on $S^2$ (unit sphere in $\mathbb{R}^3$): $dX^i = (P_{ij}(X)/1) dW^j - \tfrac{1}{2}(n-1) X^i\, dt$ where $P_{ij}(x) = \delta_{ij} - x_i x_j$ is the projection matrix and $n=3$
- [ ] Interpret: the drift term $-X^i\, dt$ points inward (toward the origin). In the Itô representation, BM on $S^2$ needs a drift to stay on the sphere.
- [ ] The Stratonovich form: $dX^i = P_{ij}(X) \circ dW^j$. No drift term. The projection handles everything.
- [ ] Verify the two are equivalent by computing the Itô correction: for $\sigma_{ij} = P_{ij}(X)$, $\tfrac{1}{2} \sum_j (\partial\sigma_{ij}/\partial x_k) \sigma_{kj} = -X^i$. So Stratonovich = Itô form + drift $-X^i\, dt$. The Itô-to-Stratonovich correction exactly cancels the inward drift.

**Why the Projection Scheme Implements Stratonovich**
- [ ] The Euler-Maruyama scheme for the Stratonovich SDE $dX = \sigma(X) \circ dW$: $X_{n+1} = X_n + \sigma(X_n) \Delta W_n + \tfrac{1}{2} \sum_j (\partial\sigma_{ij}/\partial x_k\, \sigma_{kj})(X_n) \Delta t + O(\Delta t^{3/2})$
- [ ] Understand how projection is used: $\tilde{X}_{n+1} = X_n + \sqrt{\Delta t} \cdot P_{X_n}(Z_n)$, then $X_{n+1} = \tilde{X}_{n+1}/|\tilde{X}_{n+1}|$ (for sphere)
- [ ] Show: to first order in $\Delta t$, $X_{n+1} = X_n + P_{X_n}(\sqrt{\Delta t}\, Z_n) - \tfrac{1}{2} (X_n \cdot (\sqrt{\Delta t}\, Z_n)^2) X_n + O(\Delta t^{3/2})$. The second term contributes an $O(\Delta t)$ drift. Compute its expectation: $E[\tfrac{1}{2} (X_n \cdot \sqrt{\Delta t}\, Z_n)^2 X_n] = \tfrac{1}{2} \Delta t \cdot E[Z^T P_X Z] X_n = \tfrac{1}{2} \Delta t (n-1) X_n\, dt$ where $n-1 = 2$ for $S^2 \subset \mathbb{R}^3$. This is exactly the Itô-Stratonovich correction, so the scheme is consistent with the Stratonovich formulation.
- [ ] **Conclusion to write in notes**: the re-normalization after each step automatically incorporates the Itô correction, so the projection scheme implements Stratonovich EM without any extra drift term needing to be computed explicitly.

---

### Section 11: Brownian Motion on a Manifold

**Definition**
- [ ] Define Brownian motion on a Riemannian manifold $(M, g)$: a continuous stochastic process $X_t$ on $M$ with generator $\tfrac{1}{2}\Delta_g$. Equivalently, for every smooth $f: M \to \mathbb{R}$, $f(X_t) - f(X_0) - \tfrac{1}{2}\int_0^t \Delta_g f(X_s)\, ds$ is a martingale.
- [ ] State (without proof): BM on $M$ can be constructed as the solution to the Stratonovich SDE on $M$ corresponding to choosing $\sigma$ to be the "square root" of the metric $g$. For $S^2$ and $T^2$, the projection scheme implements this.
- [ ] State: BM on $M$ is the diffusion whose transition density $p_t(x, y)$ solves the heat equation $\partial_t p = \tfrac{1}{2}\Delta_g p$ with initial condition $p_0(x, \cdot) = \delta_x$.

**The Heat Kernel**
- [ ] Define the heat kernel $p_t(x, y)$: the fundamental solution to $\partial_t u = \tfrac{1}{2}\Delta_g u$. It is simultaneously (1) the transition density of BM ($P_x(X_t \in dy) = p_t(x,y)\, d\mu_g(y)$), and (2) the Green's function for the heat equation.
- [ ] State properties: $p_t(x,y) > 0$, $\int p_t(x,y)\, d\mu_g(y) = 1$, $p_{s+t}(x,y) = \int p_s(x,z) p_t(z,y)\, d\mu_g(z)$ (Chapman-Kolmogorov)
- [ ] Heat kernel on $S^2$: via spectral expansion. If $\varphi_l$ are eigenfunctions of $\Delta_g$ with eigenvalues $-\lambda_l$: $p_t(x,y) = \sum_l e^{-\lambda_l t/2} \sum_m \varphi_{lm}(x) \varphi_{lm}(y)$. For $S^2$, $\lambda_l = l(l+1)$, eigenfunctions are spherical harmonics $Y^m_l$, and: $p_t(x,y) = \sum_{l=0}^\infty [(2l+1)/(4\pi)] e^{-l(l+1)t/2} P_l(\cos d(x,y))$ where $d(x,y)$ is geodesic distance and $P_l$ is the Legendre polynomial.
- [ ] Verify: as $t \to \infty$, all terms except $l=0$ vanish, leaving $p_\infty(x,y) = 1/(4\pi)$ = uniform density on $S^2$. This is the correct long-time behavior on $S^2$.
- [ ] For $T^2$: the spectral expansion does not simplify cleanly (see Paper 4, Section 9 notes). The long-time limit is $p_\infty(u,v) = (R + r \cos v)/(4\pi^2 R)$, which is the normalized invariant measure.

**Euler-Maruyama Convergence**
- [ ] State the strong convergence theorem for EM: under Lipschitz conditions on $\sigma$ and $b$, the EM scheme converges with strong order $\tfrac{1}{2}$ (i.e., $E[|X_T - \tilde{X}_T|^2] = O(\Delta t)$).
- [ ] State the weak convergence theorem: for smooth test functions $f$, $|E[f(X_T)] - E[f(\tilde{X}_T)]| = O(\Delta t)$. Weak order 1.
- [ ] State: the geometric projection introduces an $O(\Delta t)$ error per step from the constraint manifold (points are pushed slightly off the surface before renormalization). This does not degrade the order of convergence but affects the constant.
- [ ] **Practical implication**: use $\Delta t \leq 0.01$ for $S^2$ and $T^2$ simulations. At $\Delta t = 0.1$, the approximation error is large enough to see visually in the distribution plots.

**Checkpoint**
- [ ] Write the Stratonovich SDE for BM on $S^2$ 
- [ ] Explain why Itô fails on manifolds (coordinate non-invariance argument)
- [ ] Derive the Itô form of BM on $S^2$ and identify the inward drift term
- [ ] Explain why the projection + renormalize scheme implements Stratonovich and not Itô
- [ ] Write the heat kernel formula for $S^2$; identify the eigenvalues, eigenfunctions, and long-time limit
- [ ] State the invariant measures for $S^2$ and embedded $T^2$ and explain where they come from

---