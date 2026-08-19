# Import the base class that contains Manifold abstract methods
from .base import Manifold
import numpy as np
import math

class Torus(Manifold):
    """The Torus class defines a geometric representation of a torus in R^3.
    It stores the torus parameters R and r, the major and minor radius,
    respectively.

    The class also includes methods for parameterization
    (converting between torus coordinates (u, v) and Cartesian coordinates
    (x, y, z)), computing surface normals and tangent directions, projecting
    points in R^3 onto the torus surface, and simulating Brownian motion
    using the Euler-Maruyama method.

    The Torus class ensures that all simulated points are constrained to the
    torus manifold for each step to an updated position on the torus. It also
    enables simulations to store the trajectory a point takes after many time
    steps.
    """
    def __init__(self, R, r):
        """Initializes the major and minor radii that define the torus'
        geometry.

        Arguments:
            R: Distance from the center of the central hole to the center
                of the tube.
            r: Radius of the tube.
        """
        self.R = R
        self.r = r

    def parametrize(self, u, v):
        """Converts parameters (u, v) on the torus to Cartesian (x, y, z)
        coordinates. Uses formulas

        x(u, v) = (R + rcos(v))cos(u)
        y(u, v) = (R + rcos(v))sin(u)
        z(u, v) = rsin(v)

        The toroidal angle (u) ranges from 0 to 2 pi and rotates around the
        main z-axis. The poloidal angle (v) ranges from 0 to 2 pi and rotates
        around the circular cross section of the tube.

        Arguments:
            u: The toroidal angle of the torus.
            v: The poloidal angle of the torus.

        Returns:
            The Cartesian coordinates of a point on the torus.
        """
        x = (self.R + self.r * math.cos(v)) * math.cos(u)
        y = (self.R + self.r * math.cos(v)) * math.sin(u)
        z = self.r * math.sin(v)
        point = np.array([x, y, z])
        return point

    def normal_vector(self, u, v):
        """Computes the unit normal vector at a point on the torus.
        The normal vector points perpendicular to the torus (away from the
        tube at that location).

        Uses the analytic formula for the torus normal, expressed as

        N(u, v) = (cos(u)cos(v), sin(u)cos(v), sin(v))

        The Cartesian components of the normal vector are

        x = cos(u)cos(v),
        y = sin(u)cos(v),
        z = sin(v)

        Arguments:
            u: The toroidal angle of the torus.
            v: The poloidal angle of the torus.

        Returns:
            The Cartesian coordinates of the unit normal vector at a
            point on the torus.
        """
        x = math.cos(u) * math.cos(v)
        y = math.sin(u) * math.cos(v)
        z = math.sin(v)
        normal_vector = np.array([x, y, z])
        return normal_vector

    def angles_from_point(self, x):
        """Recovers the angles (u, v) from a Cartesian point. Inverse of
        parametrize.

        Arguments:
            x: A point on the torus in R^3.

        Returns:
            A tuple (u, v) of the toroidal and poloidal angles of x.
        """
        x_coor = x[0]
        y_coor = x[1]
        z_coor = x[2]
        u = math.atan2(y_coor, x_coor)
        rho = math.sqrt(x_coor**2 + y_coor**2)
        v = math.atan2(z_coor, rho - self.R)
        return u, v

    def angles_from_points(self, X):
        """Vectorized version of angles_from_point for many points at once.

        Arguments:
            X: An (N, 3) array of points on the torus.

        Returns:
            A tuple (u, v) of (N,) arrays holding the toroidal and poloidal
            angles of each point in X.
        """
        x_coor = X[:, 0]
        y_coor = X[:, 1]
        z_coor = X[:, 2]
        u = np.arctan2(y_coor, x_coor)
        rho = np.sqrt(x_coor**2 + y_coor**2)
        v = np.arctan2(z_coor, rho - self.R)
        return u, v

    def project_to_tangent(self, x, v):
        """Projects a vector v onto the tangent plane at a point x on the torus.

        Takes a Cartesian point, matching the signature shared by every
        manifold. Recovers the angles from x, then defers to
        project_to_tangent_at_angles.

        Arguments:
            x: A point on the torus in R^3.
            v: An arbitrary vector in R^3 at point x.

        Returns:
            The component of v which lies in the tangent plane at x.
        """
        u_angle, v_angle = self.angles_from_point(x)
        return self.project_to_tangent_at_angles(u_angle, v_angle, v)

    def project_to_tangent_multiple(self, X, V):
        """Vectorized version of project_to_tangent for many points at once.

        Arguments:
            X: An (N, 3) array of points on the torus.
            V: An (N, 3) array of vectors, one per point in X.

        Returns:
            An (N, 3) array holding the tangential component of each vector
            in V at its corresponding point in X.
        """
        u_angles, v_angles = self.angles_from_points(X)

        normals = np.stack([
            np.cos(u_angles) * np.cos(v_angles),
            np.sin(u_angles) * np.cos(v_angles),
            np.sin(v_angles)
        ], axis=1)

        normal_components = np.sum(V * normals, axis=1, keepdims=True)
        return V - normal_components * normals

    def project_to_tangent_at_angles(self, u, v, vector):
        """Projects a vector onto the tangent plane of the torus. This
        is done by removing the normal component of the vector and only
        leaving the tangential component.

        The dot product of the vector and the unit normal vector measures
        how much of the vector points in the normal direction (away from
        the torus). When multiplied by the unit normal vector, it is the
        normal component of the vector.

        The formula used to find the tangential component of the vector is

        tangential_vector = vector - (dot product of vector and N) * N

        where N is the normal vector.

        Arguments:
            u: The toroidal angle of the torus.
            v: The poloidal angle of the torus.
            vector: An arbitrary vector.

        Returns:
            The tangential vector at (u, v).
        """
        normal = self.normal_vector(u, v)
        tangential_vector = vector - (np.dot(vector, normal)) * normal
        return tangential_vector

    def project_to_manifold_multiple(self, X):
        """Vectorized version of project_to_manifold for many points at once.

        Arguments:
            X: An (N, 3) array of points in R^3 that may or may not lie on
                the torus.

        Returns:
            An (N, 3) array containing the nearest point on the torus for
            each input point.
        """
        x_coor = X[:, 0]
        y_coor = X[:, 1]

        distance_from_z = np.sqrt(x_coor**2 + y_coor**2)
        center_x = self.R * (x_coor / distance_from_z)
        center_y = self.R * (y_coor / distance_from_z)
        center = np.stack([center_x, center_y, np.zeros_like(center_x)], axis=1)

        offset = X - center
        offset_norm = np.linalg.norm(offset, axis=1, keepdims=True)
        unit_offset = offset / offset_norm

        return center + self.r * unit_offset

    def sample_tangent_noise_multiple(self, X):
        """Vectorized version of sample_tangent_noise for many points at once.

        Arguments:
            X: An (N, 3) array of points on the torus.

        Returns:
            An (N, 3) array of random tangent vectors, one per input point.
        """
        u, v = self.angles_from_points(X)

        X_u = np.stack([
            -(self.R + self.r * np.cos(v)) * np.sin(u),
            (self.R + self.r * np.cos(v)) * np.cos(u),
            np.zeros_like(u)
        ], axis=1)

        X_v = np.stack([
            -self.r * np.sin(v) * np.cos(u),
            -self.r * np.sin(v) * np.sin(u),
            self.r * np.cos(v)
        ], axis=1)

        e_u = X_u / np.linalg.norm(X_u, axis=1, keepdims=True)
        e_v = X_v / np.linalg.norm(X_v, axis=1, keepdims=True)

        N = X.shape[0]
        a = np.random.randn(N, 1)
        b = np.random.randn(N, 1)

        return a * e_u + b * e_v

    def sample_tangent_noise(self, x):
        """
        Generates a random Gaussian vector in R^3 and projects it onto
        the tangent space at point x, which is on the torus.

        The Cartesian point x is first converted into its corresponding
        parameters (u, v) using the torus' geometry.

        Then, the derivative of X with respect to u and the derivate of X
        with respect to v are calculated. Both of them are normalized.
        These are the tangent drections (perpendicular to each other) on
        the surface.

        Two Gaussian random vectors are generated, multiplied to each
        tangent direction, and then summed to produce a single vector.
        This is the random step the point takes on the torus.

        Arguments:
            x: A point on the torus.

        Returns:
            A random vector in R^3 which is on the tangent space at point
            x on the torus.
        """
        u, v = self.angles_from_point(x)

        X_u = np.array([
            -(self.R + self.r * np.cos(v)) * np.sin(u),
            (self.R + self.r * np.cos(v)) * np.cos(u),
            0
        ])

        X_v = np.array([
            -self.r * np.sin(v) * np.cos(u),
            -self.r * np.sin(v) * np.sin(u),
            self.r * np.cos(v)
        ])

        e_u = X_u / np.linalg.norm(X_u)
        e_v = X_v / np.linalg.norm(X_v)

        a = np.random.randn()
        b = np.random.randn()

        return a * e_u + b * e_v

    def sample_tangent_noise_anisotropic(self, x):
        """
        Generated anistropic noise in one tangent direction at point
        x on the torus.

        A torus has two orthogonal tangent direction:
        - The direction around the large circle of the torus (R)
        - The direction around the smaller circular cross-sections of the
        torus (r)

        The toroidal direction is the motion around the large circle, while
        the poloidal direction is the motion around the cross-section.

        A Gaussian random vector is first generated and then multiplied
        by a scalar value (the noise). This is the random step the point
        takes on the torus, constrained to one tangent direction.

        Arguments:
            x: A point on the torus.

        Returns:
            A random vector in R^3 constrained to one tangent direction
            and at point x on the torus.
        """
        x_coor = x[0]
        y_coor = x[1]
        z_coor = x[2]
        u = math.atan2(y_coor, x_coor)
        rho = math.sqrt(x_coor**2 + y_coor**2)
        v = math.atan2(z_coor, rho - self.R)

        X_u = np.array([
            -(self.R + self.r * math.cos(v)) * math.sin(u),
            (self.R + self.r * math.cos(v)) * math.cos(u),
            0.0
        ])

        e_u = X_u / np.linalg.norm(X_u)

        scalar_noise = np.random.randn()

        return scalar_noise * e_u


    def sample_tangent_noise_anisotropic_multiple(self, X):
        """
        Generates anistropic Gaussian noise for many points on
        the torus.

        For each point, a scalar Gaussian variable (the noise) is
        multiplied by one tangent direction (e_u). Here, this is the
        direction around the large circle of the torus (R).

        Arguments:
            X: An (N, 3) array of points on the torus.

        Returns:
            An (N, 3) array of random Gaussian tangent vectors.
        """
        x_coor = X[:, 0]
        y_coor = X[:, 1]
        z_coor = X[:, 2]

        u = np.arctan2(y_coor, x_coor)
        rho = np.sqrt(x_coor**2 + y_coor**2)
        v = np.arctan2(z_coor, rho - self.R)

        X_u = np.stack([
            -(self.R + self.r * np.cos(v)) * np.sin(u),
            (self.R + self.r * np.cos(v)) * np.cos(u),
            np.zeros_like(u)
        ], axis=1)

        e_u = X_u / np.linalg.norm(X_u, axis=1, keepdims=True)

        N = X.shape[0]
        scalar_noise = np.random.randn(N, 1)

        return scalar_noise * e_u

    def project_to_manifold(self, x):
        """Projects a point in R^3 onto the torus. The projection is computed
        analytically rather than numerically.

        A torus consists of a large circle (radius R) and small circles (radius
        r) on every cross-section of the large circle.

        First, the nearest point on the major circle of radius R in the xy-plane
        is computed. This point is used as the center of the nearest tube
        cross-section of the torus. The offset is then computed from the tube center
        to the input point. It is normalized and scaled to the length of the tube's
        radius, which is r. The endpoint of the scaled offset vector is the nearest
        point on the torus, which is returned.

        Arguments:
            x: A point in R^3 that may or may not be on the torus.

        Returns:
            The nearest point on the torus from the input point.
        """
        x_coor = x[0]
        y_coor = x[1]

        distance_from_z = math.sqrt(x_coor**2 + y_coor**2)
        center_x = self.R * (x_coor / distance_from_z)
        center_y = self.R * (y_coor / distance_from_z)
        center = np.array([center_x, center_y, 0])

        offset = x - center
        offset_norm = np.linalg.norm(offset)
        unit_offset = offset / offset_norm

        point = center + self.r * unit_offset
        return point

    def euler_maruyama_step(self, x, dt):
        """Simulates one step of Brownian motion from point x to the next
        point on the torus. Noise is first generated for point x and
        then scaled by the square root of the time step. Then the next
        point becomes the previous plus the scaled noise and must be
        projected onto the torus.

        Variance measures how spread out the random positions are. It grows
        linearly with time (t). Standard deviation is the square root of
        variance and represents the net displacement (the distance from the
        start). Hence, the distance the walker travels from the starting point
        increases with the square root of t.

        The formula used to find the noise scaled is:
            Change in W_t = square root of change in t * Z, Z ~ N(0, 1)

        where change in W_t is the total random change in the system for the respective
        time step, t is the time step and Z is the standard normal random
        noise.

        Arguments:
            x: A point on the torus.
            dt: A time step.

        Returns:
            The next point on the torus.
        """
        noise = self.sample_tangent_noise(x)
        noise_scaled = np.sqrt(dt) * noise
        x_updated = x + noise_scaled
        return self.project_to_manifold(x_updated)