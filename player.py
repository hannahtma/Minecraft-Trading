from __future__ import annotations
from avl import AVLTree

from cave import Cave
from material import Material
from trader import Trader
from food import Food
from random_gen import RandomGen
from node import TreeNode

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
        self.foods = AVLTree()

    def get_balance(self):
        return self.balance

    def get_materials_sold(self):
        return self.materials_sold
    
    def get_foods(self):
        return self.foods

    def set_traders(self, traders_list: list[Trader]) -> None:
        self.traders_list = traders_list
        # print("This is trader list:")
        # for x in self.traders_list:
        #     print(x)

    def set_foods(self, foods_list: list[Food]) -> None:
        for food in foods_list:
            food_item = TreeNode(food.get_hunger_bars(), food)
            if self.foods.__contains__(food_item.key) != True:
                self.foods.__setitem__(food_item.key, food_item.item)
        # self.current = TreeNode(foods_list[len(foods_list)-1].get_hunger_bars(), foods_list[len(foods_list)-1])

    @classmethod
    def random_player(self) -> Player:
        name = RandomGen.random_choice(PLAYER_NAMES)
        balance = None

        return Player(name, balance)

    def set_materials(self, materials_list: list[Material]) -> None:
        self.materials_list = materials_list
        
    def set_caves(self, caves_list: list[Cave]) -> None:
        self.caves_list = caves_list

    def select_food_and_caves(self) -> tuple[Food | None, float, list[tuple[Cave, float]]]:
        self.caves = []
        food_choice = self.foods.get_maximal(self.foods.root)
        print("food choice", food_choice)

        self.hunger_bars = food_choice.item.get_hunger_bars()
        self.balance -= food_choice.item.get_price()
        print("hunger bars", self.hunger_bars)
        print("balance: ", self.balance)

        self.materials_sold = []
        while self.hunger_bars > 0 and self.traders_list.is_empty() == False:
            print("current self.hunger_bars:", self.hunger_bars)
            print("current self.balance:", self.balance)

            best_price = self.traders_list.get_maximal(self.traders_list.root)
            self.traders_list.__delitem__(best_price.key)
            # for x in self.traders_list:
            #     print("trader",x)
            print("best price: ", best_price)

            item_to_buy = best_price.item.get_selected_material()
            print("item to buy: ", item_to_buy)

            # print("this is self.caves_list: ")
            # print("here",type(self.caves_list))

            for cave in self.caves_list:
                print(cave)

            for cave in self.caves_list:
                if cave.get_material() == item_to_buy:
                    the_cave = self.caves_list.index(cave)
                    self.caves.append(the_cave)
                    self.hunger_bars -= item_to_buy.get_mining_rate() * cave.get_quantity()
                    print("after purchase: ", self.hunger_bars)
                    self.balance += best_price.item.get_buy_price() * cave.get_quantity()
                    self.materials_sold.append((cave,cave.get_quantity()))
        print("this is materials sold",self.materials_sold)
        
        return (food_choice, self.balance, self.caves)

    def __str__(self) -> str:
        return f"{self.name} {self.balance}💰"
