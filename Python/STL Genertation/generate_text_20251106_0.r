import streamlit as st
import subprocess
import tempfile
import os

from solid2 import scad_render_to_file, text, linear_extrude
import plotly.graph_objects as go
from stl import mesh
import numpy as np


# =====================================
# STL GENERATION FUNCTION
# =====================================
def generate_text_stl(
    text_str: str,
    font_name: str,
    size: float,
    thickness: float,
    halign: str,
    valign: str,
) -> str:
    """Generates an STL file for given text and returns the STL path."""
    output_dir = os.path.abspath(".")
    scad_path = os.path.join(output_dir, "text_model.scad")
    stl_path = os.path.join(output_dir, "text_model.stl")


    model = linear_extrude(height=thickness)(
        text(
            text_str,
            font=font_name,
            size=size,
            halign=halign,
            valign=valign,
        )
    )

    scad_render_to_file(model, scad_path)

    # Render STL via OpenSCAD CLI
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
font_name = st.sidebar.text_input("Font name", "Brush Script MT")
font_size = st.sidebar.slider("Font size (mm)", 5, 100, 20)
thickness = st.sidebar.slider("Extrusion height (mm)", 1, 20, 3)

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
                valign=valign
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
            # # # # # stl_viewer(stl_path, width=600, height=400)
            # # # # success = stl_from_file(
            # # # #     file_path=stl_path,          # Path to the STL file
            # # # #     color='#FF9900',                 # Color of the STL file (hexadecimal value)
            # # # #     material='material',             # Material of the STL file ('material', 'flat', or 'wireframe')
            # # # #     auto_rotate=True,                # Enable auto-rotation of the STL model
            # # # #     opacity=1,                       # Opacity of the STL model (0 to 1)
            # # # #     shininess=100,                   # How shiny the specular highlight is, when using the 'material' style.
            # # # #     cam_v_angle=60,                  # Vertical angle (in degrees) of the camera
            # # # #     cam_h_angle=-90,                 # Horizontal angle (in degrees) of the camera
            # # # #     cam_distance=None,               # Distance of the camera from the object (defaults to 3x bounding box size)
            # # # #     height=500,                      # Height of the viewer frame
            # # # #     max_view_distance=1000,          # Maximum viewing distance for the camera,
            # # # #     key=None
            # # # # )
            # # # import plotly.graph_objects as go
            # # # import numpy as np
            # # # import stl
            # # # import streamlit_stl as sstl
            # # # stl_from_file = stl_component.stl_from_file

            # # # with open(stl_path, "rb") as f:
            # # #     st.write(f"{type(f)=}")
            # # #     stl_mesh = stl.read_binary_file(f)
            # # #     fig = go.Figure(
            # # #         data=[go.Mesh3d(
            # # #             x=stl_mesh.x.flatten(),
            # # #             y=stl_mesh.y.flatten(),
            # # #             z=stl_mesh.z.flatten(),
            # # #             color='orange',
            # # #             opacity=1.0
            # # #         )]
            # # #     )
            # # #     st.plotly_chart(fig, use_container_width=True)

            # # # Load STL file using numpy-stl
            # # your_mesh = mesh.Mesh.from_file(stl_path)

            # # # Build Plotly figure
            # # fig = go.Figure(
            # #     data=[
            # #         go.Mesh3d(
            # #             x=your_mesh.x.flatten(),
            # #             y=your_mesh.y.flatten(),
            # #             z=your_mesh.z.flatten(),
            # #             color='orange',
            # #             opacity=1.0,
            # #             flatshading=True,
            # #         )
            # #     ]
            # # )

            # # fig.update_layout(
            # #     scene=dict(
            # #         xaxis=dict(visible=False),
            # #         yaxis=dict(visible=False),
            # #         zaxis=dict(visible=False)
            # #     ),
            # #     margin=dict(l=0, r=0, t=0, b=0)
            # # )

            # # st.plotly_chart(fig, use_container_width=True)

            # # # your_mesh = mesh.Mesh.from_file(stl_path)

            # # # fig = go.Figure(
            # # #     data=[
            # # #         go.Mesh3d(
            # # #             x=your_mesh.x.flatten(),
            # # #             y=your_mesh.y.flatten(),
            # # #             z=your_mesh.z.flatten(),
            # # #             color="orange",
            # # #             opacity=1.0,
            # # #             flatshading=True,
            # # #         )
            # # #     ]
            # # # )

            # # # fig.update_layout(
            # # #     scene=dict(
            # # #         xaxis=dict(visible=False),
            # # #         yaxis=dict(visible=False),
            # # #         zaxis=dict(visible=False)
            # # #     ),
            # # #     margin=dict(l=0, r=0, t=0, b=0)
            # # # )

            # # # st.plotly_chart(fig, use_container_width=True)
            # m = mesh.Mesh.from_file(stl_path)

            # # Each facet in the STL has 3 vertices (triangles)
            # vertices = np.vstack((m.x, m.y, m.z)).T
            # i, j, k = np.arange(0, len(vertices), 3), np.arange(1, len(vertices), 3), np.arange(2, len(vertices), 3)

            # fig = go.Figure(
            #     data=[
            #         go.Mesh3d(
            #             x=vertices[:, 0],
            #             y=vertices[:, 1],
            #             z=vertices[:, 2],
            #             i=i,
            #             j=j,
            #             k=k,
            #             color="orange",
            #             opacity=1.0,
            #             flatshading=True,
            #             lighting=dict(ambient=0.5, diffuse=0.9, roughness=0.3),
            #             lightposition=dict(x=0, y=0, z=1)
            #         )
            #     ]
            # )

            # fig.update_layout(
            #     scene=dict(
            #         aspectmode="data",
            #         xaxis=dict(visible=False),
            #         yaxis=dict(visible=False),
            #         zaxis=dict(visible=False),
            #         camera=dict(eye=dict(x=1.5, y=-1.5, z=1.5))
            #     ),
            #     margin=dict(l=0, r=0, t=0, b=0),
            #     paper_bgcolor="#0e1117",
            # )

            # st.plotly_chart(fig, use_container_width=True)
            
            
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



# import subprocess
# from solid2 import scad_render_to_file, text, linear_extrude
# from streamlit_stl import stl_from_file


# # === CONFIGURABLE PARAMETERS ===

# TEXT_STRING      = "Avery with Spaces"                # What to render
# FONT_NAME        = "Brush Script MT"      # Must be installed on your system
# TEXT_SIZE        = 20                     # Font size in mm
# TEXT_THICKNESS   = 5                      # Extrusion height (Z)
# OUTPUT_SCAD_PATH = "avery_text.scad"      # Output .scad file
# OUTPUT_STL_PATH  = "avery_text.stl"       # Output .stl file
# OPENSCAD_PATH    = "openscad"             # Command or full path to openscad.exe

# # Alignment & justification options (supported by OpenSCAD's text function)
# TEXT_HALIGN      = "center"               # 'left', 'center', or 'right'
# TEXT_VALIGN      = "baseline"             # 'top', 'center', 'bottom', 'baseline'

# # === STL GENERATION LOGIC ===

# def generate_text_stl(
#     text_str=TEXT_STRING,
#     font_name=FONT_NAME,
#     size=TEXT_SIZE,
#     thickness=TEXT_THICKNESS,
#     scad_path=OUTPUT_SCAD_PATH,
#     stl_path=OUTPUT_STL_PATH,
#     openscad_path=OPENSCAD_PATH,
#     halign=TEXT_HALIGN,
#     valign=TEXT_VALIGN
# ):
#     # Create extruded text
#     model = linear_extrude(height=thickness)(
#         text(text_str, font=font_name, size=size, halign=halign, valign=valign)
#     )

#     # Render to SCAD
#     scad_render_to_file(model, scad_path)

#     # Call OpenSCAD CLI to export STL
#     subprocess.run([openscad_path, "-o", stl_path, scad_path], check=True)

#     print(f"✅ Generated STL: {stl_path}")

# # # === Example ===
# # if __name__ == "__main__":
# #     generate_text_stl()



# success = stl_from_file(
#     file_path=path_to_conf,          # Path to the STL file
#     color='#FF9900',                 # Color of the STL file (hexadecimal value)
#     material='material',             # Material of the STL file ('material', 'flat', or 'wireframe')
#     auto_rotate=True,                # Enable auto-rotation of the STL model
#     opacity=1,                       # Opacity of the STL model (0 to 1)
#     shininess=100,                   # How shiny the specular highlight is, when using the 'material' style.
#     cam_v_angle=60,                  # Vertical angle (in degrees) of the camera
#     cam_h_angle=-90,                 # Horizontal angle (in degrees) of the camera
#     cam_distance=None,               # Distance of the camera from the object (defaults to 3x bounding box size)
#     height=500,                      # Height of the viewer frame
#     max_view_distance=1000,          # Maximum viewing distance for the camera
#     key=None                         # Streamlit component key
# )