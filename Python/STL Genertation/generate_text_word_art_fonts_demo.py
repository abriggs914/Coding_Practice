import math
import os
import subprocess

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from matplotlib import font_manager
from solid2 import (
    scad_render_to_file,
    text,
    linear_extrude,
    rotate,
    translate,
    union,
    offset,
    multmatrix,
)
from stl import mesh


# =====================================
# HELPERS
# =====================================
def safe_filename(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in value.strip())
    return cleaned or "text_model"


def estimate_char_width(ch: str, size: float, spacing: float) -> float:
    """Rough width estimate in mm for per-character word-art placement.

    OpenSCAD text() does not expose exact glyph width, so this intentionally
    uses a practical approximation. It is good enough for decorative text,
    arching, and cylindrical/bottle-style wrapping.
    """
    if ch == " ":
        width_factor = 0.38
    elif ch in "il.,'|!":
        width_factor = 0.28
    elif ch in "mwMW@#%&":
        width_factor = 0.88
    elif ch.isupper():
        width_factor = 0.68
    else:
        width_factor = 0.56
    return size * width_factor * spacing


def make_text_2d(
    text_str: str,
    font_name: str,
    size: float,
    halign: str,
    valign: str,
    bold_amount: float,
):
    base = text(text_str, font=font_name, size=size, halign=halign, valign=valign)
    return offset(r=bold_amount)(base) if bold_amount > 0 else base


def italicize_2d(shape_2d, italic_degrees: float):
    """Shear the 2D text in X as Y increases, similar to italic text."""
    if abs(italic_degrees) < 0.01:
        return shape_2d

    shear = math.tan(math.radians(italic_degrees))
    return multmatrix(m=[[1, shear, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])(shape_2d)


def extruded_text(
    text_str: str,
    font_name: str,
    size: float,
    thickness: float,
    halign: str,
    valign: str,
    bold_amount: float,
    italic_degrees: float,
):
    shape_2d = make_text_2d(text_str, font_name, size, halign, valign, bold_amount)
    shape_2d = italicize_2d(shape_2d, italic_degrees)
    return linear_extrude(height=thickness)(shape_2d)


def layout_text_flat(
    text_str: str,
    font_name: str,
    size: float,
    thickness: float,
    halign: str,
    valign: str,
    bold_amount: float,
    italic_degrees: float,
    diagonal_degrees: float,
):
    model = extruded_text(text_str, font_name, size, thickness, halign, valign, bold_amount, italic_degrees)
    return rotate(a=[0, 0, diagonal_degrees])(model) if abs(diagonal_degrees) > 0.01 else model


def layout_text_arch(
    text_str: str,
    font_name: str,
    size: float,
    thickness: float,
    bold_amount: float,
    italic_degrees: float,
    arch_radius: float,
    arch_degrees: float,
    arch_flip: bool,
    spacing: float,
):
    chars = list(text_str)
    if not chars:
        return union()()

    widths = [estimate_char_width(ch, size, spacing) for ch in chars]
    total_width = sum(widths)
    radius = max(arch_radius, size)

    # Let the radius decide the natural arc, but cap it to the user's arc slider.
    natural_angle = math.degrees(total_width / radius)
    total_angle = min(abs(arch_degrees), natural_angle) if arch_degrees else natural_angle
    start_angle = -total_angle / 2
    direction = -1 if arch_flip else 1

    pieces = []
    travelled = 0.0
    for ch, width in zip(chars, widths):
        travelled += width / 2
        t = travelled / total_width if total_width else 0.5
        angle = start_angle + (t * total_angle)
        theta = math.radians(angle)

        x = radius * math.sin(theta)
        y = direction * radius * math.cos(theta)

        # Tangent angle keeps each letter upright along the curve.
        tangent_angle = -angle if arch_flip else angle
        if arch_flip:
            tangent_angle += 180

        letter = extruded_text(ch, font_name, size, thickness, "center", "center", bold_amount, italic_degrees)
        pieces.append(translate([x, y, 0])(rotate(a=[0, 0, tangent_angle])(letter)))
        travelled += width / 2

    return union()(*pieces)


def layout_text_cylindrical_wrap(
    text_str: str,
    font_name: str,
    size: float,
    thickness: float,
    bold_amount: float,
    italic_degrees: float,
    wrap_radius: float,
    wrap_degrees: float,
    spacing: float,
    inward: bool,
):
    """Approximate text wrapped around a cylinder/bottle.

    This places each character tangent to a cylinder. It does not physically bend
    each glyph mesh, but for names/labels it produces a usable curved text model.
    """
    chars = list(text_str)
    if not chars:
        return union()()

    radius = max(wrap_radius, size)
    widths = [estimate_char_width(ch, size, spacing) for ch in chars]
    total_width = sum(widths)
    natural_angle = math.degrees(total_width / radius)
    total_angle = min(abs(wrap_degrees), natural_angle) if wrap_degrees else natural_angle
    start_angle = -total_angle / 2

    pieces = []
    travelled = 0.0
    for ch, width in zip(chars, widths):
        travelled += width / 2
        t = travelled / total_width if total_width else 0.5
        angle = start_angle + (t * total_angle)

        letter = extruded_text(ch, font_name, size, thickness, "center", "center", bold_amount, italic_degrees)

        # Build around Z axis: X/Y are cylinder plane, Z is text extrusion height.
        # Rotate letter so its face is tangent to the cylinder.
        tangent = angle + (90 if not inward else -90)
        radial = rotate(a=[0, 0, tangent])(letter)
        radial = translate([radius, 0, 0])(radial)
        radial = rotate(a=[0, 0, angle])(radial)
        pieces.append(radial)
        travelled += width / 2

    return union()(*pieces)


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
    diagonal_degrees: float = 0.0,
    italic: bool = False,
    italic_degrees: float = 12.0,
    bold: bool = False,
    bold_amount: float = 0.0,
    layout_mode: str = "Flat",
    arch_radius: float = 80.0,
    arch_degrees: float = 120.0,
    arch_flip: bool = False,
    wrap_radius: float = 80.0,
    wrap_degrees: float = 120.0,
    wrap_inward: bool = False,
    character_spacing: float = 1.0,
):
    output_dir = os.path.abspath(".")
    scad_path = os.path.join(output_dir, "text_model.scad")
    stl_path = os.path.join(output_dir, "text_model.stl")

    final_italic_degrees = italic_degrees if italic else 0.0
    final_bold_amount = bold_amount if bold else 0.0

    if layout_mode == "Arch":
        model = layout_text_arch(
            text_str=text_str,
            font_name=font_name,
            size=size,
            thickness=thickness,
            bold_amount=final_bold_amount,
            italic_degrees=final_italic_degrees,
            arch_radius=arch_radius,
            arch_degrees=arch_degrees,
            arch_flip=arch_flip,
            spacing=character_spacing,
        )
    elif layout_mode == "Cylindrical wrap / bottle":
        model = layout_text_cylindrical_wrap(
            text_str=text_str,
            font_name=font_name,
            size=size,
            thickness=thickness,
            bold_amount=final_bold_amount,
            italic_degrees=final_italic_degrees,
            wrap_radius=wrap_radius,
            wrap_degrees=wrap_degrees,
            spacing=character_spacing,
            inward=wrap_inward,
        )
    else:
        model = layout_text_flat(
            text_str=text_str,
            font_name=font_name,
            size=size,
            thickness=thickness,
            halign=halign,
            valign=valign,
            bold_amount=final_bold_amount,
            italic_degrees=final_italic_degrees,
            diagonal_degrees=diagonal_degrees,
        )

    scad_render_to_file(model, scad_path)
    subprocess.run(["openscad", "-o", stl_path, scad_path], check=True)
    return stl_path


# =====================================
# STREAMLIT APP UI
# =====================================
st.set_page_config(page_title="3D Text Generator", page_icon="🔤", layout="wide")

st.title("🧱 3D Text → STL Generator")
st.caption("Generate 3D-printable word-art text with custom fonts, extrusion, bolding, italics, arching, diagonal rotation, and cylindrical/bottle-style wrapping.")

# Sidebar configuration
st.sidebar.header("⚙️ Parameters")

text_str = st.sidebar.text_input("Text to render", "Avery")

# Get a short list of nice, legible fonts — or all available TTFs
font_paths = font_manager.findSystemFonts(fontpaths=None, fontext="ttf")
font_names = sorted(set(font_manager.FontProperties(fname=fp).get_name() for fp in font_paths))
font_names = [f for f in font_names if f and f[0].isupper()]  # optional filter


# =====================================
# FONT DEMO BROWSER
# =====================================
page = st.radio("Mode", ["Generator", "Font Browser"], horizontal=True)

if not font_names:
    font_names = ["Liberation Sans", "Arial"]

if page == "Font Browser":
    cols = st.columns([1,3])
    with cols[0]:
        selected_font = st.selectbox("Jump to Font", font_names)
    with cols[1]:
        st.markdown("### Font Preview Gallery")
        for f in font_names:
            st.markdown(
                f'''
                <div style="font-family:{f}; font-size:32px; padding:8px;
                            border-bottom:1px solid #444;">
                    <b>{f}</b><span>
                    {text_str}
                </div>
                ''',
                unsafe_allow_html=True
            )
            
else:
    font_name = st.sidebar.selectbox(
        "Font name",
        options=font_names,
        index=font_names.index("Brush Script MT") if "Brush Script MT" in font_names else 0,
    )

    font_size = st.sidebar.slider("Font size (mm)", 5, 100, 20)
    thickness = st.sidebar.slider("Extrusion height (mm)", 1, 20, 3)

    st.sidebar.subheader("🎨 Word-art style")
    layout_mode = st.sidebar.radio("Layout mode", ["Flat", "Arch", "Cylindrical wrap / bottle"], index=0)

    bold = st.sidebar.checkbox("Bold / thicken strokes", value=False)
    bold_amount = st.sidebar.slider("Bold amount (mm)", 0.0, 5.0, 0.8, 0.1, disabled=not bold)

    italic = st.sidebar.checkbox("Italic / slant text", value=False)
    italic_degrees = st.sidebar.slider("Italic slant (degrees)", -30.0, 30.0, 12.0, 1.0, disabled=not italic)

    character_spacing = st.sidebar.slider("Character spacing", 0.60, 2.00, 1.00, 0.05)

    diagonal_degrees = 0.0
    arch_radius = 80.0
    arch_degrees = 120.0
    arch_flip = False
    wrap_radius = 80.0
    wrap_degrees = 120.0
    wrap_inward = False

    if layout_mode == "Flat":
        diagonal_degrees = st.sidebar.slider("Diagonal rotation (degrees)", -90.0, 90.0, 0.0, 1.0)
        halign = st.sidebar.selectbox("Horizontal alignment", ["left", "center", "right"], index=1)
        valign = st.sidebar.selectbox("Vertical alignment", ["baseline", "bottom", "center", "top"], index=0)
    else:
        # Per-character modes use centered letters for more predictable placement.
        halign = "center"
        valign = "center"

    if layout_mode == "Arch":
        arch_radius = st.sidebar.slider("Arch radius (mm)", 20.0, 300.0, 80.0, 5.0)
        arch_degrees = st.sidebar.slider("Maximum arch span (degrees)", 10.0, 360.0, 120.0, 5.0)
        arch_flip = st.sidebar.checkbox("Flip arch downward", value=False)

    if layout_mode == "Cylindrical wrap / bottle":
        wrap_radius = st.sidebar.slider("Cylinder/bottle radius (mm)", 10.0, 300.0, 80.0, 5.0)
        wrap_degrees = st.sidebar.slider("Maximum wrap span (degrees)", 10.0, 360.0, 120.0, 5.0)
        wrap_inward = st.sidebar.checkbox("Face inward instead of outward", value=False)
        st.sidebar.caption("This approximates bottle text by placing each character tangent to a cylinder. It does not mathematically bend each glyph mesh.")

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
                    diagonal_degrees=diagonal_degrees,
                    italic=italic,
                    italic_degrees=italic_degrees,
                    bold=bold,
                    bold_amount=bold_amount,
                    layout_mode=layout_mode,
                    arch_radius=arch_radius,
                    arch_degrees=arch_degrees,
                    arch_flip=arch_flip,
                    wrap_radius=wrap_radius,
                    wrap_degrees=wrap_degrees,
                    wrap_inward=wrap_inward,
                    character_spacing=character_spacing,
                )

                st.success("✅ STL Generated Successfully!")
                st.download_button(
                    "⬇️ Download STL",
                    data=open(stl_path, "rb").read(),
                    file_name=f"{safe_filename(text_str)}.stl",
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
                            lightposition=dict(x=0, y=1, z=1),
                        )
                    ]
                )

                fig.update_layout(
                    scene=dict(
                        aspectmode="data",
                        xaxis=dict(visible=False),
                        yaxis=dict(visible=False),
                        zaxis=dict(visible=False),
                        camera=dict(eye=dict(x=1.5, y=-1.5, z=1.5)),
                    ),
                    margin=dict(l=0, r=0, t=0, b=0),
                    paper_bgcolor="#0e1117",
                )

                st.plotly_chart(fig, use_container_width=True)

            except subprocess.CalledProcessError as e:
                st.error("❌ OpenSCAD failed to render STL. Make sure OpenSCAD is installed and in PATH.")
                st.exception(e)
            except Exception as e:
                st.error("❌ Failed to generate the STL.")
                st.exception(e)

    else:
        st.info("👈 Enter your text and click *Generate STL* to begin.")
