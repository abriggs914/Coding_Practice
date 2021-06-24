import webbrowser

from pdf_writer import PDF, MARGIN_LINES_MARGIN, MARGIN_LINES_WIDTH, MAX_X, MAX_Y, random_test_set
from colour_utility import *

# Python program to read a csv and create a PDF of it's data

import csv
import datetime


class Line:
	def __init__(self, quote_date, wo, quote, price, model_no, width, spread):
		self.quote_date = datetime.datetime.strftime(datetime.datetime.strptime(quote_date[:10], "%Y-%m-%d"), "%Y-%m-%d")
		self.wo = wo
		self.quote = quote
		self.price = price
		self.model_no = model_no
		self.width = width
		self.spread = spread

	def csv_entry(self):
		return dict(zip(["WO#", "Q#", "$", "Name", "Width", "Spread"],
						[self.wo, self.quote, self.price, self.model_no, self.width, self.spread]))

	def __repr__(self):
		return "QD: {}, QO: {}, Q#: {}, P$: {}, MN: {}, W: {}, S: {}".format(self.quote_date, self.wo, self.quote,
																			 self.price, self.model_no, self.width,
																			 self.spread)



if __name__ == "__main__":
	data = {}
	FILE_NAME = "last_100_quotes.PDF"
	with open("random query data.csv", "r") as f:
		lines = csv.DictReader(f)
		for i, line in enumerate(lines):
			# for key, val in line.items():
			# print("key", key)
			entry = Line(*line.values())
			print(entry)
			if entry.quote_date not in data:
				data[entry.quote_date] = []
			data[entry.quote_date].append(entry.csv_entry())

	print("data:", data)

	TITLE_HEIGHT = 12
	TITLE_MARGIN = 15
	TABLE_MARGIN = 6
	FOOTER_MARGIN = 10
	TXT_MARGIN = 10
	ori = "P"

	if ori == "L":
		MAX_X, MAX_Y = MAX_Y, MAX_X

	pdf = PDF(FILE_NAME, orientation=ori, unit='mm', format='A4')
	pdf.set_auto_page_break(True, margin=5)
	pdf.set_title("Dealer Delivery Reports")
	pdf.set_author('Avery Briggs')
	pdf.add_page()

	# pdf.margin_lines(MARGIN_LINES_MARGIN, MARGIN_LINES_MARGIN, MAX_X - (2 * MARGIN_LINES_MARGIN),
	# 				 MAX_Y - (2 * MARGIN_LINES_MARGIN), BWS_RED, WHITE)
	pdf.margin_border(BWS_RED, WHITE)
	pdf.titles("Dealer Delivery Reports", MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN,
			   TITLE_MARGIN + MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN,
			   MAX_X - (2 * (MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN)), TITLE_HEIGHT, BWS_BLACK)

	# TABLE_X = 5 + MARGIN_LINES_WIDTH + TABLE_MARGIN
	# TABLE_Y = 10 + MARGIN_LINES_WIDTH + TABLE_MARGIN

	TABLE_W = (MAX_X - (2 * (MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN)) - (2 * TABLE_MARGIN))

	TABLE_X = TABLE_MARGIN + MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN
	TABLE_Y = TABLE_MARGIN + MARGIN_LINES_WIDTH + TITLE_HEIGHT + TITLE_MARGIN

	# TABLE_LEFT_MARGIN = 6
	TITLE_V_MARGIN = 5

	table1 = pdf.table(
		title="Last 100 Quotes",
		x=TABLE_X,
		y=TABLE_Y,
		w=TABLE_W,
		contents=data,
		desc_txt="Last 100 Quotes as of 2021-06-15",
		# contents=random_test_set(453),
		header_colours=[GRAY_30, BLACK],
		colours=[[WHITE, GRAY_69],
				 [BLACK]],
		show_row_names=True,
		include_top_doc_link=True,
		new_page_for_table=False,
		row_name_col_lbl="Date",
		start_with_header=True,
		cell_border_style=1,
		col_align={"Date": "L", "$": "R", "Name": "L"}
	)

	# date = datetime.datetime.now()
	# pdf.texts(
	# 	MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN + TXT_MARGIN,
	# 	TABLE_MARGIN + MARGIN_LINES_WIDTH + TITLE_HEIGHT + TITLE_MARGIN,
	# 	0,
	# 	10,
	# 	"Prepared at {} on {}".format(
	# 		datetime.datetime.strftime(date, "%I:%M:%S %p"),
	# 		datetime.datetime.strftime(date, "%Y-%m-%d")
	# 	),
	# 	font=('Arial', '', 10)
	# )

	pdf.time_stamp()
	pdf.output(FILE_NAME, 'F')
	webbrowser.open(FILE_NAME)
