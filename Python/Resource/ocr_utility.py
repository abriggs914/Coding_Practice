
import pandas as pd
import numpy as np

import cv2
import pytesseract
from pytesseract import Output

from itertools import groupby


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

VERSION = \
    """	
    General OCR Utility Functions for Pytesseract
    Version..............1.01
    Date...........2026-03-06
    Author(s)....Avery Briggs
    """


def VERSION_DETAILS():
    return VERSION.lower().split("version")[0].strip()


def VERSION_NUMBER():
    return float(".".join(VERSION.lower().split("version")[-1].split("date")[0].split(".")[-2:]).strip())


def VERSION_DATE():
    return datetime.datetime.strptime(VERSION.lower().split("date")[-1].split("author")[0].split(".")[-1].strip(),
                                      "%Y-%m-%dictionary")


def VERSION_AUTHORS():
    return [w.removeprefix(".").strip().title() for w in VERSION.lower().split("author(s)")[-1].split("..") if
            w.strip()]


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


pytesseract.pytesseract.tesseract_cmd = r"C:\Users\abriggs\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def clean_numeric(txt):
	txt = txt.replace("S", "5").replace("O", "0")
	txt = txt.replace("..", ".").replace(",", ".")
	txt = txt.replace("!", "|").replace("(", "|")
	txt = txt.replace(")", "|").replace("|", "")
	return txt


def combine_num_parts(num_txt):
	snt_splt = num_txt.split(" ")
	t_price_a = ""
	t_price_b = snt_splt[-1]
	# print(f"{txt=}, {snt_splt=}")
	if (len(snt_splt) > 2) and (snt_splt[-2].isnumeric()) and ("." not in snt_splt[-2]):
		t_price_a = snt_splt[-2]
	t_price = f"{t_price_a}{t_price_b}".strip()
	# print(f"    {t_price=}")
	return t_price

	# ----------------- Image utilities -----------------
def pil_to_cv(pil_img):
	arr = np.array(pil_img)
	if arr.ndim == 2:
		return arr
	return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)


def deskew(gray):
	# Compute rotation angle via minAreaRect on edges and rotate back
	edges = cv2.Canny(gray, 50, 150)
	coords = np.column_stack(np.where(edges > 0))
	if coords.size < 10:
		return gray  # nothing to skew-correct
	rect = cv2.minAreaRect(coords.astype(np.float32))
	angle = rect[-1]
	if angle < -45:
		angle = -(90 + angle)
	else:
		angle = -angle
	(h, w) = gray.shape[:2]
	M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
	return cv2.warpAffine(gray, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


def preprocess_for_ocr(cv_bgr, adaptive=True):
	# gray = cv2.cvtColor(cv_bgr, cv2.COLOR_BGR2GRAY)
	# gray = deskew(gray)
	# # Light denoise
	# gray = cv2.bilateralFilter(gray, 5, 40, 40)
	# if adaptive:
	# 	# bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 31, 12)
	# 	bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 25,10)
	# else:
	# 	_, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
	# return gray, bw
	gray = cv2.cvtColor(cv_bgr, cv2.COLOR_BGR2GRAY)
	gray = deskew(gray)
	gray = cv2.bilateralFilter(gray, 5, 40, 40)

	if adaptive:
		bw = cv2.adaptiveThreshold(
			gray, 255,
			cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
			27, 9
		)
	else:
		_, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

	# 🔍 Morph close + open to emphasize fine dots/lines
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
	bw = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel, iterations=1)
	bw = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel, iterations=1)

	return gray, bw


# ----------------- Table grid detection -----------------
def detect_table_cells(bw, min_line_len_frac=0.12, line_thickness=1):
	"""
	Detects table grid by morphological operations.
	Returns a list of cell boxes [(x, y, w, h), ...] sorted by rows then cols.
	"""
	h, w = bw.shape
	min_len = int(min(h, w) * min_line_len_frac)

	# Kernels for morphology
	horiz_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (max(10, w // 50), 2))
	vert_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, max(5, h // 20)))

	# Extract horizontal and vertical lines
	horiz = cv2.morphologyEx(bw, cv2.MORPH_OPEN, horiz_kernel, iterations=2)
	vert = cv2.morphologyEx(bw, cv2.MORPH_OPEN, vert_kernel, iterations=2)

	# # Keep only long lines
	# def filter_long_lines(img, axis=0):
	# 	cnts, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	# 	keep = np.zeros_like(img)
	# 	for c in cnts:
	# 		x, y, cw, ch = cv2.boundingRect(c)
	# 		ln = ch if axis == 0 else cw
	# 		if ln >= min_len:
	# 			cv2.drawContours(keep, [c], -1, 255, -1)
	# 	return keep
	#
	# horiz = filter_long_lines(horiz, axis=1)
	# vert = filter_long_lines(vert, axis=0)

	grid = cv2.bitwise_or(horiz, vert)

	# Intersections can help ensure real grid (optional)
	intersections = cv2.bitwise_and(horiz, vert)
	if intersections.sum() < 255 * 10:
		# Not enough grid structure
		return []

	# # Find boxes by looking at closed contours in the grid's inverted mask
	# # Create a mask where table cells (white areas bounded by lines) are blobs
	# table_mask = cv2.bitwise_not(grid)
	# # Slight closing to merge tiny gaps
	# table_mask = cv2.morphologyEx(table_mask, cv2.MORPH_CLOSE,
	# 							  cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), 1)


	footer_cutoff = int(h * 0.90)  # keep upper 90% of the page only
	bw_no_footer = bw[:footer_cutoff, :]  # crop binary image
	h, w = bw_no_footer.shape
	# recompute kernels and grid using bw_no_footer instead of bw
	horiz = cv2.morphologyEx(bw_no_footer, cv2.MORPH_OPEN, horiz_kernel, iterations=2)
	vert = cv2.morphologyEx(bw_no_footer, cv2.MORPH_OPEN, vert_kernel, iterations=2)
	grid = cv2.bitwise_or(horiz, vert)
	table_mask = cv2.bitwise_not(grid)

	cnts, _ = cv2.findContours(table_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	boxes = []
	for c in cnts:
		x, y, cw, ch = cv2.boundingRect(c)
		if cw > int(w * 0.999) and ch > int(h * 0.999):
			continue  # keep skipping full page only
		elif cw > int(w * 0.90):  # previously cropped wide cells
			boxes.append((x, y, cw, ch))
			continue
		boxes.append((x, y, cw, ch))

	if not boxes:
		return []

	# Cluster into rows (by y) then sort each row by x
	boxes = sorted(boxes, key=lambda b: (b[1], b[0]))
	rows = []
	y_tol = 12
	for k, group in groupby(boxes, key=lambda b: b[1]):
		row = list(group)
		if not rows:
			rows.append(row)
		else:
			# close to previous row? append; else new row
			if abs(rows[-1][0][1] - row[0][1]) <= y_tol:
				rows[-1].extend(row)
			else:
				rows.append(row)

	# Normalize each row order and reduce duplicates/overlaps
	cleaned = []
	for row in rows:
		row = sorted(row, key=lambda b: b[0])
		# remove overlapping duplicates
		keep = []
		for b in row:
			if not keep or b[0] >= keep[-1][0] + keep[-1][2] * 0.6:
				keep.append(b)
		if len(keep) >= 2:  # need at least 2 cells to be a row
			cleaned.append(keep)

	# Ensure rows have similar column counts; choose the modal count
	if not cleaned:
		return []
	counts = pd.Series([len(r) for r in cleaned])
	target_cols = counts.mode().iat[0]
	grid_cells = [r for r in cleaned if len(r) == target_cols]
	# Flatten back to list
	cells = [b for r in grid_cells for b in r]
	return cells, target_cols


# ----------------- OCR helpers -----------------
def preserve_decimals(gray):
	# Equalize contrast locally
	gray = cv2.convertScaleAbs(gray, alpha=1.4, beta=10)

	# Strengthen faint dots via morphological closing
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
	gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel, iterations=1)

	# Light adaptive threshold (keeps decimals visible)
	bw = cv2.adaptiveThreshold(
		gray, 255,
		cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
		35, 4
	)
	# Invert back to white background (Tesseract prefers dark text on white)
	return cv2.bitwise_not(bw)


def ocr_cell(image_bgr, psm=6, digits_only=False):
	# cfg = f"--oem 3 --psm {psm}"
	# if digits_only:
	# 	cfg += " -c tessedit_char_whitelist=0123456789.,-/"
	# txt = pytesseract.image_to_string(image_bgr, config=cfg)
	# return txt.strip()

	cfg_base = "--oem 3 --dpi 300 -c classify_bln_numeric_mode=1"
	psms = [7, 13, 6, 8]  # try single line, block, sparse text
	whitelist = "0123456789.,;:-/"
	if digits_only:
		cfg_base += f" -c tessedit_char_whitelist={whitelist}"

	min_len: int = 8
	txts = []
	for psm in psms:
		cfg = f"{cfg_base} --psm {psm}"
		roi_proc = preserve_decimals(cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY))
		txt = pytesseract.image_to_string(roi_proc, config=cfg).strip()
		# if "77" in txt:
		# 	print(f"TXT77: {txt=}, {psm=}, {cfg=}")

		if len(txt.replace(" ", "").strip()) >= min_len:
			txts.append(txt)
		else:
			txts.append("")

	# print(f"OCR_CELL:")
	# print(txts)
	return txts

def assemble_table_from_cells(cv_bgr, rows, cols, cells):
	"""Convert cell boxes to a DataFrame by OCRing each cell."""
	# Sort by row (top->down) and column (left->right)
	cells = sorted(cells, key=lambda b: (b[1], b[0]))
	# cluster into rows
	y_tol = 12
	grouped = []
	for b in cells:
		if not grouped:
			grouped.append([b])
		else:
			if abs(grouped[-1][0][1] - b[1]) <= y_tol:
				grouped[-1].append(b)
			else:
				grouped.append([b])
	# keep only rows with target count
	grouped = [sorted(r, key=lambda b: b[0]) for r in grouped if len(r) == cols]

	data = []
	off: int = 1
	for r in grouped:
		row_vals = []
		for (x, y, w, h) in r:
			roi = cv_bgr[max(0, y + off):y + h - off, max(0, x + off):x + w - off]
			roi = cv2.copyMakeBorder(roi, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=[255, 255, 255])
			# st.write(f"{r=}, {x=}, {y=}, {w=}, {h=}, {roi=}")
			row_vals.append("".join(ocr_cell(roi)))
		data.append(row_vals)
	if not data:
		return None
	df = pd.DataFrame(data)
	# Heuristic: first row often header
	if df.shape[0] >= 2:
		df.columns = [c if c else f"col{j}" for j, c in enumerate(df.iloc[0].tolist())]
		df = df.iloc[1:].reset_index(drop=True)
	return df


# ----------------- Fallback: word clustering table -----------------
def words_to_naive_table(cv_bgr, y_gap=14, x_gap=28):
	gray = cv2.cvtColor(cv_bgr, cv2.COLOR_BGR2GRAY)
	data = pytesseract.image_to_data(gray, output_type=Output.DATAFRAME, config="--oem 3 --psm 6")
	data = data.dropna(subset=["text"])
	if data.empty:
		return None
	# Build lines by y proximity
	lines = []
	for _, w in data.sort_values(["block_num", "par_num", "line_num", "left"]).iterrows():
		y = int(w["top"])
		placed = False
		for line in lines:
			if abs(line["y"] - y) <= y_gap:
				line["items"].append(w)
				placed = True
				break
		if not placed:
			lines.append({"y": y, "items": [w]})
	# Split each line into cells by x-gap
	table = []
	for line in sorted(lines, key=lambda d: d["y"]):
		items = sorted(line["items"], key=lambda r: int(r["left"]))
		if not items:
			continue
		cells, cur = [], [items[0]["text"]]
		for a, b in zip(items, items[1:]):
			gap = int(b["left"]) - (int(a["left"]) + int(a["width"]))
			if gap > x_gap:
				cells.append(" ".join(cur))
				cur = [b["text"]]
			else:
				cur.append(b["text"])
		cells.append(" ".join(cur))
		table.append(cells)
	if not table:
		return None
	n = max(map(len, table))
	table = [r + [""] * (n - len(r)) for r in table]
	return pd.DataFrame(table)


def rotate_cv(img, deg):
	deg = deg % 360
	if deg == 0:
		return img
	if deg == 90:
		return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
	if deg == 180:
		return cv2.rotate(img, cv2.ROTATE_180)
	if deg == 270:
		return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
	# arbitrary angle (rarely needed for invoices)
	h, w = img.shape[:2]
	M = cv2.getRotationMatrix2D((w // 2, h // 2), deg, 1.0)
	return cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def try_cast(v, type_: str = "str"):
	vs = str(v).replace(" ", "").strip()
	try:
		if type_.lower().strip() == "int":
			return int(vs)
		elif type_.lower().strip() == "float":
			return float(vs)
		else:
			return v
	except:
		return None