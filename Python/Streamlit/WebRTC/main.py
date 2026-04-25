import time
import threading

import av
import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

st.set_page_config(layout="wide")
st.title("Live Webcam + Periodic Filtered Snapshots")

# ---------- Controls ----------
col_a, col_b, col_c = st.columns(3)

with col_a:
    filter_name = st.selectbox(
        "Filter",
        ["None", "Grayscale", "Canny", "Blur"]
    )

with col_b:
    mode = st.radio(
        "Mode",
        ["Live filter", "Periodic snapshots"],
        horizontal=True
    )

with col_c:
    interval_ms = st.slider(
        "Snapshot interval (ms)",
        min_value=100,
        max_value=3000,
        value=750,
        step=50,
    )

# Filter tuning sliders
if filter_name == "Blur":
    blur_k = st.slider("Blur strength", 1, 31, 11, 2)
elif filter_name == "Canny":
    canny_low = st.slider("Canny low threshold", 0, 255, 100)
    canny_high = st.slider("Canny high threshold", 0, 255, 200)
else:
    blur_k = 11
    canny_low = 100
    canny_high = 200


def apply_filter(img):
    if filter_name == "Grayscale":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    if filter_name == "Canny":
        edges = cv2.Canny(img, canny_low, canny_high)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    if filter_name == "Blur":
        k = blur_k if blur_k % 2 == 1 else blur_k + 1
        return cv2.GaussianBlur(img, (k, k), 0)

    return img


class Processor(VideoProcessorBase):
    def __init__(self):
        self.lock = threading.Lock()
        self.last_capture_ts = 0.0
        self.latest_original = None
        self.latest_filtered = None

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        original = img.copy()
        filtered = apply_filter(img)

        now = time.time()
        interval_s = interval_ms / 1000.0

        with self.lock:
            if now - self.last_capture_ts >= interval_s:
                self.latest_original = original.copy()
                self.latest_filtered = filtered.copy()
                self.last_capture_ts = now

        # Live side-by-side stream
        if mode == "Live filter":
            output = cv2.hconcat([original, filtered])
        else:
            # In snapshot mode, keep the live stream mostly original
            label_img = original.copy()
            cv2.putText(
                label_img,
                f"Snapshot every {interval_ms} ms",
                (15, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )
            output = cv2.hconcat([original, label_img])

        return av.VideoFrame.from_ndarray(output, format="bgr24")


ctx = webrtc_streamer(
    key="webcam-demo",
    video_processor_factory=Processor,
    media_stream_constraints={"video": True, "audio": False},
)

st.markdown("### Periodic snapshots")
snap_col1, snap_col2 = st.columns(2)
orig_placeholder = snap_col1.empty()
filt_placeholder = snap_col2.empty()

# Poll the processor for the most recent periodic capture
if ctx.state.playing:
    while ctx.state.playing:
        processor = ctx.video_processor
        if processor:
            with processor.lock:
                orig = processor.latest_original.copy() if processor.latest_original is not None else None
                filt = processor.latest_filtered.copy() if processor.latest_filtered is not None else None

            if orig is not None:
                orig_placeholder.image(
                    cv2.cvtColor(orig, cv2.COLOR_BGR2RGB),
                    caption="Original snapshot",
                    use_container_width=True,
                )
            if filt is not None:
                filt_placeholder.image(
                    cv2.cvtColor(filt, cv2.COLOR_BGR2RGB),
                    caption="Filtered snapshot",
                    use_container_width=True,
                )

        time.sleep(max(interval_ms / 1000.0, 0.1))

# import streamlit as st
# import cv2
# import av
# from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

# st.set_page_config(layout="wide")
# st.title("Live Webcam Filters")

# filter_name = st.selectbox(
#     "Choose a filter",
#     ["None", "Grayscale", "Canny", "Blur"]
# )

# class VideoProcessor(VideoProcessorBase):
#     def recv(self, frame):
#         img = frame.to_ndarray(format="bgr24")
#         original = img.copy()

#         if filter_name == "Grayscale":
#             processed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)

#         elif filter_name == "Canny":
#             edges = cv2.Canny(img, 100, 200)
#             processed = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

#         elif filter_name == "Blur":
#             processed = cv2.GaussianBlur(img, (21, 21), 0)

#         else:
#             processed = img

#         # Put original and filtered side by side
#         combined = cv2.hconcat([original, processed])

#         return av.VideoFrame.from_ndarray(combined, format="bgr24")

# webrtc_streamer(
#     key="side_by_side_webcam",
#     video_processor_factory=VideoProcessor,
#     media_stream_constraints={"video": True, "audio": False},
# )