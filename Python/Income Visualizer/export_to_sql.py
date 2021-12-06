x = """INSERT INTO
	[ScotiaTransactions]
(
	[Date],
	[Amount],
	[Notes],
	[Type],
	[Entity]
)
VALUES (
    {vals}
)"""

import csv
import datetime

with open("pcbanking.csv", "r") as f1, open("sql_output.txt", "w") as f2:
    lines = csv.DictReader(f1)
    m = "\n"
    for line in lines:
        date, amount, notes, ttype, entity = line.values()
        date = datetime.datetime.strptime(date, "%m/%d/%Y")
        date = datetime.datetime.strftime(date, "%Y-%m-%d")
        m += "\t(" + ", ".join([
            '\'' + date.replace('\'', '\'\'').strip() + '\'',
            amount,
            '\'' + notes.replace('\'', '\'\'').strip() + '\'',
            '\'' + ttype.replace('\'', '\'\'').strip() + '\'',
            '\'' + entity.replace('\'', '\'\'').strip() + '\''
        ]) + '),\n'
    m = m[:-2]
    print("m:", x.format(vals=m))
