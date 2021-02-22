import random as rand
from utility import *

def random_money(low, high):
	return low + (rand.random() * (high - low))
	
def gen_cash_payment(price):
	hundreds = price // 100
	fifties = (price - (hundreds * 100)) // 50
	twenties = (price - (hundreds * 100) - (fifties * 50)) // 20
	tens = (price - (hundreds * 100) - (fifties * 50) - (twenties * 20)) // 10
	fives = (price - (hundreds * 100) - (fifties * 50) - (twenties * 20) - (tens * 10)) // 5
	twoonies = (price - (hundreds * 100) - (fifties * 50) - (twenties * 20) - (tens * 10) - (fives * 5)) // 2
	loonies = (price - (hundreds * 100) - (fifties * 50) - (twenties * 20) - (tens * 10) - (fives * 5) - (twoonies * 2)) // 1
	quarters = (price - (hundreds * 100) - (fifties * 50) - (twenties * 20) - (tens * 10) - (fives * 5) - (twoonies * 2) - loonies) // 0.25
	dimes = (price - (hundreds * 100) - (fifties * 50) - (twenties * 20) - (tens * 10) - (fives * 5) - (twoonies * 2) - loonies - (quarters * 0.25)) // 0.1
	nickels = (price - (hundreds * 100) - (fifties * 50) - (twenties * 20) - (tens * 10) - (fives * 5) - (twoonies * 2) - loonies - (quarters * 0.25) - (dimes * 0.1)) // 0.05
		
	diff = round(100 * (price - (hundreds * 100) - (fifties * 50) - (twenties * 20) - (tens * 10) - (fives * 5) - (twoonies * 2) - loonies - (quarters * 0.25) - (dimes * 0.1) - (nickels * 0.05)))
	# print("diff: {d}".format(d=diff))
	
	if diff > 2:
		nickels += 1
	
	payment = {
		"Hundreds": hundreds,
		"Fifties": fifties,
		"Twenties": twenties,
		"Tens": tens,
		"Fives": fives,
		"Twoonies": twoonies,
		"Loonies": loonies,
		"Quarters": quarters,
		"Dimes": dimes,
		"Nickels": nickels
	}
	return payment
	
def count_change(p):
	return (p["Hundreds"] * 100) + (p["Fifties"] * 50) + (p["Twenties"] * 20) + (p["Tens"] * 10) + (p["Fives"] * 5) + (p["Twoonies"] * 2) + (p["Loonies"]) + (p["Quarters"] * 0.25) + (p["Dimes"] * 0.1) + (p["Nickels"] * 0.05)

if __name__ == "__main__":
	
	# gen random price.
	# gen randomish payment
	# see who beneifts from the transaction
	
	# price = random_money(10, 20)
	# print(price)
	# print(money(price))
	# payment = gen_cash_payment(price)
	# print(dict_print(payment, "Payment"))
	# print("Counted Payment: {m}".format(m=money(count_change(payment))))
	
	
	n_transactions = 100
	n_runs = 100
	low, high = 50, 100
	
	res = {}
	
	for i in range(n_runs):
		buyer_balance, seller_balance = 0, 0
		buyer_history, seller_history = [], []
		for j in range(n_transactions):
			price = random_money(low, high)
			payment = count_change(gen_cash_payment(price))
			diff = round(100 * (price - payment)) / 100
			# print("diff: " + str(diff))
			buyer_diff = diff if diff != 0 else 0
			seller_diff = (-1 * diff) if diff != 0 else 0
			# if diff > 0:
				# buyer_diff = diff
				# seller_diff = -1 * diff
			# elif diff < 0:
				# buyer_diff = diff
				# seller_diff = -1 * diff
			# else:
				# buyer_diff = 0
				# seller_diff = 0
			
			# print(money(price))
			# print(money(payment))
			# print(money(diff/100))
			# print(money(buyer_diff))
			# print(money(seller_diff))
			
			buyer_history.append(buyer_diff)
			buyer_balance += buyer_diff
			seller_history.append(seller_diff)
			seller_balance += seller_diff
		# print("BB: {bb}, SB: {sb}".format(bb=buyer_balance, sb=seller_balance))
			
		run = {
			"Buyer Balance": money(buyer_balance),
			"Seller Balance": money(seller_balance)
			# "Buyer Balance: ": "".join(["a" for q in range(120)]),
			# "Seller Balance: ": "b"
			# "Buyer History ": buyer_history,
			# "Seller History ": seller_history,
		}
		res["Run " + str(i+1)] = run
		
	
	buyer_balance, seller_balance = 0, 0
	for run, data in res.items():
		buyer_balance += float(data["Buyer Balance"][1:].strip())
		seller_balance += float(data["Seller Balance"][1:].strip())
	final_tally = {
			"Buyer Balance": money(buyer_balance),
			"Seller Balance": money(seller_balance)
			# "Buyer Balance: ": "".join(["a" for q in range(120)]),
			# "Seller Balance: ": "b"
			# "Buyer History ": buyer_history,
			# "Seller History ": seller_history,
		}
	
	print(dict_print(res, "Res"))
	print("Res: " + str(res))
	print(dict_print(final_tally, "Final Tally"))
	
	
	
	# for i in [(10, 9.99), (10, 10), (10, 10.01)]:
		# print("\n\n")
		# price = i[0]
		# payment = i[1]
		# diff = price - (payment)
		# if diff > 0:
			# buyer_diff = diff
			# seller_diff = -1 * diff
		# elif diff < 0:
			# buyer_diff = diff
			# seller_diff = -1 * diff
		# else:
			# buyer_diff = 0
			# seller_diff = 0
		# print(money(price))
		# print(money((payment)))
		# print(money(diff/100))
		# print(money(buyer_diff))
		# print(money(seller_diff))
		
		# buyer_history.append(buyer_diff)
		# buyer_balance += buyer_diff
		# seller_history.append(seller_diff)
		# seller_balance += seller_diff
		
		
