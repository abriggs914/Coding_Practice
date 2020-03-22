#code
import random

valid_chars = []
for i in range(65, 91) :
    valid_chars.append(str(chr(i)))
    valid_chars.append(str(chr(i + 32)))
    
numbers = [str(i) or i in range(10)]
    
special_chars = [
    "(", ")", "[", "]", "{", "}", "~", "!", "@", "#", "$", "%", "^",
    "&", "*", "_", "+", "-", "=", ";", ":", "<", ">", "/", "?", "."]
    
valid_chars += numbers
valid_chars += special_chars
    
def check(min_num, lst, pass_word) :
    chars = []
    for c in lst :
        chars.append(c)
    if min_num == 0 :
        for c in chars :
            if c in pass_word :
                return False
    else :
        for i in range(min_num) :
            found = False
            for c in chars :
                if c in pass_word :
                    found = True
                    break
            if not found :
                return False
    return True
 
def get_pass(min_len, num_special, num_numbers, omit_chars=None) :
    chars = []
    for char in valid_chars :
        if omit_chars :
            if char in omit_chars :
                continue
        chars.append(char)
    pass_word = ""
    for i in range(min_len) :
        pass_word += random.choice(chars)
    
    while not (check(num_special, special_chars, pass_word) and check(num_numbers, numbers, pass_word)) :
        pass_word = get_pass(min_len, num_special, num_numbers, omit_chars)
    return pass_word
        
        
# print(valid_chars)
for i in range(100) :
    print(get_pass(12, 0, 0)) #, ["(", ")", "[", "]", "{", "}", "<", ">", "@", "%", "?", "="]))
    