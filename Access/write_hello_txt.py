import datetime



#if __name__ == "__main__":
p1 = "hello.txt"
p2 = r"C:\Users\abrig\Documents\Coding_Practice\Access\hello.txt"
with open(p2, "w") as f:
	now = datetime.datetime.now()
	f.write(f"Hello at {now:%Y-%m-%d %H:%M:%S}")
print(f"program over.")
		