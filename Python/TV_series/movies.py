

list_of_movies = [
	{
		"Star Wars": [
			"Episode IV - A New Hope",
			"Episode V - The Empire Strikes Back",
			"Episode VI - Return of the Jedi",
			"Episode I - The Phantom Menace",
			"Episode II - Attack of the Clones",
			"Episode III - Revenge of the Sith"
			"Rogue One"
		]
	},
	{
		"The Dark Knight": [
			"Batman Begins",
			"The Dark Knight",
			"The Dark Knight Rises"
		]
	},
	{
		"Pirates Of The Caribbean": [
			"Pirates of the Caribbean: The Curse of the Black Pearl",
			"Pirates of the Caribbean: Dead Man's Chest",
			"Pirates of the Caribbean: At World's End",
			"Pirates of the Caribbean: On Stranger Tides",
			"Pirates of the Caribbean: Dead Men Tell No Tales"
		]
	},
	"The Prestiege",
	"Free Guy",
	{
		"Transformers": [
			"Transformers",
			"Transformers: Revenge of the Fallen",
			"Transformers: Dark of the Moon",
			"Transformers: Age of Extinction",
			"Transformers: The Last Knight"
		]
	},
	"Idiocracy",
	{
		"Die Hard": [
			"Die Hard",
			"Die Hard 2",
			"Die Hard with a Vengeance",
			"Live Free or Die Hard",
			"A Good Day to Die Hard"
		]
	},
	"Jungle Cruise",
	"Race To Witch Mountain",
	"The Sitter",
	"Dodgeball",
	{
		"Deadpool": [
			"Deadpool",
			"Deadpool 2"
		]
	},
	"Public Enemies",
	"Oblivion",
	"The Tomorrow War",
	{
		"Kingsman": [
			"Kingsman The Secret Service",
			"Kingsman The Golden Circle",
			"The Kingsman"
		]
	},
	"The A-Team",
	"Need For Speed",
	{	
		"SuperTroopers": [
			"SuperTroopers",
			"SuperTroopers 2"
		]
	},
	{
		"Alien": [
			"Alien",
			"Aliens",
			"Alien 3",
			"Alien Resurrection",
		]
	},
	{
		"Predator": [
			"Predator"
		]
	}
]


if __name__ == "__main__":
	n_collections = len(list_of_movies)
	n_movies = sum([1 if isinstance(mov, str) else sum([len(v) for m, v in mov.items()]) for mov in list_of_movies])
	print(f"N collections: {n_collections}")
	print(f"N movies: {n_movies}")
