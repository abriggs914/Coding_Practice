import utils
import sorts

bookshelf = utils.load_books('books_small.csv')
for book in bookshelf:
  print(book)

def by_title_ascending(book_a, book_b):
  return book_a['title_lower'] > book_b['title_lower'] 
  #if (book_a['title_lower'] > book_b['title_lower']):
  #  return True
  #return False
sort_1 = sorts.bubble_sort(bookshelf, by_title_ascending)
for book in sort_1:
  print(book['title'])
  
def by_author_ascending(book_a, book_b):
  return book_a['author_lower'] > book_b['author_lower']

def by_total_length(book_a, book_b):
  a = len(book_a['title_lower']) + len(book_a['author_lower'])
  b = len(book_b['title_lower']) + len(book_b['author_lower'])
  return a > b

bookshelf_v1 = bookshelf[:]

sort_2 = sorts.bubble_sort(bookshelf, by_author_ascending)
for book in sort_2:
  print(book['author'])

bookshelf_v2 = bookshelf[:]
sorts.quicksort(bookshelf_v2, 0, (len(bookshelf_v2)-1), by_author_ascending)
for book in bookshelf_v2:
  print(book['author'])
  
long_bookshelf = utils.load_books('books_large.csv')

#This one runs slowely because the list is mostly unsorted
sort_3 = sorts.bubble_sort(long_bookshelf, by_total_length)
print(sort_3)

sorts.quicksort(long_bookshelf, 0, len(long_bookshelf)-1, by_total_length)
print(long_bookshelf)
