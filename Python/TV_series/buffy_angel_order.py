import pandas as pd


fn = r"./buffy_angel_order.txt"
	
df_all = pd.DataFrame(columns=[
	# "Number",
	"Show",
	"Run",
	"Episode",
	"Year",
	"Rating"
])

with open(fn, "r") as f:
	lines = f.readlines()
	
	for i in range(0, len(lines), 4):
		title = lines[i]
		number_show_years = lines[i + 1]
		episode_year_rating = lines[i + 2]
		rate = lines[i + 3]
		
		# print(f"\n\t{title=}\n\t{number_show_years=}\n\t{episode_year_rating=}\n\t{rate=}")
		
		number, show_years = list(map(str.strip, number_show_years.split(".")))
		*show, years = list(map(str.strip, show_years.split(" ")))
		*episode, year_rating = list(map(str.strip, episode_year_rating.split(" ")))
		
		show = " ".join(show)
		ep, *episode = episode
		episode = " ".join(episode)
		year, rating = year_rating.split("\t")
		year = int(year.replace("(", "").replace(")", ""))
		rating = float(rating)

		print(f"{rating}")
		
		df_all.loc[-1] = (show, years, episode, year, rating)
		df_all.index = df_all.index + 1
	
	df_all = df_all.sort_index()
		
print(f"\n\t-- df_all --")
print(f"{df_all}")
print(f"\t-- end --\n")

buffy = "Buffy the Vampire Slayer"
angel = "Angel"

data = {
	"# Buffy Eps": (df_all.loc[df_all["Show"] == buffy]).count()[0],
	"# Angel Eps": (df_all.loc[df_all["Show"] == angel]).count()[0],
	"Avg Rating Buffy": f"{df_all.loc[df_all['Show'] == buffy, 'Rating'].mean():.3f}",
	"Avg Rating Angel": f"{df_all.loc[df_all['Show'] == angel, 'Rating'].mean():.3f}"
}

# average year and rating for each show.
df_a = df_all.groupby(["Show"]).mean()

# average rating and for each show for each year.
df_b = df_all.groupby(["Show", "Year"]).mean()

# top rated episode for each show for each year.
df_c = df_all.sort_values(["Rating"], ascending=[False]).groupby(["Show", "Year"]).head(1).sort_values(["Show", "Year"])

# same as df_c, except ordered columns
df_d = df_c[["Episode", "Show", "Year", "Rating"]]

print(f"{df_a}")
print(f"{df_b}")
print(f"{df_c}")
print(f"{df_d}")
print(f"{list(df_c.columns)}")

lk = max([len(str(k)) for k in data.keys()])
lv = max([len(str(v)) for v in data.values()])

print(f"\n\tStatistics:\n")

for k, v in data.items():
	print(f"{k.ljust(lk)} - {str(v).rjust(lv)}")
	