import datetime
import random


def select_remaining_games(data: dict) -> dict:
	w_data = {k: ([v_ for v_ in v] if hasattr(v, "__iter__") else v) for k, v in data.items()}
	print(f"{w_data=}")

	def brute_selector(lst, max_seq_tries=10, max_reruns=100):

		if max_reruns <= 0:
			raise ValueError("Error cannot rerun this anymore.")

		w_lst = [v for v in lst]
		choices = set()
		last_tried = [None, 0]
		failure = ""
		while w_lst:
			a = random.choice(w_lst)
			len_ = len(w_lst)
			w_lst.remove(a)
			# print(f"{a=}")
			if len_ >= 2:
				b = random.choice(w_lst)
				tup = a, b
				if a != b and (tup not in choices):
					choices.add(tup)
					w_lst.remove(b)
				else:
					if last_tried[0] == tup:
						last_tried[1] += 1
					else:
						last_tried = [tup, 1]

					w_lst.append(a)

				if last_tried[1] >= max_seq_tries:
					failure = f"times exceeded trying {tup=}"
					print(f"{max_reruns=}, {tup=}, {failure=}, {w_lst=}, lc={len(choices)}, {choices=}")

				# print(f"{w_lst=}")

			else:
				failure = f"List too small {len_=}"
				print(f"{max_reruns=}, {a=}, {failure=}, {w_lst=}, lc={len(choices)}, {choices=}")

			if failure:
				return brute_selector(lst, max_seq_tries=max_seq_tries, max_reruns=max_reruns-1)

		return list(choices)

	c_data = {}
	for k, v in w_data.items():
		c_data[k] = brute_selector(v)

	return c_data
	# try:
	# except ValueError:



	# # for d in divs[same_div]:
	# #	lo = [t for t in d for i in range(5)]
	# #	for t1 in d:
	# cho = set()
	# i = 0
	# while (len(cho) < 5) and inter_divs_left_over[same_div]:
	# 	i += 1
	# 	# ct = random.choice(inter_divs_left_over[same_div])
	# 	print(f"{([t1] + list(cho))=}")
	# 	print(f"{inter_divs_left_over[same_div][0]=}, {inter_divs_left_over[same_div]=}")
	# 	print(f"{[t2 for t2 in inter_divs_left_over[same_div] if t2 not in ([t1] + list(cho))]=}")
	# 	# ct = inter_divs_left_over[same_div][0] if (t1 != inter_divs_left_over[same_div][0]) else [t2 for t2 in inter_divs_left_over[same_div] if t2 not in ([t1] + list(cho))][0]
	# 	ct = [t2 for t2 in inter_divs_left_over[same_div] if t2 not in ([t1] + list(cho))][0]
	# 	print(f"{t1=}, {ct=}")
	# 	if (ct != t1) and (ct not in cho):
	# 		# min_t, max_t = inter_divs_counts[same_div][inter_divs_left_over[same_div][0]], inter_divs_counts[same_div][inter_divs_left_over[same_div][-1]]
	# 		# print(f"{min_t=}, {max_t=}, {inter_divs_left_over[same_div]=}")
	# 		# if abs(min_t - max_t) > 1:
	# 		# 	ct = inter_divs_left_over[same_div][0] if (t1 != inter_divs_left_over[same_div][0]) else [t2 for t2 in inter_divs_left_over[same_div] if t2 not in [[t1] + list(cho)]][0]
	# 		print(f"{i=}")
	# 		cho.add(ct)
	# 		inter_divs_left_over[same_div].remove(ct)
	# 		inter_divs_left_over[same_div].sort(key=lambda d: inter_divs_counts[same_div][d])
	# 	curr_time = datetime.datetime.now()
	#
	# 	if (curr_time - start_time).total_seconds() > total_allowed_time:
	# 		raise ValueError(
	# 			f"Timeout\n\t{i=}\n\t{t1=}\n\t{same_div=}\n\t{cho=}\n\t{inter_divs_left_over[same_div]=}\n\t{inter_divs_left_over=}\n\t{sched=}\n\t{inter_divs_counts[same_div]=}\n\t{inter_divs_counts=}")
	#
	# # inter_divs_left_over[same_div].remove(t1)
	# sched[t1] += list(cho)
	# # inter_divs_counts[same_div][t1] += (5 / 2)
	# for t2 in cho:
	# 	inter_divs_counts[same_div][t2] += 1  # (1 / 2)
	# print(f"INTER-DIV {t1=}, div={same_div}, {cho=}")
	#
	# print(f"{inter_divs_left_over=}")



if __name__ == "__main__":

	teams = list(map(lambda x: chr(x), range(97, 97+26)))
	teams = list(map(lambda x: chr(x), range(97, 97+26))) + list(map(str, range(6)))

	divs = {"a": teams[:8], "m": teams[8: 16], "c": teams[16:24], "p": teams[24:]}
	confs = {"e": ["a", "m"], "w": ["c", "p"]}

	sched = {}
	games = []
	
	inter_divs_left_over = {d: [t for t in d_teams for i in range(5)] for d, d_teams in divs.items()}
	#inter_divs_counts = {d: {t: 0 for t in d_teams for i in range(8)} for d, d_teams in divs.items()}
	inter_divs_counts = {d: {t: 0 for t in div_teams} for d, div_teams in inter_divs_left_over.items()}
	
	print(f"{inter_divs_left_over=}")
	
	total_allowed_time = 10
	start_time = datetime.datetime.now()
	curr_time = datetime.datetime.now()

	jj = [0, 0, 0]
	
	for t1 in teams:
		same_div = [k for k, v in divs.items() if t1 in v][0]		
		other_div = [[d_ for d_ in cs if same_div != d_][0] for k, cs in confs.items() if same_div in cs][0]
		same_conf = [c for c, ds in confs.items() if same_div in ds][0]
		other_conf = [c for c, ds in confs.items() if same_div not in ds][0]
		# print(f"{same_div=}, {other_div=}, {same_conf=}, {other_conf=}")  
	
		if t1 not in sched:
			sched[t1] = []
			
		# add 1 home and away game for each team.
		# 31 other teams * 2 = 62 games | 62 games Total
		for i in range(2):
			for t2 in teams:
				if t1 != t2:
					sched[t1].append(t2)
					jj[0] += 1

		print(f"A {jj=}")

		# add 1 game for each inter-conference team.
		# 15 other teams * 1 = 15 games | 77 games Total
		sched[t1] += [t for t in [[t for t in [c1 + c2]] for c1, c2 in [[t for t in [divs[d_] for d_ in d]] for c, d in confs.items() if (c == "e")]][0][0] if t != t1]
		jj[1] += 15
		print(f"B {jj=}")
		
		# add 1 game for 5 inter-division teams
		# 5 other games * 1 = 5 games | 82 games total

		v2024_01_24_2033 = """
		#for d in divs[same_div]:
		#	lo = [t for t in d for i in range(5)]
		#	for t1 in d:
		cho = set()
		i = 0
		while (len(cho) < 5) and inter_divs_left_over[same_div]:
			i += 1
			# ct = random.choice(inter_divs_left_over[same_div])
			print(f"{([t1] + list(cho))=}")
			print(f"{inter_divs_left_over[same_div][0]=}, {inter_divs_left_over[same_div]=}")
			print(f"{[t2 for t2 in inter_divs_left_over[same_div] if t2 not in ([t1] + list(cho))]=}")
			# ct = inter_divs_left_over[same_div][0] if (t1 != inter_divs_left_over[same_div][0]) else [t2 for t2 in inter_divs_left_over[same_div] if t2 not in ([t1] + list(cho))][0]
			ct = [t2 for t2 in inter_divs_left_over[same_div] if t2 not in ([t1] + list(cho))][0]
			print(f"{t1=}, {ct=}")
			if (ct != t1) and (ct not in cho):
				# min_t, max_t = inter_divs_counts[same_div][inter_divs_left_over[same_div][0]], inter_divs_counts[same_div][inter_divs_left_over[same_div][-1]]
				# print(f"{min_t=}, {max_t=}, {inter_divs_left_over[same_div]=}")
				# if abs(min_t - max_t) > 1:
				# 	ct = inter_divs_left_over[same_div][0] if (t1 != inter_divs_left_over[same_div][0]) else [t2 for t2 in inter_divs_left_over[same_div] if t2 not in [[t1] + list(cho)]][0]
				print(f"{i=}")
				cho.add(ct)
				inter_divs_left_over[same_div].remove(ct)
				inter_divs_left_over[same_div].sort(key=lambda d: inter_divs_counts[same_div][d])
			curr_time = datetime.datetime.now()
			
			if (curr_time - start_time).total_seconds() > total_allowed_time:
				raise ValueError(f"Timeout\n\t{i=}\n\t{t1=}\n\t{same_div=}\n\t{cho=}\n\t{inter_divs_left_over[same_div]=}\n\t{inter_divs_left_over=}\n\t{sched=}\n\t{inter_divs_counts[same_div]=}\n\t{inter_divs_counts=}")
		
		# inter_divs_left_over[same_div].remove(t1)
		sched[t1] += list(cho)
		# inter_divs_counts[same_div][t1] += (5 / 2)
		for t2 in cho:
			inter_divs_counts[same_div][t2] += 1  #  (1 / 2)
		print(f"INTER-DIV {t1=}, div={same_div}, {cho=}")
		
		print(f"{inter_divs_left_over=}")
		
	"""

	remaining_games = select_remaining_games(inter_divs_left_over)
	print(f"AAA")
	for div, games_ in remaining_games.items():
		for t1_t2 in games_:
			t1, t2 = t1_t2
			games.append(t1_t2)
			sched[t1].append(t2)
			sched[t2].append(t1)
			jj[2] += 2

	print(f"{len(sched['a'])=}")
	print(f"{sched=}")
	print(f"{remaining_games=}")
	print(f"{len(games)=}")
	print(f"{games=}")
	print(f"{jj=}")
