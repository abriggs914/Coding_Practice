import streamlit as st
import subprocess
import tempfile
import os

from solid2 import scad_render_to_file, text, linear_extrude, rotate, translate, union
import plotly.graph_objects as go
from stl import mesh
import numpy as np
from matplotlib import font_manager


# =====================================
# STL GENERATION FUNCTION
# =====================================
# def generate_text_stl(
#     text_str: str,
#     font_name: str,
#     size: float,
#     thickness: float,
#     halign: str,
#     valign: str,
# ) -> str:
#     """Generates an STL file for given text and returns the STL path."""
#     output_dir = os.path.abspath(".")
#     scad_path = os.path.join(output_dir, "text_model.scad")
#     stl_path = os.path.join(output_dir, "text_model.stl")


#     model = linear_extrude(height=thickness)(
#         text(
#             text_str,
#             font=font_name,
#             size=size,
#             halign=halign,
#             valign=valign,
#         )
#     )

#     scad_render_to_file(model, scad_path)

#     # Render STL via OpenSCAD CLI
#     subprocess.run(["openscad", "-o", stl_path, scad_path], check=True)

#     return stl_path


def generate_text_stl(
    text_str: str,
    font_name: str,
    size: float,
    thickness: float,
    halign: str,
    valign: str,
    wrap_radius: float = 0.0,
):
    output_dir = os.path.abspath(".")
    scad_path = os.path.join(output_dir, "text_model.scad")
    stl_path = os.path.join(output_dir, "text_model.stl")

    # Base text
    txt = linear_extrude(height=thickness)(
        text(text_str, font=font_name, size=size, halign=halign, valign=valign)
    )

    # If wrap_radius is set, bend the text
    if wrap_radius > 0:
        # approximate curvature by rotating small slices of text
        # OpenSCAD rotate_extrude can only handle 2D paths, so we wrap the extrusion manually
        curved_segments = []
        num_segments = len(text_str) * 4
        angle_per_seg = 360 / (2 * np.pi * wrap_radius) * size / num_segments
        for i in range(num_segments):
            curved_segments.append(
                rotate(a=[0, 0, i * angle_per_seg])(translate([wrap_radius, 0, 0])(txt))
            )
        model = union()(*curved_segments)
    else:
        model = txt

    scad_render_to_file(model, scad_path)
    subprocess.run(["openscad", "-o", stl_path, scad_path], check=True)
    return stl_path


# =====================================
# STREAMLIT APP UI
# =====================================
st.set_page_config(page_title="3D Text Generator", page_icon="🔤", layout="wide")

st.title("🧱 3D Text → STL Generator")
st.caption("Generate 3D-printable text with custom fonts and extrusion depth.")

# Sidebar configuration
st.sidebar.header("⚙️ Parameters")

text_str = st.sidebar.text_input("Text to render", "Avery")
# font_name = st.sidebar.text_input("Font name", "Brush Script MT")

# Get a short list of nice, legible fonts — or all available TTFs
font_paths = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
font_names = sorted(set(font_manager.FontProperties(fname=fp).get_name() for fp in font_paths))
font_names = [f for f in font_names if f[0].isupper()]  # optional filter

font_name = st.sidebar.selectbox("Font name", options=font_names, index=font_names.index("Brush Script MT") if "Brush Script MT" in font_names else 0)

font_size = st.sidebar.slider("Font size (mm)", 5, 100, 20)
thickness = st.sidebar.slider("Extrusion height (mm)", 1, 20, 3)
wrap_radius = st.sidebar.slider("Wrap radius (mm)", 0, 200, 0, disabled=True)

halign = st.sidebar.selectbox("Horizontal alignment", ["left", "center", "right"], index=1)
valign = st.sidebar.selectbox(
    "Vertical alignment", ["baseline", "bottom", "center", "top"], index=0
)

generate_btn = st.sidebar.button("🚀 Generate STL")

# =====================================
# MAIN CONTENT
# =====================================
if generate_btn:
    with st.spinner("Generating STL..."):
        try:
            stl_path = generate_text_stl(
                text_str=text_str,
                font_name=font_name,
                size=font_size,
                thickness=thickness,
                halign=halign,
                valign=valign,
                wrap_radius=wrap_radius
            )

            st.success("✅ STL Generated Successfully!")
            st.download_button(
                "⬇️ Download STL",
                data=open(stl_path, "rb").read(),
                file_name=f"{text_str.replace(' ', '_')}.stl",
                mime="application/vnd.ms-pki.stl",
            )

            # Display 3D preview
            st.subheader("🔍 3D Preview")            
            
            m = mesh.Mesh.from_file(stl_path)
            
            # Extract vertex coordinates
            # Each facet has 3 vertices: shape = (num_facets, 3, 3)
            x = m.vectors[:, :, 0].flatten()
            y = m.vectors[:, :, 1].flatten()
            z = m.vectors[:, :, 2].flatten()

            # Build face indices (0,1,2), (3,4,5), etc.
            faces = np.arange(len(x)).reshape(-1, 3)
            i, j, k = faces[:, 0], faces[:, 1], faces[:, 2]

            fig = go.Figure(
                data=[
                    go.Mesh3d(
                        x=x,
                        y=y,
                        z=z,
                        i=i,
                        j=j,
                        k=k,
                        color="orange",
                        opacity=1.0,
                        flatshading=True,
                        lighting=dict(ambient=0.4, diffuse=0.8, roughness=0.3, specular=0.4),
                        lightposition=dict(x=0, y=1, z=1)
                    )
                ]
            )

            fig.update_layout(
                scene=dict(
                    aspectmode="data",
                    xaxis=dict(visible=False),
                    yaxis=dict(visible=False),
                    zaxis=dict(visible=False),
                    camera=dict(eye=dict(x=1.5, y=-1.5, z=1.5))
                ),
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor="#0e1117",
            )

            st.plotly_chart(fig, use_container_width=True)

        except subprocess.CalledProcessError as e:
            st.error("❌ OpenSCAD failed to render STL. Make sure OpenSCAD is installed and in PATH.")
            st.exception(e)

else:
    st.info("👈 Enter your text and click *Generate STL* to begin.")