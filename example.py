from game import SoloGame
from material import Material
from cave import Cave
from trader import RandomTrader
from food import Food
from random_gen import RandomGen

RandomGen.set_seed(16)
        
gold = Material("Gold Nugget", 27.24)
netherite = Material("Netherite Ingot", 20.95)
fishing_rod = Material("Fishing Rod", 26.93)
ender_pearl = Material("Ender Pearl", 13.91)
prismarine = Material("Prismarine Crystal", 11.48)

materials = [
    gold,
    netherite,
    fishing_rod,
    ender_pearl,
    prismarine,
]

caves = [
    Cave("Boulderfall Cave", prismarine, 10),
    Cave("Castle Karstaag Ruins", netherite, 4),
    Cave("Glacial Cave", gold, 3),
    Cave("Orotheim", fishing_rod, 6),
    Cave("Red Eagle Redoubt", fishing_rod, 3),
]

waldo = RandomTrader("Waldo Morgan")
waldo.add_material(fishing_rod)     # Now selling for 7.57
orson = RandomTrader("Orson Hoover")
orson.add_material(gold)            # Now selling for 4.87
lea = RandomTrader("Lea Carpenter")
lea.add_material(prismarine)        # Now selling for 5.65
ruby = RandomTrader("Ruby Goodman")
ruby.add_material(netherite)        # Now selling for 8.54
mable = RandomTrader("Mable Hodge")
mable.add_material(gold)            # Now selling for 6.7

traders = [
    waldo,
    orson,
    lea,
    ruby,
    mable,
]

for trader in traders:
    trader.generate_deal()

g = SoloGame()
g.initialise_with_data(materials, caves, traders, ["Jackson"], [50])

# Avoid simulate_day - This regenerates trader deals and foods.
foods = [
    Food("Cabbage Seeds", 106, 30),
    Food("Fried Rice", 129, 24),
    Food("Cooked Chicken Cuts", 424, 19),
]

g.player.set_foods(foods)
food, balance, caves = g.player.select_food_and_caves()

print(balance) # 185.01974749350165 - pow(10, -4)
# Actual tests will also check your output is possible.
