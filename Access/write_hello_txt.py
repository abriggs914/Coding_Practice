import datetime
import os



#if __name__ == "__main__":
f = "hello.txt"
p2 = r"C:\Users\abrig\Documents\Coding_Practice\Access"
p3 = r"C:\Users\ABriggs\Documents\Coding Practice\Coding_Practice\Access"

p = p3 if os.path.isdir(p3) else p2

with open(f"{p}\{f}", "w") as f:
	now = datetime.datetime.now()
	f.write(f"Hello at {now:%Y-%m-%d %H:%M:%S}")
print(f"program over.")

input("hit enter to quit.")
		