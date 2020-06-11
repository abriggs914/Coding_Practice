
# Python program to estimate the resource
# costs of a very ambitious item sorting
# machine in Minecraft
#
# June 2020

bricks = {
    "Cobblestone": (64, 5),
    "Andestite": (64, 5),
    "Granite": (64, 5),
    "Dorite": (64, 5),
    "Dirt": (64, 5),
    "Iron ore": (64, 1),
    "Gold ore": (64, 1),
    "Iron ingot": (64, 3),
    "Gold ingot": (64, 3),
    "Diamond": (64, 3),
    "Coal": (64, 3),
    "Gravel":(64, 5),
    "Sand":(64, 5),
    "Obsidian":(64, 3),
    "Sandstone":(64, 5),
    "Stone":(64, 5),
    "Redstone": (64, 5),
    "Lapis lazuli": (64, 5)
}

total_chests = 0
total_storable_bricks = 0
total_hoppers = 0
total_slabs = 0
total_minerals = {
    "IRON": 0,
    "CHESTS": 0,
    "WOOD": 0,
    "COBBLESTONE": 0,
    "SLABS": 0
}

for brick_type, vals in bricks.items():
    num_in_stack = vals[0]
    num_chests = vals[1] * 2
    hoppers_required = vals[1] + 2
    slabs_required = 20 * (hoppers_required - 1)
    minerals_required = 3
    total_bricks_in_chest = (num_in_stack * num_chests) * 27
    print(brick_type + " requires " + str(num_chests) + " chests, holding a total of " + str(total_bricks_in_chest))
    total_chests += num_chests
    total_storable_bricks += total_bricks_in_chest
    
    total_minerals[brick_type] = minerals_required
    total_minerals["IRON"] += (hoppers_required * 5)
    total_minerals["CHESTS"] += (hoppers_required + num_chests)
    total_minerals["WOOD"] += (hoppers_required + num_chests) * 8
    total_minerals["COBBLESTONE"] += (slabs_required * 3)
    total_minerals["SLABS"] += slabs_required
    
print("\nRequires:\n\tChests:\t\t" + str(total_chests) + "\n\tHolding:\t" + str(total_storable_bricks) + "\n\nMinerals Required:\n")

for mineral, n_required in total_minerals.items():
    print("\t" + mineral + ":\t\t" + str(n_required))
    
print("\n\nBase Resources Estimate:\n")
print("\tIron ingots:\t" + str(total_minerals["IRON"]) + ", in stacks: (" + str(total_minerals["IRON"] / 64) + ")")
print("\tChests:\t\t" + str(total_minerals["CHESTS"]) + ", in stacks: (" + str(total_minerals["CHESTS"] / 64) + ")")
print("\tWood:\t\t" + str(total_minerals["WOOD"]) + ", in stacks: (" + str(total_minerals["WOOD"] / 64) + ")")
print("\tSlabs:\t\t" + str(total_minerals["SLABS"]) + ", in stacks: (" + str(total_minerals["SLABS"] / 64) + ")")
print("\tCobblestone:\t" + str(total_minerals["COBBLESTONE"]) + ", in stacks: (" + str(total_minerals["COBBLESTONE"] / 64) + ")")
    
