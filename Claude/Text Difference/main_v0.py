import streamlit as st
import difflib

st.set_page_config(page_title="Text Diff Tool", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Syne:wght@400;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Syne', sans-serif;
    }

    .stApp {
        background: #0f0f12;
        color: #e8e6e0;
    }

    h1 {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 2.4rem;
        letter-spacing: -0.03em;
        color: #f0ece0;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        color: #6b6860;
        font-size: 0.95rem;
        margin-bottom: 2.5rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    .stTextArea label {
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 0.8rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #9b9790 !important;
    }

    .stTextArea textarea {
        background: #16161a !important;
        border: 1px solid #2a2a30 !important;
        border-radius: 8px !important;
        color: #e8e6e0 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem !important;
        line-height: 1.7 !important;
        transition: border-color 0.2s ease !important;
    }

    .stTextArea textarea:focus {
        border-color: #5a5aff !important;
        box-shadow: 0 0 0 2px rgba(90, 90, 255, 0.15) !important;
    }

    .stButton button {
        background: #5a5aff !important;
        color: white !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.6rem 2rem !important;
        transition: background 0.2s ease, transform 0.1s ease !important;
    }

    .stButton button:hover {
        background: #7070ff !important;
        transform: translateY(-1px) !important;
    }

    .stButton button:active {
        transform: translateY(0px) !important;
    }

    .diff-container {
        background: #16161a;
        border: 1px solid #2a2a30;
        border-radius: 10px;
        overflow: hidden;
        margin-top: 1.5rem;
    }

    .diff-header {
        background: #1c1c22;
        padding: 0.75rem 1.2rem;
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 0.78rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #6b6860;
        border-bottom: 1px solid #2a2a30;
        display: flex;
        gap: 1.5rem;
    }

    .diff-content {
        padding: 1rem 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.83rem;
        line-height: 1.8;
    }

    .diff-line {
        padding: 0.05rem 1.2rem;
        display: flex;
        gap: 1rem;
    }

    .diff-line-removed {
        background: rgba(255, 80, 80, 0.1);
        border-left: 3px solid #ff5050;
    }

    .diff-line-added {
        background: rgba(80, 200, 120, 0.1);
        border-left: 3px solid #50c878;
    }

    .diff-line-unchanged {
        border-left: 3px solid transparent;
    }

    .diff-marker {
        color: #6b6860;
        min-width: 1.2rem;
        user-select: none;
    }

    .diff-marker-removed { color: #ff5050; }
    .diff-marker-added { color: #50c878; }

    .diff-text-removed { color: #ff9090; }
    .diff-text-added { color: #90e0a8; }
    .diff-text-unchanged { color: #c8c4b8; }

    .stats-bar {
        display: flex;
        gap: 1.5rem;
        margin: 1rem 0 0.5rem 0;
        padding: 0.75rem 1rem;
        background: #16161a;
        border-radius: 8px;
        border: 1px solid #2a2a30;
    }

    .stat-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.82rem;
        font-family: 'JetBrains Mono', monospace;
    }

    .stat-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
    }

    .stat-dot-removed { background: #ff5050; }
    .stat-dot-added { background: #50c878; }
    .stat-dot-unchanged { background: #4a4a54; }

    .identical-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(80, 200, 120, 0.12);
        border: 1px solid rgba(80, 200, 120, 0.3);
        color: #50c878;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 0.85rem;
        letter-spacing: 0.05em;
        margin-top: 1rem;
    }

    .divider {
        height: 1px;
        background: linear-gradient(to right, transparent, #2a2a30, transparent);
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>Text Diff</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Compare two text snippets — line by line</p>', unsafe_allow_html=True)

# Side-by-side text areas
col1, col2 = st.columns(2)
with col1:
    text_a = st.text_area("Original", height=280, placeholder="Paste your original text here...")
with col2:
    text_b = st.text_area("Modified", height=280, placeholder="Paste your modified text here...")

# Submit button
_, btn_col, _ = st.columns([2, 1, 2])
with btn_col:
    compare = st.button("Compare →", use_container_width=True)

# Diff logic
if compare:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not text_a.strip() and not text_b.strip():
        st.warning("Please enter text in both fields.")
    else:
        lines_a = text_a.splitlines()
        lines_b = text_b.splitlines()

        matcher = difflib.SequenceMatcher(None, lines_a, lines_b)
        opcodes = matcher.get_opcodes()

        removed_count = 0
        added_count = 0
        unchanged_count = 0
        diff_lines_html = []

        for tag, i1, i2, j1, j2 in opcodes:
            if tag == "equal":
                for line in lines_a[i1:i2]:
                    unchanged_count += 1
                    diff_lines_html.append(
                        f'<div class="diff-line diff-line-unchanged">'
                        f'<span class="diff-marker"> </span>'
                        f'<span class="diff-text-unchanged">{line if line else "&nbsp;"}</span>'
                        f'</div>'
                    )
            elif tag in ("replace", "delete"):
                for line in lines_a[i1:i2]:
                    removed_count += 1
                    diff_lines_html.append(
                        f'<div class="diff-line diff-line-removed">'
                        f'<span class="diff-marker diff-marker-removed">−</span>'
                        f'<span class="diff-text-removed">{line if line else "&nbsp;"}</span>'
                        f'</div>'
                    )
                if tag == "replace":
                    for line in lines_b[j1:j2]:
                        added_count += 1
                        diff_lines_html.append(
                            f'<div class="diff-line diff-line-added">'
                            f'<span class="diff-marker diff-marker-added">+</span>'
                            f'<span class="diff-text-added">{line if line else "&nbsp;"}</span>'
                            f'</div>'
                        )
            elif tag == "insert":
                for line in lines_b[j1:j2]:
                    added_count += 1
                    diff_lines_html.append(
                        f'<div class="diff-line diff-line-added">'
                        f'<span class="diff-marker diff-marker-added">+</span>'
                        f'<span class="diff-text-added">{line if line else "&nbsp;"}</span>'
                        f'</div>'
                    )

        if removed_count == 0 and added_count == 0:
            st.markdown(
                '<div class="identical-badge">✓ &nbsp;Texts are identical</div>',
                unsafe_allow_html=True
            )
        else:
            # Stats bar
            similarity = round(matcher.ratio() * 100, 1)
            st.markdown(f"""
            <div class="stats-bar">
                <div class="stat-item">
                    <div class="stat-dot stat-dot-removed"></div>
                    <span style="color:#6b6860;">Removed:</span>
                    <span style="color:#ff9090;">{removed_count} line{"s" if removed_count != 1 else ""}</span>
                </div>
                <div class="stat-item">
                    <div class="stat-dot stat-dot-added"></div>
                    <span style="color:#6b6860;">Added:</span>
                    <span style="color:#90e0a8;">{added_count} line{"s" if added_count != 1 else ""}</span>
                </div>
                <div class="stat-item">
                    <div class="stat-dot stat-dot-unchanged"></div>
                    <span style="color:#6b6860;">Unchanged:</span>
                    <span style="color:#c8c4b8;">{unchanged_count} line{"s" if unchanged_count != 1 else ""}</span>
                </div>
                <div class="stat-item" style="margin-left:auto;">
                    <span style="color:#6b6860;">Similarity:</span>
                    <span style="color:#5a5aff;font-weight:600;">{similarity}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Diff output
            diff_body = "\n".join(diff_lines_html)
            st.markdown(f"""
            <div class="diff-container">
                <div class="diff-header">
                    <span style="color:#ff5050;">− removed</span>
                    <span style="color:#50c878;">+ added</span>
                    <span>· unchanged</span>
                </div>
                <div class="diff-content">
                    {diff_body}
                </div>
            </div>
            """, unsafe_allow_html=True)