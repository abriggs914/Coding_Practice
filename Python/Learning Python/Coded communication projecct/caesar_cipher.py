coded_message = "xuo jxuhu! jxyi yi qd unqcfbu ev q squiqh syfxuh. muhu oek qrbu je tusetu yj? y xefu ie! iudt cu q cuiiqwu rqsa myjx jxu iqcu evviuj!"
caesar_offset = 10
	
def is_upper(letter):
	return ord(letter) not in range(97, 123)

def caesar_cipher_decode(message, offset):
	decoded_message = ""
	offset %= 26
	for letter in message:
		if letter.isalpha():
			upper = is_upper(letter)
			letter = ord(letter) + offset
			if not str(chr(letter)).isalpha():
				letter -= 26
			if upper and chr(letter).islower():
				letter -= 26
			elif not upper and chr(letter).isupper():
				letter += 26
			letter = chr(letter)
		decoded_message += letter
	return decoded_message

def caesar_cipher_encode(message, offset):
	encoded_message = ""
	offset %= 26
	for letter in message:
		if letter.isalpha():
			upper = is_upper(letter)
			letter = ord(letter) - offset
			if not str(chr(letter)).isalpha():
				letter += 26
			if upper and chr(letter).islower():
				letter -= 26
			elif not upper and chr(letter).isupper():
				letter += 26
			letter = chr(letter)
		encoded_message += letter
	return encoded_message
    
print("\tEncoded message: \n" + str(coded_message))
print("\tDecoded message: \n" + str(caesar_cipher_decode(coded_message, caesar_offset)))
print("\tRecoded message: \n" + str(caesar_cipher_encode(caesar_cipher_decode(coded_message, caesar_offset), caesar_offset)))

message = "Hi Vishal!"
print(caesar_cipher_encode(message, caesar_offset))

unknown_message = "vhfinmxkl atox kxgwxkxw tee hy maxlx hew vbiaxkl tl hulhexmx. px'ee atox mh kxteer lmxi ni hnk ztfx by px ptgm mh dxxi hnk fxlltzxl ltyx."

def all_shifts_decode(message):
    for i in range(27):
        print(caesar_cipher_decode(message, i))
		
all_shifts_decode(unknown_message)
guessed_shift = 7
print(caesar_cipher_decode(unknown_message, guessed_shift))

print("\n\nVigenere:\n")

alphabet = {i: chr(i + 97) for i in range(26)}
#alphabet.update({i: chr(i + 65) for i in range(26)})
	
def encode_vigenere(message, key):
	c = 0
	encoded_message = ""
	message = message.lower()
	key = key.lower()
	for letter in message:
		if letter.isalpha():
			letter_val = ord(letter) - 97
			key_val = ord(key[c]) - 97
			print("letter_val (" + letter + "): " + str(letter_val) + ",\tkey_val (" + str(key[c]) + "): " + str(key_val) + ", \tsum(" + alphabet[(letter_val + key_val) % 26] + "): " + str((letter_val + key_val) % 26))
			encoded_message += alphabet[(letter_val + key_val) % 26]
			#encoded_message += alphabet[(letter_val + key_val) % 26] + ","
			c += 1
			if c == len(key):
				c %= len(key)
		else:
			encoded_message += letter
	return encoded_message
	

def decode_vigenere(message, key):
	c = 0
	decoded_message = ""
	message = message.lower()
	key = key.lower()
	for letter in message:
		if letter.isalpha():
			letter_val = ord(letter) - 97
			key_val = ord(key[c]) - 97
			print("letter_val (" + letter + "): " + str(letter_val) + ",\tkey_val (" + str(key[c]) + "): " + str(key_val) + ", \tsum(" + alphabet[(letter_val - key_val) % 26] + "): " + str((letter_val - key_val) % 26))
			decoded_message += alphabet[(letter_val - key_val) % 26]
			#decoded_message += alphabet[(letter_val + key_val) % 26] + ","
			c += 1
			if c == len(key):
				c %= len(key)
		else:
			decoded_message += letter
	return decoded_message
			
	
#soln = ""

vigenere_message = "barry is the spy"
vigenere_word = "dog"
soln = "eoxum ov hnh gvb"
valid_shifts = [4, 14, 15, 12, 16, 24, 11, 21, 25, 22, 22, 17, 5]

print(alphabet)
print("Vigenere message:\t" + vigenere_message)
ans = encode_vigenere(vigenere_message, vigenere_word)
print(vigenere_message + "\n" + ans + "\n" + soln)
print("Right? " + str(ans == soln))
print(encode_vigenere(soln, vigenere_word))


vigenere_message = "dfc aruw fsti gr vjtwhr wznj? vmph otis! cbx swv jipreneo uhllj kpi rahjib eg fjdkwkedhmp!"
vigenere_word = "friends"

print(decode_vigenere(vigenere_message, vigenere_word))

