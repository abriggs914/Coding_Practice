def ppd(price, days=None):
    i = 0
    days = days if days is not None else float("inf")
    while i < days:
        i += 1
        yield price / i
        

def avg_ppd(price, days):
    gen = list(ppd(price, days))
    if not gen:
        return 0
    return sum(gen) / len(gen)
        

def w_avg_ppd(price, days):
    gen = list(ppd(price, days))
    if not gen:
        return 0
    return sum(v * i for i, v in enumerate(gen)) / ((len(gen) * (len(gen) + 1)) / 2)
    
    
if __name__ == "__main__":
    
    gen_ppd_jr_21 = ppd(334)
    print(avg_ppd(334, 30))
    print(w_avg_ppd(334, 30))
    print(w_avg_ppd(334, 8))
    print(w_avg_ppd(334, 365))