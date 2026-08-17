# Import the base class that contains Manifold abstract methods
from .base import Manifold
import numpy as np

class PoincareDisk(Manifold):
    """The PoincareDisk class represents the hyperbolic plane H^2 using the
    Poincare disk model: the open unit disk {(x, y) : x^2 + y^2 < 1} in R^2,
    equipped with the conformal metric g_ij = lambda(x,y)^2 * delta_ij where
    lambda(x,y) = 2 / (1 - x^2 - y^2).

    Unlike Sphere and Torus, H^2 has no isometric embedding into R^3
    (Hilbert's theorem), so points here are 2D vectors.

    Every formula in this class is derived step by step in
    docs/writeups/2-poincare-disk-derivation.md, starting from this
    project's own stated convention that Brownian motion's generator is
    half the Laplace-Beltrami operator. In particular:

    - The governing Ito SDE for a point X_t in the disk is driftless:
        dX_t = lambda(X_t)^{-1} dW_t = ((1 - |X_t|^2) / 2) dW_t

    - The radial process rho_t = 2*artanh(|X_t|) (the geodesic distance
      from the origin) satisfies dRho_t = dBeta_t + (1/2)*coth(rho_t) dt.
      This closed-form target is the primary check for this manifold 
      since H^2 has no stationary distribution to compare against.
    """

    def __init__(self, epsilon=1e-10):
        """Initializes the Poincare disk.

        Arguments:
            epsilon: How far inside the unit circle a point is clamped to
            if a numerical step pushes it to or past the boundary. 
        """
        self.epsilon = epsilon

    def conformal_factor(self, x):
        '''Computes the conformal factor lambda(x) = 2 / (1 - |x|^2) at a
        point x in the disk. This is the scalar by which the Euclidean
        metric is multiplied to get the hyperbolic metric at x.

        Arguments:
            x: A point in the open unit disk.

        Returns:
            The conformal factor lambda(x) at point x.
        '''
        norm_sq = np.dot(x, x)
        return 2.0 / (1.0 - norm_sq)

    def project_to_tangent(self, x, v):
        '''Returns v unchanged.

        Unlike Sphere and Torus, which are embedded in R^3 and therefore
        need to remove the ambient normal component of a vector to obtain
        a tangent vector, H^2 in the Poincare disk model is intrinsically
        2-dimensional: the tangent space at every interior point x is all
        of R^2, since there is no ambient subspace to restrict to.

        Note this method only ensures v lies in the correct 2D subspace 
        (trivially true here), it does not account for the fact that the 
        tangent space's inner product is non-Euclidean.

        Arguments:
            x: A point in the disk.
            v: A vector in R^2.

        Returns:
            v, unchanged.
        '''
        return v

    def project_to_tangent_multiple(self, X, V):
        '''Vectorized version of project_to_tangent for many points/vectors
        at once. Returns V unchanged, for every tangent space here is all of R^2.

        Arguments:
            X: A set of points in the disk.
            V: A set of vectors in R^2, one per point in X.

        Returns:
            V, unchanged.
        '''
        return V

    def sample_tangent_noise(self, x):
        '''Generates the tangent noise at point x for the
        Euler-Maruyama step, per the Ito SDE derived in
        docs/writeups/2-poincare-disk-derivation.md section 3:

            sample_tangent_noise(x) = ((1 - |x|^2) / 2) * Z,  Z ~ N(0, I_2)

        Since project_to_tangent is the identity here, all
        of the manifold-specific work for turning flat Gaussian noise into
        the correct tangent noise happens in this scaling factor, which is
        exactly lambda(x)^{-1}, the inverse conformal factor.

        Arguments:
            x: A point in the disk.

        Returns:
            A random vector in R^2, scaled for the hyperbolic metric at x.
        '''
        z = np.random.randn(2)
        return z / self.conformal_factor(x)

    def sample_tangent_noise_multiple(self, X):
        '''Vectorized version of sample_tangent_noise for many points at
        once.

        Arguments:
            X: An (N, 2) array of points in the disk.

        Returns:
            An (N, 2) array of random tangent vectors, one per input point.
        '''
        N = X.shape[0]
        Z = np.random.randn(N, 2)
        norms_sq = np.sum(X * X, axis=1, keepdims=True)
        conformal_factors = 2.0 / (1.0 - norms_sq)
        return Z / conformal_factors

    def project_to_manifold(self, x):
        '''Clamps a point x back inside the open unit disk if a numerical
        step has pushed it to or past the boundary.

        The true continuous-time process on H^2 never reaches the
        boundary |x| = 1 in finite time (see
        docs/writeups/2-poincare-disk-derivation.md section 6). It exists
        to prevent floating-point arithmetic from producing an
        undefined or negative (1 - |x|^2), which the conformal factor and
        the noise scaling in sample_tangent_noise both depend on.

        Arguments:
            x: A point in R^2 that may lie at or beyond the unit circle
            due to numerical error.

        Returns:
            x, unchanged if |x| < 1 - epsilon; otherwise x rescaled
            radially to have norm exactly 1 - epsilon.
        '''
        norm = np.linalg.norm(x)
        if norm >= 1.0 - self.epsilon:
            return x * ((1.0 - self.epsilon) / norm)
        return x

    def project_to_manifold_multiple(self, X):
        '''Vectorized version of project_to_manifold for many points at
        once.

        Arguments:
            X: An (N, 2) array of points in R^2 that may lie at or beyond
            the unit circle due to numerical error.

        Returns:
            An (N, 2) array with any offending points rescaled radially to
            have norm exactly 1 - epsilon.
        '''
        norms = np.linalg.norm(X, axis=1, keepdims=True)
        clamped = np.where(
            norms >= 1.0 - self.epsilon,
            X * ((1.0 - self.epsilon) / norms),
            X,
        )
        return clamped

    def euler_maruyama_step(self, x, dt):
        '''Simulates one step of Brownian motion from point x to the next
        point in the disk. Noise is first generated for point x (already
        scaled for the hyperbolic metric, see sample_tangent_noise) and
        then scaled by the square root of the time step. Then the next
        point becomes the previous plus the scaled noise, clamped back
        inside the disk if numerical error pushed it to or past the
        boundary.

        Arguments:
            x: A point in the disk.
            dt: A time step.

        Returns:
            The next point in the disk.
        '''
        noise = self.sample_tangent_noise(x)
        noise_scaled = np.sqrt(dt) * noise
        x_updated = x + noise_scaled
        return self.project_to_manifold(x_updated)

    def geodesic_distance_from_origin(self, x):
        '''Computes the hyperbolic (geodesic) distance from the origin to
        point x, using the standard Poincare-disk radial distance formula:

            rho(x) = 2 * artanh(|x|) = ln((1 + |x|) / (1 - |x|))

        This is the arc length of the straight-line radius from the origin
        to x, measured with the hyperbolic metric (see
        docs/writeups/2-poincare-disk-derivation.md section 4).

        Arguments:
            x: A point in the disk.

        Returns:
            The geodesic distance from the origin to x.
        '''
        r = np.linalg.norm(x)
        return np.log((1.0 + r) / (1.0 - r))

    def geodesic_distance_from_origin_multiple(self, X):
        '''Vectorized version of geodesic_distance_from_origin for many
        points at once.

        Arguments:
            X: An (N, 2) array of points in the disk.

        Returns:
            An (N,) array of geodesic distances from the origin.
        '''
        r = np.linalg.norm(X, axis=1)
        return np.log((1.0 + r) / (1.0 - r))

    def geodesic_distance(self, z, w):
        '''Computes the hyperbolic (geodesic) distance between two points z
        and w in the disk, using the standard closed-form Poincare-disk
        distance formula:

            d(z, w) = arccosh(1 + 2|z - w|^2 / ((1 - |z|^2)(1 - |w|^2)))

        Arguments:
            z: A point in the disk.
            w: A point in the disk.

        Returns:
            The geodesic distance between z and w.
        '''
        diff_norm_sq = np.dot(z - w, z - w)
        z_norm_sq = np.dot(z, z)
        w_norm_sq = np.dot(w, w)
        argument = 1.0 + 2.0 * diff_norm_sq / ((1.0 - z_norm_sq) * (1.0 - w_norm_sq))
        return np.arccosh(argument)

    def geodesic_distance_multiple(self, Z, w):
        '''Vectorized version of geodesic_distance: computes the distance
        from every point in Z to a single point w.

        Arguments:
            Z: An (N, 2) array of points in the disk.
            w: A single point in the disk.

        Returns:
            An (N,) array of geodesic distances from each point in Z to w.
        '''
        diff = Z - w
        diff_norm_sq = np.sum(diff * diff, axis=1)
        z_norm_sq = np.sum(Z * Z, axis=1)
        w_norm_sq = np.dot(w, w)
        argument = 1.0 + 2.0 * diff_norm_sq / ((1.0 - z_norm_sq) * (1.0 - w_norm_sq))
        return np.arccosh(argument)
