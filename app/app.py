import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math

import sys
sys.path.append("..")
from src.manifolds.sphere import Sphere
from src.manifolds.torus import Torus
from src.simulation.simulator import simulator, torus_simulator, hyperbolic_simulator
from src.visualization.kde import sphere_kde
from src.visualization.hyperbolic_kde import disk_kde, boundary_angle_histogram

# Explanatory content shown in each parameter's help modal: the equation it
# appears in (LaTeX, or None if it isn't part of an equation) and a
# plain-language explanation of what changing it does.
PARAM_HELP = {
    "N": {
        "title": "Number of Particles (N)",
        "latex": None,
        "explanation": (
            "N is how many independent sample paths are simulated at once. More particles give "
            "a smoother, more accurate empirical distribution and density heatmap, at the cost "
            "of more computation. It does not change the dynamics of any single particle."
        ),
    },
    "T": {
        "title": "Number of Steps (T)",
        "latex": r"t_{\text{final}} = T \cdot dt",
        "explanation": (
            "T is how many discrete time steps the simulation advances. Combined with the time "
            "step dt, it sets the total elapsed simulated time and how many frames the animated "
            "trajectory has."
        ),
    },
    "dt": {
        "title": "Time Step (dt)",
        "latex": r"X_{n+1} = \Pi_M\left(X_n + \sqrt{dt}\; Z_n\right), \qquad Z_n \sim \mathcal{N}(0, I)\ \text{in the tangent plane}",
        "explanation": (
            "dt is the size of each discrete time increment in the Euler-Maruyama approximation "
            "of Brownian motion on the manifold. It enters as the square root of dt scaling the "
            "random tangent step, since Brownian motion accumulates standard deviation "
            "proportional to the square root of elapsed time. Smaller dt more closely "
            "approximates the true continuous-time process, but needs more steps (T) to reach "
            "the same total simulated time."
        ),
    },
    "k": {
        "title": "Concentration Parameter (k)",
        "latex": r"\text{density}(y) \;\propto\; \sum_i \exp\big(k \cdot x_i \cdot y\big)",
        "explanation": (
            "k is the concentration parameter of the von Mises-Fisher kernel used to turn the "
            "final particle positions into the sphere's density heatmap. Larger k concentrates "
            "each particle's contribution more tightly around itself, producing a sharper "
            "heatmap; smaller k spreads it out into a smoother estimate. It only "
            "affects the visualization."
        ),
    },
    "noise_type": {
        "title": "Noise Type",
        "latex": r"\text{Isotropic: } v = \Pi_x(Z),\ Z \sim \mathcal{N}(0, I) \qquad\quad \text{Anisotropic: } v = \Pi_x(u) \cdot Z,\ Z \sim \mathcal{N}(0, 1)",
        "explanation": (
            "Isotropic noise samples a full Gaussian vector and projects it onto the tangent "
            "plane, so a particle can move in any tangent direction. Anisotropic noise (sphere "
            "only) instead scales a single fixed tangent direction by one scalar Gaussian, so "
            "motion is restricted to that one direction."
        ),
    },
    "lat_long": {
        "title": "Starting Latitude / Longitude",
        "latex": r"x_0 = (\cos\theta\cos\phi,\ \cos\theta\sin\phi,\ \sin\theta)",
        "explanation": (
            "Latitude (theta) and longitude (phi) are converted to radians and plugged into the "
            "standard spherical parametrization to give the starting point x0 on the unit "
            "sphere."
        ),
    },
    "R_r": {
        "title": "Major / Minor Radius (R, r)",
        "latex": r"x(u,v) = (R + r\cos v)\cos u,\quad y(u,v) = (R + r\cos v)\sin u,\quad z(u,v) = r \sin v",
        "explanation": (
            "R is the distance from the torus's central axis to the center of its tube; r is "
            "the radius of the tube itself. Together they define the torus's surface and "
            "curvature. The outer half (cos v > 0) is positively curved, the inner half "
            "is negatively curved."
        ),
    },
    "uv": {
        "title": "Starting Toroidal / Poloidal Angle (u, v)",
        "latex": r"x_0 = \big((R + r\cos v)\cos u,\ (R + r\cos v)\sin u,\ r\sin v\big)",
        "explanation": (
            "u is the angle around the torus's central axis, v is the angle around its "
            "circular cross-section. Together they set the starting point x0 on the torus."
        ),
    },
    "r_theta": {
        "title": "Starting Radius / Angle (r, theta)",
        "latex": r"x_0 = (r\cos\theta,\ r\sin\theta), \qquad \rho_0 = \ln\!\left(\frac{1+r}{1-r}\right)",
        "explanation": (
            "r and theta are polar coordinates in the Poincare disk, converted to (x, y) to give "
            "the starting point x0. r must stay below 1; rho0 is the corresponding hyperbolic "
            "distance of the starting point from the center."
        ),
    },
}

# Helper function for displaying parameter details in app modal
@st.dialog("Parameter Details")
def show_param_help(key):
    info = PARAM_HELP[key]
    st.markdown(f"#### {info['title']}")
    if info["latex"]:
        st.latex(info["latex"])
    st.markdown(info["explanation"])

# Helper function for rendering app sidebar widgets with a help button. 
# Clicking the button opens a modal with an explanation of the parameter.
def with_help(widget_key, render_widget, content_key=None):
    content_key = content_key or widget_key
    col_widget, col_help = st.columns([8, 2])
    with col_widget:
        value = render_widget()
    with col_help:
        if st.button("?", key=f"help_btn_{widget_key}", use_container_width=True):
            show_param_help(content_key)
    return value

# Helper function for creating a sphere surface
def sphere_creation():
    # Get angle arrays
    theta = np.linspace(0, 2*math.pi, num=100)
    phi = np.linspace(0, math.pi, num=100)
    
    # Store theta and phi angles in a 2 dimensional coordinate matrix
    theta_grid, phi_grid = np.meshgrid(theta, phi)
    
    # Apply sphere formulas for each axis of the surface
    x_surface = np.sin(phi_grid) * np.cos(theta_grid)
    y_surface = np.sin(phi_grid) * np.sin(theta_grid)
    z_surface = np.cos(phi_grid)
    
    # Create surface of sphere
    surface = go.Surface(
        x=x_surface,
        y=y_surface,
        z=z_surface,
        opacity=0.5,
        showscale=False # Hide the color scale bar
    )
    return surface, x_surface, y_surface, z_surface

# Helper function for creating a torus surface
def torus_creation(R, r):
    # Get angle arrays
    u = np.linspace(0, 2*math.pi, num=100) # angle around the central axis of the torus
    v = np.linspace(0, 2*math.pi, num=100) # angle around the circular cross-section of the torus
    
    # Store u and v angles in a 2 dimensional coordinate matrix
    u_grid, v_grid = np.meshgrid(u, v)
    
    # Apply torus formulas for each axis of the surface
    x_surface = (R + r*np.cos(v_grid)) * np.cos(u_grid)
    y_surface = (R + r*np.cos(v_grid)) * np.sin(u_grid)
    z_surface = r*np.sin(v_grid)
    
    # Create surface of torus
    surface = go.Surface(
        x=x_surface,
        y=y_surface,
        z=z_surface,
        opacity=0.5,
        showscale=False
    )
    return surface, x_surface, y_surface, z_surface


# Helper function for creating the Poincare disk's boundary circle and density heatmap.
# Note this is 2D since H^2 has no isometric embedding into R^3 (Hilbert's theorem)

M = 100 # Resolution of density heatmap's mesh grid. Higher M -> smoother heatmap but longer render time

def disk_creation(mesh_resolution=M):

    # Create the boundary circle of the Poincare disk
    theta = np.linspace(0, 2*math.pi, num=200)
    boundary = go.Scatter( 
        x=np.cos(theta),
        y=np.sin(theta),
        mode="lines",
        line=dict(color="gray"),
        showlegend=False
    )
    # Create mesh grid of points inside disk for the density heatmap
    grid = np.linspace(-1, 1, num=mesh_resolution)
    x_mesh, y_mesh = np.meshgrid(grid, grid)
    return boundary, x_mesh, y_mesh

# Helper function that removes the numeric tick labels from a plot's axes
def hide_axis_numbers(figure, is_3d=True):
    if is_3d:
        figure.update_layout(scene=dict(
            xaxis=dict(showticklabels=False),
            yaxis=dict(showticklabels=False),
            zaxis=dict(showticklabels=False),
        ))
    else:
        figure.update_xaxes(showticklabels=False)
        figure.update_yaxes(showticklabels=False)
    return figure

# Helper function for drawing the animated BM trajectory on both manifolds
def build_animation_figure(surface, path, starting_point):
    # Create frames for animation
    frames = []
    for i in range(1, len(path), 10):
        frames.append(
            go.Frame(
                data=[go.Scatter3d(
                    x=path[:i, 0],
                    y=path[:i, 1],
                    z=path[:i, 2],
                    mode="lines",
                    line=dict(color="black")
                )
            ],
            traces=[1],
            name=str(i)
            )
        )
    # Starting point
    starting_marker = go.Scatter3d(
        x=[starting_point[0]],
        y=[starting_point[1]],
        z=[starting_point[2]],
        mode="markers",
        marker=dict(size=5, color="red"),
        showlegend=False
    )
    # Starting trace
    animated_trace = go.Scatter3d(
        x=path[:1, 0],
        y=path[:1, 1],
        z=path[:1, 2],
        mode="lines",
        line=dict(color="black"),
        showlegend=False
    )
    # Render the animation figure
    animation_figure = go.Figure(
        data=[surface, animated_trace, starting_marker],
        frames=frames
    )
    animation_figure.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                buttons=[
                    dict(
                        label="Play",
                        method="animate",
                        args=[
                            None,
                            {
                                # 3D (WebGL) traces like Scatter3d, need
                                # redraw=True to animate; the camera
                                # is instead kept steady via uirevision
                                # below, which persists through redraws
                                "frame": {"duration": 50, "redraw": True},
                                "fromcurrent": True
                            }
                        ]
                    )
                ]
            )
        ],
        showlegend=False,
        # Keeps the camera position (zoom/rotation) across any
        # re-renders instead of resetting to default view
        uirevision="constant"
    )
    hide_axis_numbers(animation_figure)
    return animation_figure, starting_marker

# Helper function for building the animated trajectory figure on the Poincare disk
def build_animation_figure_2d(boundary, path, starting_point):
    frames = []
    for i in range(1, len(path), 10):
        frames.append(
            go.Frame(
                data=[go.Scatter(
                    x=path[:i, 0],
                    y=path[:i, 1],
                    mode="lines",
                    line=dict(color="black")
                )
            ],
            traces=[1],
            name=str(i)
            )
        )
    starting_marker = go.Scatter(
        x=[starting_point[0]],
        y=[starting_point[1]],
        mode="markers",
        marker=dict(size=8, color="red"),
        showlegend=False
    )
    animated_trace = go.Scatter(
        x=path[:1, 0],
        y=path[:1, 1],
        mode="lines",
        line=dict(color="black"),
        showlegend=False
    )
    animation_figure = go.Figure(
        data=[boundary, animated_trace, starting_marker],
        frames=frames
    )
    animation_figure.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                buttons=[
                    dict(
                        label="Play",
                        method="animate",
                        args=[
                            None,
                            {
                                "frame": {"duration": 50, "redraw": True},
                                "fromcurrent": True
                            }
                        ]
                    )
                ]
            )
        ],
        showlegend=False,
        uirevision="constant",
        xaxis=dict(scaleanchor="y", scaleratio=1, range=[-1.05, 1.05]),
        yaxis=dict(range=[-1.05, 1.05]),
    )
    hide_axis_numbers(animation_figure, is_3d=False)
    return animation_figure, starting_marker

# Set up browser tab title and layout
st.set_page_config(page_title="Brownian Motion Simulation", layout="wide")

# Sidebar layout
# Use lambda functions to defer evaluation of widgets until after the manifold is selected so the noise type options update accordingly
with st.sidebar:
    st.header("Settings")
    st.write("Edit the parameters here")

    manifold = st.selectbox(
        "Select the manifold:",
        options=["Sphere", "Torus", "Poincaré Disk"]
    )

    N = with_help("N", lambda: st.slider(
        label="Number of Particles (N)",
        min_value=1, max_value=1000,
        value=500
    ))
    T = with_help("T", lambda: st.slider(
        label="Number of Steps (T)",
        min_value=10,
        max_value=5000,
        value=1000
    ))
    dt = with_help("dt", lambda: st.slider(
        label="Time Step (dt)",
        min_value=0.001,
        max_value=0.1,
        value=0.01
    ))
    k = with_help("k", lambda: st.slider(
        label="Concentration Parameter (k)",
        min_value=1,
        max_value=100,
        value=20
    ))

    noise_options = ["Isotropic", "Anisotropic"] if manifold == "Sphere" else ["Isotropic"]
    noise_type = with_help("noise_type", lambda: st.selectbox(
        label="Noise Type",
        options=noise_options
    ))

    if manifold == "Sphere":
        lat = with_help("lat", lambda: st.slider(
            label="Starting latitude",
            min_value=-90,
            max_value=90,
            value=0
        ), content_key="lat_long")
        long = with_help("long", lambda: st.slider(
            label="Starting longitude",
            min_value=-180,
            max_value=180,
            value=0
        ), content_key="lat_long")
        # Convert degrees to radians
        lat_rad = np.radians(lat)
        long_rad = np.radians(long)
        # Compute the starting point on the sphere from radians
        starting_point = np.array([
            np.cos(lat_rad) * np.cos(long_rad),
            np.cos(lat_rad) * np.sin(long_rad),
            np.sin(lat_rad)
        ])
        start_label = f"({lat} degrees, {long} degrees)"
        
    elif manifold == "Torus":
        R = with_help("R", lambda: st.slider(
            label="Major radius (R)",
            min_value=1.0,
            max_value=10.0,
            value=3.0,
            step=0.5
        ), content_key="R_r")
        r = with_help("r", lambda: st.slider(
            label="Minor radius (r)",
            min_value=0.1,
            max_value=R - 0.1,
            value=min(1.0, R - 0.1),
            step=0.1
        ), content_key="R_r")
        start_u = with_help("start_u", lambda: st.slider(
            label="Starting toroidal angle (u)",
            min_value=0,
            max_value=360,
            value=0
        ), content_key="uv")
        start_v = with_help("start_v", lambda: st.slider(
            label="Starting poloidal angle (v)",
            min_value=0,
            max_value=360,
            value=0
        ), content_key="uv")
        # Convert degrees to radians
        u_rad = np.radians(start_u)
        v_rad = np.radians(start_v)
        # Compute the starting point on the torus from radians
        starting_point = Torus(R, r).parametrize(u_rad, v_rad)
        start_label = f"(u={start_u} degrees, v={start_v} degrees)"
        
    else: # Poincare Disk
        start_r = with_help("start_r", lambda: st.slider(
            label="Starting radius (r)",
            min_value=0.0,
            max_value=0.95,
            value=0.0,
            step=0.05
        ), content_key="r_theta")
        start_theta = with_help("start_theta", lambda: st.slider(
            label="Starting angle (theta, degrees)",
            min_value=0,
            max_value=360,
            value=0
        ), content_key="r_theta")
        theta_rad = np.radians(start_theta)
        starting_point = np.array([
            start_r * np.cos(theta_rad),
            start_r * np.sin(theta_rad)
        ])
        start_label = f"(r={start_r}, theta={start_theta} degrees)"

    # Run simulation button
    run_clicked = st.button(
        "Run Simulation",
        type="primary",
        use_container_width=True
    )

# Title
st.title("Brownian Motion Simulation")

# Project description
st.markdown("""
### Project Description
This project simulates Brownian motion on a Riemannian manifold.
Brownian motion is the random evolution of particles over time. It is simulated using the Euler-Maruyama method for stochastic differential equations.
Two types of noise are supported:
- Isotropic noise allows motion in all tangent directions, uniformly.
- Anisotropic noise restricts motion to only one tangent direction, producing structured trajectories (currently only implemented for the sphere).

Animation and visualizations are provided below, with these features:
- Red dot to display the initial position of particles on the manifold.
- Black trajectories showing sample paths of individual particles.
- Final particle distribution with black dots to display the final positions on the manifold.
- A density heatmap of the final particle distribution (a von Mises-Fisher KDE over the sphere surface, an occupation histogram in (u, v) coordinates for the torus, or a geodesic KDE plus boundary-angle histogram for the Poincaré disk).

What users can adjust:
- Number of particles (N)
- Number of time steps (T)
- Size of time steps (dt)
- Concentration parameter (k), used by the sphere's and Poincaré disk's KDE heatmaps
- Noise type (isotropic vs anisotropic)
- Starting position on the manifold
- Major/minor radius (R, r), for the torus
""")

st.divider()

# Build the surface for the currently selected manifold up front
is_disk = (manifold == "Poincaré Disk")

if manifold == "Sphere":
    surface, x_surface, y_surface, z_surface = sphere_creation()
elif manifold == "Torus":
    surface, x_surface, y_surface, z_surface = torus_creation(R, r)
else: # Poincare Disk
    surface, x_surface, y_surface = disk_creation()

if is_disk:
    starting_marker = go.Scatter(
        x=[starting_point[0]],
        y=[starting_point[1]],
        mode="markers",
        marker=dict(size=8, color="red"),
        showlegend=False
    )
else:
    starting_marker = go.Scatter3d(
        x=[starting_point[0]],
        y=[starting_point[1]],
        z=[starting_point[2]],
        mode="markers",
        marker=dict(size=5, color="red"),
        showlegend=False
    )

# Simulation shown
st.subheader("Simulation")
# Display user's selected parameters after they click Run Simulation
if run_clicked == True:
    st.markdown("**Selected Parameters**")
    cols1 = st.columns(3)
    cols2 = st.columns(3)
    cols1[0].markdown(f"**Manifold**  \n{manifold}")
    cols1[1].markdown(f"**Particles**  \n{N}")
    cols1[2].markdown(f"**Steps**  \n{T}")
    cols2[0].markdown(f"**dt**  \n{dt}")
    cols2[1].markdown(f"**Noise Type**  \n{noise_type}")
    cols2[2].markdown(f"**Starting Point**  \n{start_label}")
    # Run simulation on the selected manifold
    if manifold == "Sphere":
        trajectory = simulator(T, N, dt, noise_type.lower(), starting_point=starting_point)
    elif manifold == "Torus":
        trajectory = torus_simulator(T, N, dt, R, r, starting_point=starting_point)
    else: # Poincare Disk
        trajectory = hyperbolic_simulator(T, N, dt, starting_point=starting_point)
    # Get first particle path
    path = trajectory[:, 0, :]
    # Build the animated trajectory figure (2D for the disk, 3D otherwise)
    if is_disk:
        animation_figure, starting_marker = build_animation_figure_2d(surface, path, starting_point)
    else:
        animation_figure, starting_marker = build_animation_figure(surface, path, starting_point)
    # Plot the animation
    st.plotly_chart(animation_figure, key="animation_figure")
else:
    # Empty state: show the selected surface and starting point only, with
    # no trajectory yet
    empty_figure = go.Figure(data=[surface, starting_marker])
    if is_disk:
        empty_figure.update_layout(
            xaxis=dict(scaleanchor="y", scaleratio=1, range=[-1.05, 1.05]),
            yaxis=dict(range=[-1.05, 1.05]),
        )
    empty_figure = hide_axis_numbers(empty_figure, is_3d=not is_disk)
    st.plotly_chart(empty_figure)

st.divider()

# Visualizations (plots)
st.subheader("Visualizations")
# Tabs
tab1, tab2 = st.tabs([
    "Final Particle Distribution",
    "Density Heatmap"
])
# Run simulation to display plots
if run_clicked == True:
    # Show final positions of all particles
    with tab1:
        final_positions = trajectory[-1]
        if is_disk:
            # Particle trace (2D, no z-coordinate)
            particle_trace = go.Scatter(
                x=final_positions[:, 0],
                y=final_positions[:, 1],
                mode="markers",
                marker=dict(size=3, color="black"),
                showlegend=False
            )
            figure = go.Figure(data=[surface, particle_trace, starting_marker])
            figure.update_layout(
                xaxis=dict(scaleanchor="y", scaleratio=1, range=[-1.05, 1.05]),
                yaxis=dict(range=[-1.05, 1.05]),
            )
            figure = hide_axis_numbers(figure, is_3d=False)
        else:
            # Coordinates
            x_coor = final_positions[:, 0]
            y_coor = final_positions[:, 1]
            z_coor = final_positions[:, 2]
            # Particle trace
            particle_trace = go.Scatter3d(
                x=x_coor,
                y=y_coor,
                z=z_coor,
                mode="markers",
                marker=dict(size=2, color="black"),
                showlegend=False
            )
            # Plot figure
            figure = hide_axis_numbers(go.Figure(
                data=[surface, particle_trace, starting_marker]
            ))
        st.plotly_chart(figure)
    # Show density heatmap
    with tab2:
        # Get final positions
        final_positions = trajectory[-1]
        if manifold == "Sphere":
            # Create a vMF KDE over sphere surface
            density = sphere_kde(
                final_positions,
                x_surface,
                y_surface,
                z_surface,
                k,
                N
            )
            density_surface = go.Surface(
                x=x_surface,
                y=y_surface,
                z=z_surface,
                surfacecolor=density,
                colorscale="Viridis",
                showscale=True
            )
            figure = hide_axis_numbers(go.Figure(data=[density_surface, starting_marker]))
            st.plotly_chart(figure)
        elif manifold == "Torus":      
            x_coor = final_positions[:, 0]
            y_coor = final_positions[:, 1]
            z_coor = final_positions[:, 2]
            rho = np.sqrt(x_coor**2 + y_coor**2)
            u_values = np.arctan2(y_coor, x_coor) % (2 * np.pi)
            v_values = np.arctan2(z_coor, rho - R) % (2 * np.pi)
            histogram, u_edges, v_edges = np.histogram2d(
                u_values, v_values, bins=30, range=[[0, 2 * np.pi], [0, 2 * np.pi]]
            )
            max_count = histogram.max()
            density = histogram / max_count if max_count > 0 else histogram
            heatmap = go.Heatmap(
                z=density.T,
                x=(u_edges[:-1] + u_edges[1:]) / 2,
                y=(v_edges[:-1] + v_edges[1:]) / 2,
                colorscale="Viridis"
            )
            figure = hide_axis_numbers(go.Figure(data=[heatmap]), is_3d=False)
            figure.update_layout(
                xaxis_title="u (toroidal angle)",
                yaxis_title="v (poloidal angle)"
            )
            st.plotly_chart(figure)
            st.caption(
                "The theoretical invariant density is p(u, v) = (R + r cos v) / (4π²R) "
                "which is not uniform in v since the embedded torus has non-constant curvature."
            )
        else: # Poincare Disk
            # Geodesic KDE using hyperbolic distance (see src/visualization/hyperbolic_kde.py). 
            # H^2 has no invariant density to compare against since Brownian motion here is transient 
            # so this just shows the current particle position.
            density = disk_kde(final_positions, x_surface, y_surface, k, N)
            density_plot = go.Contour(
                x=x_surface[0],
                y=y_surface[:, 0],
                z=density,
                colorscale="Viridis",
                showscale=True,
                connectgaps=False,
                contours=dict(coloring="heatmap"),
            )
            figure = go.Figure(data=[density_plot])
            figure.update_layout(
                xaxis=dict(scaleanchor="y", scaleratio=1, range=[-1.05, 1.05]),
                yaxis=dict(range=[-1.05, 1.05]),
            )
            figure = hide_axis_numbers(figure, is_3d=False)
            st.plotly_chart(figure)
            st.caption(
                "Geodesic KDE using the exact hyperbolic distance in the hyperbolic "
                "disk. H² has no invariant density to converge to, so particles are "
                "expected to concentrate nearthe boundary circle as time increases "
                "rather than filling the disk uniformly."
            )

            # Paths converge to a random point on the boundary circle; by the rotational
            # symmetry of the metric about the origin, that limiting angle must
            # be uniformly distributed. See notebooks/Notebook-04.ipynb.
            radius_threshold = 0.8
            histogram, bin_edges = boundary_angle_histogram(
                final_positions, radius_threshold=radius_threshold
            )
            if histogram is not None:
                bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
                angle_figure = go.Figure(data=[
                    go.Barpolar(
                        r=histogram,
                        theta=np.degrees(bin_centers),
                        marker=dict(color="teal"),
                    )
                ])
                angle_figure.update_layout(showlegend=False)
                st.plotly_chart(angle_figure)
                st.caption(
                    f"Angular position of particles with radius ≥ {radius_threshold}, "
                    "near the boundary circle. Rotational symmetry of the hyperbolic "
                    "metric about the origin implies this angle should approach a "
                    "uniform distribution as more particles reach the boundary."
                )
            else:
                st.caption(
                    f"No particles have reached radius ≥ {radius_threshold} yet."
                    "Try more steps (T) or a larger time step (dt)."
                )
