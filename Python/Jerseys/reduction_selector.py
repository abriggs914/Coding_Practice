
from nhl_utility import *
from utility import flatten
import random
import pandas as pd

teams = flatten([league[conf][div] for conf in league for div in league[conf]])
# df_teams = pd.DataFrame(data={"TeamName": teams})


class ReductionSelector:
	def __init__(self, original: list, n_per_choice: int = 3):
		self.original = original.copy()
		self.values = original.copy()
		self.n_per_choice = n_per_choice
		self.saved = []
		self.removed = []
		self.data = pd.DataFrame(data={"V": self.values})

	def start(self):
		while len(self.values) > 1:
			random.shuffle(self.values)
			rnd = 1 + len(self.original) - len(self.values)
			chx = self.values[-self.n_per_choice:]
			sel = input(f"\n#{rnd}\n\t{chx}\n\tPlease choose 1 to remove:\n\t\t").strip()

			for i, c in enumerate(chx):
				if sel.lower() == str(c).lower():
					sel = i
					break
				elif str(i) == sel:
					sel = i
					break

			if not isinstance(sel, int):
				if sel:
					sel = len(chx) - 1

			if isinstance(sel, int):
				self.removed.append(chx[sel])
				chx.pop(sel)
				self.values.pop((len(self.values) - self.n_per_choice) + sel)
			else:
				self.removed.append(None)

			self.saved.append(chx)
			
		print(f"\n\n\tFinal Selection:\n\t\t'{self.values[0]}'")
		print(f"Saved Freq")
		# save_freqs = []
		self.data["SaveFreq"] = 0
		for i, tn in enumerate(sorted(self.original.copy())):
			print(f"#{i+1} - {tn}", end=" ")
			n_appears = 0
			#n_appears = 1 if tn == rem else 0
			n_saved = 0
			for j, sv_lst in enumerate(self.saved):
				rem = self.removed[j]
				n_saved += int(bool(tn in sv_lst)) + int(bool(tn == rem))
			print(f"x{n_saved}")
			# save_freqs.append(n_saved)
			self.data.loc[self.data["V"] == tn, "SaveFreq"] = n_saved

		self.data.sort_values(by="SaveFreq", ascending=False, inplace=True)
		print(self.data)


if __name__ == "__main__":
	rs = ReductionSelector(teams)
	rs.start()
