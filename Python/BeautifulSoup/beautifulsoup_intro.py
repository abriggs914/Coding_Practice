#WEB SCRAPING WITH BEAUTIFUL SOUP
# Rules of Scraping
# When we scrape websites, we have to make sure we are following some guidelines so that we are treating the websites and their owners with respect.
# Always check a website’s Terms and Conditions before scraping. Read the statement on the legal use of data. Usually, the data you scrape should not be used for commercial purposes.
# Do not spam the website with a ton of requests. A large number of requests can break a website that is unprepared for that level of traffic. As a general rule of good practice, make one request to one webpage per second.
# If the layout of the website changes, you will have to change your scraping code to follow the new structure of the site.

# WEB SCRAPING WITH BEAUTIFUL SOUP
# Requests
# In order to get the HTML of the website, we need to make a request to get the content of the webpage. To learn more about requests in a general sense, you can check out this article.
# https://www.codecademy.com/articles/http-requests

# Python has a requests library that makes getting content really easy. All we have to do is import the library, and then feed in the URL we want to GET:

# import requests

# webpage = requests.get('https://www.codecademy.com/articles/http-requests')
# print(webpage.text)
# This code will print out the HTML of the page.

# We don’t want to unleash a bunch of requests on any one website in this lesson, so for the rest of this lesson we will be scraping a local HTML file and pretending it’s an HTML file hosted online.

#Import the requests library.
import requests

#Make a GET request to the URL containing the turtle adoption website:
#https://s3.amazonaws.com/codecademy-content/courses/beautifulsoup/shellter.html
#Store the result of your request in a variable called webpage_response.
url = 'https://s3.amazonaws.com/codecademy-content/courses/beautifulsoup/shellter.html'
webpage_response = requests.get(url)
print(webpage_response)

#Store the content of the response in a variable called webpage by using .content.
#Print webpage out to see the content of this HTML.
webpage = webpage_response.content
print(webpage)

#---------------------------------------------------------------------------------------------------------------------------------------------------------

#import requests

#WEB SCRAPING WITH BEAUTIFUL SOUP
# The BeautifulSoup Object
# When we printed out all of that HTML from our request, it seemed pretty long and messy. How could we pull out the relevant information from that long string?
# BeautifulSoup is a Python library that makes it easy for us to traverse an HTML page and pull out the parts we’re interested in. We can import it by using the line:
# from bs4 import BeautifulSoup
# Then, all we have to do is convert the HTML document to a BeautifulSoup object!
# If this is our HTML file, rainbow.html:
# <body>
#   <div>red</div>
#   <div>orange</div>
#   <div>yellow</div>
#   <div>green</div>
#   <div>blue</div>
#   <div>indigo</div>
#   <div>violet</div>
# </body>
# soup = BeautifulSoup("rainbow.html", "html.parser")
# "html.parser" is one option for parsers we could use. There are other options, like "lxml" and "html5lib" that have different advantages and disadvantages, but for our purposes we will be using "html.parser" throughout.
# With the requests skills we just learned, we can use a website hosted online as that HTML:
# webpage = requests.get("http://rainbow.com/rainbow.html", "html.parser")
# soup = BeautifulSoup(webpage.content)
# When we use BeautifulSoup in combination with pandas, we can turn websites into DataFrames that are easy to manipulate and gain insights from.

#webpage_response = requests.get('https://s3.amazonaws.com/codecademy-content/courses/beautifulsoup/shellter.html')

#webpage = webpage_response.content

#Import the BeautifulSoup package.
from bs4 import BeautifulSoup

#Create a BeautifulSoup object out of the webpage content and call it soup. Use "html.parser" as the parser.
#Print out soup! Look at how it contains all of the HTML of the page! We will learn how to traverse this content and find what we need in the next exercises.
soup = BeautifulSoup(webpage, "html.parser")
print(soup)

#---------------------------------------------------------------------------------------------------------------------------------------------------------

#import requests
#from bs4 import BeautifulSoup

#WEB SCRAPING WITH BEAUTIFUL SOUP
# Object Types
# BeautifulSoup breaks the HTML page into several types of objects.
# Tags
# A Tag corresponds to an HTML Tag in the original document. These lines of code:
# soup = BeautifulSoup('<div id="example">An example div</div><p>An example p tag</p>')
# print(soup.div)
# Would produce output that looks like:
# <div id="example">An example div</div>
# Accessing a tag from the BeautifulSoup object in this way will get the first tag of that type on the page.
# You can get the name of the tag using .name and a dictionary representing the attributes of the tag using .attrs:
# print(soup.div.name)
# print(soup.div.attrs)
# div
# {'id': 'example'}
# NavigableStrings
# NavigableStrings are the pieces of text that are in the HTML tags on the page. You can get the string inside of the tag by calling .string:
# print(soup.div.string)
# An example div

#webpage_response = requests.get('https://s3.amazonaws.com/codecademy-content/courses/beautifulsoup/shellter.html')

#webpage = webpage_response.content
#soup = BeautifulSoup(webpage, "html.parser")
#Print out the first p tag on the shellter.html page.
print(soup.p)

#Print out the string associated with the first p tag on the shellter.html page.
print(soup.p.string)

#---------------------------------------------------------------------------------------------------------------------------------------------------------

#import requests
#from bs4 import BeautifulSoup

#WEB SCRAPING WITH BEAUTIFUL SOUP
# Navigating by Tags
# To navigate through a tree, we can call the tag names themselves. Imagine we have an HTML page that looks like this:
# <h1>World's Best Chocolate Chip Cookies</h1>
# <div class="banner">
#   <h1>Ingredients</h1>
# </div>
# <ul>
#   <li> 1 cup flour </li>
#   <li> 1/2 cup sugar </li>
#   <li> 2 tbsp oil </li>
#   <li> 1/2 tsp baking soda </li>
#   <li> ½ cup chocolate chips </li> 
#   <li> 1/2 tsp vanilla <li>
#   <li> 2 tbsp milk </li>
# </ul>
# If we made a soup object out of this HTML page, we have seen that we can get the first h1 element by calling:
# print(soup.h1)
# <h1>World's Best Chocolate Chip Cookies</h1>
# We can get the children of a tag by accessing the .children attribute:
# for child in soup.ul.children:
#     print(child)
# <li> 1 cup flour </li>
# <li> 1/2 cup sugar </li>
# <li> 2 tbsp oil </li>
# <li> 1/2 tsp baking soda </li>
# <li> ½ cup chocolate chips </li> 
# <li> 1/2 tsp vanilla <li>
# <li> 2 tbsp milk </li>
# We can also navigate up the tree of a tag by accessing the .parents attribute:
# for parent in soup.li.parents:
#     print(parent)
# This loop will first print:
# <ul>
# <li> 1 cup flour </li>
# <li> 1/2 cup sugar </li>
# <li> 2 tbsp oil </li>
# <li> 1/2 tsp baking soda </li>
# <li> ½ cup chocolate chips </li>
# <li> 1/2 tsp vanilla </li>
# <li> 2 tbsp milk </li>
# </ul>
# Then, it will print the tag that contains the ul (so, the body tag of the document). Then, it will print the tag that contains the body tag (so, the html tag of the document).

#webpage_response = requests.get('https://s3.amazonaws.com/codecademy-content/courses/beautifulsoup/shellter.html')

#webpage = webpage_response.content
#soup = BeautifulSoup(webpage, "html.parser")

#Loop through all of the children of the first div and print out each one.
for children in soup.div:
  print(children)

#---------------------------------------------------------------------------------------------------------------------------------------------------------

#import requests
#from bs4 import BeautifulSoup

#WEB SCRAPING WITH BEAUTIFUL SOUP
# Find All
# If we want to find all of the occurrences of a tag, instead of just the first one, we can use .find_all().

# This function can take in just the name of a tag and returns a list of all occurrences of that tag.

# print(soup.find_all("h1"))
# ['<h1>World's Best Chocolate Chip Cookies</h1>', '<h1>Ingredients</h1>']
# .find_all() is far more flexible than just accessing elements directly through the soup object. With .find_all(), we can use regexes, attributes, or even functions to select HTML elements more intelligently.

# Using Regex
# What if we want every <ol> and every <ul> that the page contains? We can select both of these types of elements with a regex in our .find_all():

# import re
# soup.find_all(re.compile("[ou]l"))
# What if we want all of the h1 - h9 tags that the page contains? Regex to the rescue again!

# import re
# soup.find_all(re.compile("h[1-9]"))
# Using Lists
# We can also just specify all of the elements we want to find by supplying the function with a list of the tag names we are looking for:

# soup.find_all(['h1', 'a', 'p'])
# Using Attributes
# We can also try to match the elements with relevant attributes. We can pass a dictionary to the attrs parameter of find_all with the desired attributes of the elements we’re looking for. If we want to find all of the elements with the "banner" class, for example, we could use the command:

# soup.find_all(attrs={'class':'banner'})
# Or, we can specify multiple different attributes! What if we wanted a tag with a "banner" class and the id "jumbotron"?

# soup.find_all(attrs={'class':'banner', 'id':'jumbotron'})
# Using A Function
# If our selection starts to get really complicated, we can separate out all of the logic that we’re using to choose a tag into its own function. Then, we can pass that function into .find_all()!

# def has_banner_class_and_hello_world(tag):
#     return tag.attr('class') == "banner" and tag.string == "Hello world"

# soup.find_all(has_banner_class_and_hello_world)
# This command would find an element that looks like this:

# <div class="banner">Hello world</div>
# but not an element that looks like this:

# <div>Hello world</div>
# Or this:

# <div class="banner">What's up, world!</div>

#webpage_response = requests.get('https://s3.amazonaws.com/codecademy-content/courses/beautifulsoup/shellter.html')

#webpage = webpage_response.content
#soup = BeautifulSoup(webpage, "html.parser")
turtle_links = soup.find_all('a')
print(turtle_links)

#---------------------------------------------------------------------------------------------------------------------------------------------------------

#import requests
#from bs4 import BeautifulSoup

#WEB SCRAPING WITH BEAUTIFUL SOUP
# Select for CSS Selectors
# Another way to capture your desired elements with the soup object is to use CSS selectors. The .select() method will take in all of the CSS selectors you normally use in a .css file!
# <h1 class='results'>Search Results for: <span class='searchTerm'>Funfetti</span></h1>
# <div class='recipeLink'><a href="spaghetti.html">Funfetti Spaghetti</a></div>
# <div class='recipeLink' id="selected"><a href="lasagna.html">Lasagna de Funfetti</a></div>
# <div class='recipeLink'><a href="cupcakes.html">Funfetti Cupcakes</a></div>
# <div class='recipeLink'><a href="pie.html">Pecan Funfetti Pie</a></div>
# If we wanted to select all of the elements that have the class 'recipeLink', we could use the command:
# soup.select(".recipeLink")
# If we wanted to select the element that has the id 'selected', we could use the command:
# soup.select("#selected")
# Let’s say we wanted to loop through all of the links to these funfetti recipes that we found from our search.
# for link in soup.select(".recipeLink > a"):
#   webpage = requests.get(link)
#   new_soup = BeautifulSoup(webpage)
# This loop will go through each link in each .recipeLink div and create a soup object out of the webpage it links to. So, it would first make soup out of <a href="spaghetti.html">Funfetti Spaghetti</a>, then <a href="lasagna.html">Lasagna de Funfetti</a>, and so on.

prefix = "https://s3.amazonaws.com/codecademy-content/courses/beautifulsoup/"
#webpage_response = requests.get('https://s3.amazonaws.com/codecademy-content/courses/beautifulsoup/shellter.html')

#webpage = webpage_response.content
#soup = BeautifulSoup(webpage, "html.parser")

turtle_links = soup.find_all("a")
links = []
#go through all of the a tags and get the links associated with them:
for a in turtle_links:
    links.append(prefix+a["href"])
    
#Define turtle_data:
turtle_data = {}

#follow each link:
for link in links:
  webpage = requests.get(link)
  turtle = BeautifulSoup(webpage.content, "html.parser")
  #Add your code here:
  turtle_name = turtle.select('.name')[0]
  turtle_data[turtle_name] = []
  
#We have taken the links you found in the last exercise and turned them into links we can follow by prepending a prefix to them.
#Now, we’re looping through each of the links on the home page and following them to learn more about each turtle!
#We are going to want to store information about each turtle in a dictionary called turtle_data.
#First, before the loop that goes through the turtle_links, create an empty dictionary called turtle_data.

#Now, let’s fill in some data from each turtle. Inside the loop that iterates through links, you’ll see that we’ve created a BeautifulSoup object out of each individual turtle’s page.
#You can click on a turtle in the web browser to see how an individual turtle’s page looks. What kind of information from this page might we want to store?
  
#If you used your Inspector tools to look at the turtle’s page, you might have seen that the turtle’s name is in a p tag with the class name.
#Inside the loop, use .select() to select the tags with class name. Store the first entry of that list in a variable called turtle_name.
#Add turtle_name to the dictionary as a key, and for now set the value of that key to an empty list.

#---------------------------------------------------------------------------------------------------------------------------------------------------------

#import requests
#from bs4 import BeautifulSoup

#WEB SCRAPING WITH BEAUTIFUL SOUP
#Reading Text
#When we use BeautifulSoup to select HTML elements, we often want to grab the text inside of the element, so that we can analyze it. We can use .get_text() to retrieve the text inside of whatever tag we want to call it on.
#<h1 class="results">Search Results for: <span class='searchTerm'>Funfetti</span></h1>
#If this is the HTML that has been used to create the soup object, we can make the call:
#soup.get_text()
#Which will return:
#'Search Results for: Funfetti'
#Notice that this combined the text inside of the outer h1 tag with the text contained in the span tag inside of it! Using get_text(), it looks like both of these strings are part of just one longer string. If we wanted to separate out the texts from different tags, we could specify a separator character. This command would use a . character to separate:
#soup.get_text('|')
#Now, the command returns:
#'Search Results for: |Funfetti'
#``

#prefix = "https://s3.amazonaws.com/codecademy-content/courses/beautifulsoup/"
#webpage_response = requests.get('https://s3.amazonaws.com/codecademy-content/courses/beautifulsoup/shellter.html')

#webpage = webpage_response.content
#soup = BeautifulSoup(webpage, "html.parser")

turtle_links = soup.find_all("a")
links = []
#go through all of the a tags and get the links associated with them"
for a in turtle_links:
    links.append(prefix+a["href"])
    
#Define turtle_data:
turtle_data = {}

#follow each link:
for link in links:
  webpage = requests.get(link)
  turtle = BeautifulSoup(webpage.content, "html.parser")
  turtle_name = turtle.select(".name")[0].get_text()
  
  stats = turtle.find("ul")
  stats_text = stats.get_text("|")
  turtle_data[turtle_name] = stats_text.split("|")
  
#After the loop, print out turtle_data. We have been storing the names as the whole p tag containing the name.
#Instead, let’s call get_text() on the turtle_name element and store the result as the key of our dictionary instead.
  
#Instead of associating each turtle with an empty list, let’s have each turtle associated with a list of the stats that are available on their page.
#It looks like each piece of information is in a li element on the turtle’s page.
#Get the ul element on the page, and get all of the text in it, separated by a '|' character so that we can easily split out each attribute later.
#Store the resulting string in turtle_data[turtle_name] instead of storing an empty list there.

#When we store the list of info in each turtle_data[turtle_name], separate out each list element again by splitting on '|'.

#-------------------------------------------------------------------------------------------------------------------------------------------------------

#import requests
#from bs4 import BeautifulSoup
import pandas as pd

#WEB SCRAPING WITH BEAUTIFUL SOUP
#Review
#Amazing! Now you know the basics of how to use BeautifulSoup to turn websites into data. If you take our Data Visualization or Data Manipulation courses, you can see how you might analyze this data and find patterns!
#You now can see how far the rabbit hole goes by finding some interesting data you want to analyze on the web. But remember to be respectful to site owners if you test out your scraping chops on real sites.

#prefix = "https://s3.amazonaws.com/codecademy-content/courses/beautifulsoup/"
#webpage_response = requests.get('https://s3.amazonaws.com/codecademy-content/courses/beautifulsoup/shellter.html')

#webpage = webpage_response.content
#soup = BeautifulSoup(webpage, "html.parser")

turtle_links = soup.find_all("a")
links = []
#go through all of the a tags and get the links associated with them"
for a in turtle_links:
    links.append(prefix+a["href"])
    
#Define turtle_data:
turtle_data = {}

#follow each link:
for link in links:
  webpage = requests.get(link)
  turtle = BeautifulSoup(webpage.content, "html.parser")
  turtle_name = turtle.select(".name")[0].get_text()
  
  stats = turtle.find("ul")
  stats_text = stats.get_text("|")
  turtle_data[turtle_name] = stats_text.split("|")
  
#Create a DataFrame out of the turtle_data dictionary you’ve created. Call it turtle_df.
#turtle_df = pd(turtle_data)
turtle_df = pd.DataFrame.from_dict(turtle_data, orient='index')

#Wow! Now we have all of the turtles’ information in one DataFrame. But obviously, in just scraping this data and plopping it into Pandas, we’re left with a pretty messy DataFrame.
#There are newlines in the data, the column names are hidden in strings in the rows, and none of the numerical data is stored as a numerical type.
#It would be pretty hard to create any sort of analysis on this raw data. What if we wanted to make a histogram of the ages of turtles in the Shellter?
#This is where Data Cleaning and Regex comes in! Try to practice what you know about data cleaning to get turtles_df into a usable state. It’s up to you to decide what “usable” means to you.
print(turtle_df)
