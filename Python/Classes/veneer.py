#VENEER
#Veneer
#Here at Veneer we strive to provide the best marketplace experience to connect vetted art dealers with premium galleries. Create a marketplace for people and organizations to buy and sell pieces of art!
#In this project we’ll be developing classes and objects that represent the various responsibilities of art dealership software.
#If you get stuck during this project or would like to see an experienced developer work through it, click “Get Help“ to see a project walkthrough video.
# https://youtu.be/c4s0C52sqjQ

#Here at Veneer, our main concern is the buying and selling of priceless art works. Let’s start out by building a model for these works of art.
#Define a class called Art.

#Give Art a constructor that takes self and three additional parameters: artist, title, medium, and year.
#Assign these values to self.artist, self.title, self.medium and self.year.

#Give your Art class a string representation method. This method should return a representation of the artwork in as close to standard citation format as we can manage (without italics). It should state:
#The artist’s name
#The name of the artwork in quotes
#The year the work was created
#The medium
#For instance:
#Monet, Claude. "Vétheuil in the Fog". 1879, oil on canvas.

#A full citation of a work of art necessarily includes the name of the person/entity whose collection it includes, as well as the location if that place is a museum.
#Because the work of art has an owner property, we can retrieve some of that information from self.owner.
#Let’s update Art‘s string representation method to add the self.owner.name at the very end, followed by a comma, followed by self.owner.location, followed by a period.

def dollar_amount(dollars):
  num = dollars[1:]
  lst = num.split(' ')
  lst = lst[0]
  num = lst[:len(lst)-1]
  return int(num)

class Art:
  
  def __init__(self, artist, title, medium, year, owner):
    self.artist = artist
    self.title = title
    self.medium = medium
    self.year = year
    self.owner = owner
  
  def __repr__(self):
    return "{artist}. \"{title}\". {year}, {medium}. {owner}, {location}".format(artist = self.artist, title = self.title, year = self.year, medium = self.medium, owner = self.owner.name, location = self.owner.location)
  
#In order to buy and sell works of art, we need a marketplace that will maintain the responsibilities of buying, selling, listing, and delisting of those artworks.
#Create a new class called Marketplace.

#Give your Marketplace class a constructor. In Marketplace‘s constructor, define self.listings as a new list.

#Create an .add_listing() method for your Marketplace class. This should take two arguments: self and new_listing. Have .add_listing() add the new listing to Marketplace‘s listings attribute.

#Since we’ll need a way to remove listings when they expire or are acted upon, let’s implement a .remove_listing() method for our Marketplace

#The main usage of our application will be the perusal of a marketplace’s listings. Let’s include that functionality as well.
#Add a .show_listings() method to your Marketplace class that iterates through each listing in self.listings and prints them all out.
class Marketplace:
  
  def __init__(self):
    self.listings = []
    
  def add_listing(self, new_listing):
    self.listings.append(new_listing)
  
  def remove_listing(self, new_listing):
    self.listings.remove(new_listing)
  
  def show_listings(self):
    for item in self.listings:
      print(item)

#Create our main marketplace by instantiating Marketplace and saving it into the variable veneer.
veneer = Marketplace()

#Print out the results of veneer.show_listings(). This should be empty for now so won’t print anything, but it’s good to test if your code has any errors!
veneer.show_listings()

#Now that we have a marketplace to facilitate the buying and selling, let’s create our class to list works of art!
#Create a new class called Listing. We’ll use these as listings for our Marketplace.

#Our Listing class needs a constructor! It should define the following instance variables:
#self.art, the work of art being listed
#self.price, the price of the work
#self.seller an instance of Client.
#Each instance variable should be set equal to an argument passed to the constructor.

#Give the Listing a string representation which should print out the following:
#The name of the work of art
#The price of the work of art
#Remember not to use the string representation of Art for this, it’s too verbose and our clientele will want to parse the listings without reading all of the metadata unless they’re interested in purchasing in the artwork.
class Listing:
  
  def __init__(self, art, price, seller):
    self.art = art
    self.price = price
    self.seller = seller
  
  def __repr__(self):
    return "Name: {name}\nPrice: {price}\nSeller: {seller}".format(name = self.art.title, price = self.price, seller = self.seller)

#Now for the most important aspect of a marketplace, clients! Create a new class called Client.

#Give our Client class a constructor. A client should have the following data:
#elf.name the name of the person or institution.
#self.location is the name of the location of the museum or “Private Collection” if the client is a collector.
#self.is_museum, a boolean value representing whether the client is a museum (if True) or a collector (if False).
#name, location, and is_museum should all be passed as arguments to the constructor.

#Update our Client class to have a new method, .sell_artwork(). This method should take two parameters: self, artwork, and price.
#.sell_artwork() should do the following:
#Check that artwork.owner is the same (==) as self (i.e., make sure the client owns the art they’re trying to sell).
#Create a new Listing with the given art, price, and client.
#Add the listing to the marketplace using veneer.add_listing().

#There’s one last piece of functionality before we’re ready to hit the market (so to speak), our clients need to be able to buy art!
#Create a .buy_artwork() method for the Client class. .buy_artwork() should take two arguments: self and artwork.
#Start by having .buy_artwork() check that the artwork is not owned by the client.
#The next thing .buy_artwork() should do is make sure that the artwork is listed in veneer.listings. Save the appropriate listing as art_listing, we’ll need to remove it later.

#If the art is not currently owned and is listed then go through with the transaction! .buy_artwork() should do the following:
#Change the artwork.owner to the client doing the purchasing.
#Remove the listing from the marketplace using veneer.remove_listing()
class Client:
  
  def __init__(self, name, location, is_museum):
    self.name = name
    self.location = location
    self.is_museum = is_museum
    self.wallet = 0
    
  def sell_artwork(self, artwork, price):
    if (artwork.owner.name == self.name):
      listing = Listing(artwork, price, self.name)
      veneer.add_listing(listing)
      
  def buy_artwork(self, artwork):
    if (artwork.owner.name != self.name):      
      for listing in veneer.listings:
        if (artwork.title == listing.art.title):
          art_listing = listing
          artwork.owner.wallet += dollar_amount(art_listing.price)
          artwork.owner = self
          self.wallet -= dollar_amount(art_listing.price)
          veneer.remove_listing(art_listing)
  
  def __repr__(self):
    return "Name: {name}\nLocation: {location}\nMuseum: {museum}\nWallet: {wallet}".format(name = self.name, location = self.location, museum = self.is_museum, wallet = self.wallet)
  
#Now instantiate our first Client: her name is Edytta Halpirt and she is a collector and not a museum.
#Save our new Client to a variable called edytta.
edytta = Client("Edytta Halpirt", "Private Collection", False)

#Every purchase requires a buyer and a seller, let’s create a second Client with the following information:
#It’s name is “The MOMA”
#It is located in “New York”
#It is a museum.
#Save this Client to a variable called moma.
moma = Client("The MOMA", "New York", True) 
  
#We need to get the MOMA to purchase a Picasso from Edytta, but for now try running your code to make sure our Client class doesn’t produce any errors.

#Now that we have Clients our works of Art can have owners! Let’s update our Art class constructor to take an additional parameter, owner, and assign that to self.owner.
  
#Move our instantiation of girl_with_mandolin to after our instantiation of edytta. When creating the Art object for girl_with_mandolin, pass in edytta as the owner.
  
#Let’s see how our Art class looks, create a new work of art. Our first client wants to list a particular Picasso painting to make more space for her new fascination with Italian Futurism, so let’s see if we can use our data model for this piece:
#The artist is “Picasso, Pablo”.
#The work’s title is “Girl with a Mandolin (Fanny Tellier)”.
#The artwork was created in 1910.
#The medium is “oil on canvas”.
#Save this work of art into the variable girl_with_mandolin.
girl_with_mandolin = Art("Picasso, Pablo", "Girl with a Mandolin (Fanny Tellier)", "oil on canvas", 1910, edytta)  

#Move our print statement printing out girl_with_mandolin to after its new instantiation. Does it print out the following?
#Picasso, Pablo. "Girl with a Mandolin (Fanny Tellier)". 1910, oil on canvas. Edytta Halpirt, Private Collection.

#Print out girl_with_mandolin and run your code, does your code produce this output?
#Picasso, Pablo. "Girl with a Mandolin (Fanny Tellier)". 1910, oil on canvas.
print(girl_with_mandolin)  

#Use edytta.sell_artwork() to create a listing for girl_with_mandolin. Edytta wants to sell it for $6M (USD).
edytta.sell_artwork(girl_with_mandolin, "$6M (USD)") 
  
#Call veneer.show_listings(), is our newly listed work of art on the market?
veneer.show_listings() 

#The MOMA is very interested in purchasing girl_with_mandolin. Call .buy_artwork() from the moma instance with girl_with_mandolin as an argument.
moma.buy_artwork(girl_with_mandolin) 
  
#Finally, print out girl_with_mandolin one last time. It should display the following:
#Monet, Claude. "Vétheuil in the Fog". 1879, oil on canvas. The MOMA, New York.
print(girl_with_mandolin)
  
#Also call veneer.show_listings(). There shouldn’t be any listings left! Congrats on one purchase successfully made!
veneer.show_listings()

vetheuil_in_the_fog = Art("Monet, Claude", "Vétheuil in the Fog", "oil on canvas", 1879, moma)

moma.sell_artwork(vetheuil_in_the_fog, "$7M (USD)")

veneer.show_listings()

edytta.buy_artwork(vetheuil_in_the_fog)

veneer.show_listings()

#Amazing! We built out a whole marketplace with buyers, sellers, art, and listings!
#Here are some more things you could try:
#Add a wallet instance variable to clients, update the buying and selling of artworks to also exchange dollar amounts.
print(edytta)
print(moma)

#Create a wishlist for your clients, things that are listed but they’re not sure if they should purchase just yet.
#Create expiration dates for listings! Have out of date listings automatically removed from the marketplace.  