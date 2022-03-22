import datetime
from dateutil.relativedelta import relativedelta


"""
	General datetime Utility Functions
	Version...............1.1
	Date...........2022-03-22
	Author.......Avery Briggs
"""


class datetime2(datetime.datetime):

	def __init__(self, *args, **kwargs):
		super().__init__()

	def add_month(self, n_months=1):
		return self + relativedelta(months=n_months)


if __name__ == '__main__':
	d2 = datetime.datetime(2022, 10, 10)
	d1 = datetime2(2022, 10, 10, 23, 48, 12)
	print("d1:", d1)
	print("d1 + M:", d1.add_month(3))