file = 'words.txt'

read_file = open(file, 'r')

words_list = []
for line in read_file:
        words_list.append(read_file.readline().split('\n')[0].lower())
        
#for i in range(5):
	#print(words_list[i])
        
possible_words = []

# enter avaiable letters below
available_letters = list(set(['z','n','w','f','p','l',',i','y','t','p','e','e']))
special_chars = ['.', '-']
available_letters += special_chars
available_letters = [letter.lower() for letter in available_letters]

for word in words_list:
        if len(word) == 8 and word[0] == 'z':
                print('word:\t' + str(word))
        for letter in word:
                if str(letter).lower() not in available_letters:
                        break
                if word.index(letter) == len(word) -1:
                        possible_words.append(word)

print('\tPossible Words:')
for word in possible_words:
        print(word)
