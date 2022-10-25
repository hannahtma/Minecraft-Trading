from __future__ import annotations

from cave import Cave
from material import Material
from trader import Trader
from food import Food
from random_gen import RandomGen

# List taken from https://minecraft.fandom.com/wiki/Mob
PLAYER_NAMES = [
    "Steve",
    "Alex",
    "ɘᴎiɿdoɿɘH",
    "Allay",
    "Axolotl",
    "Bat",
    "Cat",
    "Chicken",
    "Cod",
    "Cow",
    "Donkey",
    "Fox",
    "Frog",
    "Glow Squid",
    "Horse",
    "Mooshroom",
    "Mule",
    "Ocelot",
    "Parrot",
    "Pig",
    "Pufferfish",
    "Rabbit",
    "Salmon",
    "Sheep",
    "Skeleton Horse",
    "Snow Golem",
    "Squid",
    "Strider",
    "Tadpole",
    "Tropical Fish",
    "Turtle",
    "Villager",
    "Wandering Trader",
    "Bee",
    "Cave Spider",
    "Dolphin",
    "Enderman",
    "Goat",
    "Iron Golem",
    "Llama",
    "Panda",
    "Piglin",
    "Polar Bear",
    "Spider",
    "Trader Llama",
    "Wolf",
    "Zombified Piglin",
    "Blaze",
    "Chicken Jockey",
    "Creeper",
    "Drowned",
    "Elder Guardian",
    "Endermite",
    "Evoker",
    "Ghast",
    "Guardian",
    "Hoglin",
    "Husk",
    "Magma Cube",
    "Phantom",
    "Piglin Brute",
    "Pillager",
    "Ravager",
    "Shulker",
    "Silverfish",
    "Skeleton",
    "Skeleton Horseman",
    "Slime",
    "Spider Jockey",
    "Stray",
    "Vex",
    "Vindicator",
    "Warden",
    "Witch",
    "Wither Skeleton",
    "Zoglin",
    "Zombie",
    "Zombie Villager",
    "H̴͉͙̠̥̹͕͌̋͐e̸̢̧̟͈͍̝̮̹̰͒̀͌̈̆r̶̪̜͙̗̠̱̲̔̊̎͊̑̑̚o̷̧̮̙̗̖̦̠̺̞̾̓͆͛̅̉̽͘͜͝b̸̨̛̟̪̮̹̿́̒́̀͋̂̎̕͜r̸͖͈͚̞͙̯̲̬̗̅̇̑͒͑ͅi̶̜̓̍̀̑n̴͍̻̘͖̥̩͊̅͒̏̾̄͘͝͝ę̶̥̺̙̰̻̹̓̊̂̈́̆́̕͘͝͝"
]

class Player():

    DEFAULT_EMERALDS = 50

    MIN_EMERALDS = 14
    MAX_EMERALDS = 40

    def __init__(self, name, emeralds=None) -> None:
        self.name = name
        self.balance = self.DEFAULT_EMERALDS if emeralds is None else emeralds

    def set_traders(self, traders_list: list[Trader]) -> None:
        self.traders_list = traders_list

    def set_foods(self, foods_list: list[Food]) -> None:
        self.foods_list = foods_list

    @classmethod
    def random_player(self) -> Player:
        name_index = RandomGen(0, 80)
        self.name = PLAYER_NAMES[name_index]
        balance = None

        return Player(self.name, balance)

    def set_materials(self, materials_list: list[Material]) -> None:
        self.materials_list = materials_list

    def set_caves(self, caves_list: list[Cave]) -> None:
        self.caves_list = caves_list

    def select_food_and_caves(self) -> tuple[Food | None, float, list[tuple[Cave, float]]]:
        max_hunger_bars = 0
        for food in range(len(self.foods_list)):
            if self.foods_list[food].get_hunger_bars() > max_hunger_bars:
                max_hunger_bars = self.foods_list[food].get_hunger_bars()
                food_choice = self.foods_list[food]

        self.hunger_bars = max_hunger_bars
        self.balance -= food_choice.get_price()

        while self.hunger_bars > 0:
            print("current self.hunger_bars:", self.hunger_bars)
            print("current self.balance:", self.balance)
            best_price = 0
            for trader in self.traders_list:
                if trader.get_buy_price() > best_price:
                    best_price = trader.get_buy_price()
                    print("best price for", trader.get_selected_material(), "is", trader.get_buy_price())
                    item_to_buy = trader.get_selected_material()
                    
            for cave in self.caves_list:
                if item_to_buy == cave.get_material():
                    the_cave = cave

            self.hunger_bars -= item_to_buy.get_mining_rate() * the_cave.get_quantity()
            self.balance += best_price * the_cave.get_quantity()
        
        return (food_choice, self.balance, self.caves_list)

    def __str__(self) -> str:
        return f"{self.caves_list}"

if __name__ == "__main__":
    print(len(PLAYER_NAMES))