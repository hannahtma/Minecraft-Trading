""" Game

Implements the key features that take place during a particular game, 
which includes random generating materials, caves, traders and players
as well as simulating days and verifying that player choices are correct
"""

from __future__ import annotations
from abc import abstractmethod
from hash_table import LinearProbeTable
from node import TreeNode

from player import Player, PLAYER_NAMES
from trader import Trader
from material import Material
from cave import Cave
from food import Food
from random_gen import RandomGen
from avl import AVLTree
from trader import RandomTrader, RangeTrader, HardTrader
from heap import MaxHeap
from linked_stack import LinkedStack

class Game:

    MIN_MATERIALS = 5
    MAX_MATERIALS = 10

    MIN_CAVES = 5
    MAX_CAVES = 10

    MIN_TRADERS = 4
    MAX_TRADERS = 8

    MIN_FOOD = 2
    MAX_FOOD = 5

    def __init__(self) -> None:
        """
            Instantiates a game object
        """
        self.materials = AVLTree()
        self.traders = AVLTree()

    def initialise_game(self) -> None:
        """
            Initialise all game objects: Materials, Caves, Traders.
        """
        N_MATERIALS = RandomGen.randint(self.MIN_MATERIALS, self.MAX_MATERIALS)
        self.generate_random_materials(N_MATERIALS)
        print("Materials:\n\t", end="")
        print("\n\t".join(map(str, self.get_materials())))
        N_CAVES = RandomGen.randint(self.MIN_CAVES, self.MAX_CAVES)
        self.generate_random_caves(N_CAVES)
        print("Caves:\n\t", end="")
        print("\n\t".join(map(str, self.get_caves())))
        N_TRADERS = RandomGen.randint(self.MIN_TRADERS, self.MAX_TRADERS)
        self.generate_random_traders(N_TRADERS)
        print("Traders:\n\t", end="")
        print("\n\t".join(map(str, self.get_traders())))

    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader]):
        """
            Initialize the materials, caves, and traders to the parameter arguments

            Complexity: o()
        """
        self.set_materials(materials)
        self.set_caves(caves)
        self.set_traders(traders)
    
    def set_materials(self, mats: list[Material]) -> None:
        """
            Sets self.materials to the material list passed through

            Parameters:
                - mats: the list of materials for the game

            :complexity: O(1)
        """
        # self.materials_key_list = []
        # for material in mats:
        #     self.materials.__setitem__(material.get_mining_rate(), material)
        #     self.materials_key_list.append(material.get_mining_rate())
        self.materials = mats

    def set_caves(self, caves: list[Cave]) -> None:
        """
            Sets self.caves to the cave list passed through

            Parameters:
                - caves: the list of caves for the game

            :complexity: O(n), where n is the number of caves
        """
        self.caves = caves
        self.cave_materials = []
        for cave in caves:
            self.cave_materials.append(cave.get_material())

    def set_traders(self, traders: list[Trader]) -> None:
        """
            Sets self.traders to the trader list passed through

            Parameters:
                - traders: the list of traders for the game

            :complexity: O(1)
        """
        self.traders = traders
        
    def get_materials(self) -> list[Material]:
        
        return self.materials

    def get_caves(self) -> list[Cave]:
        return self.caves

    def get_traders(self) -> list[Trader]:
        return self.traders

    def generate_random_materials(self, amount):
        """
        Generates <amount> random materials using Material.random_material
        Generated materials must all have different names and different mining_rates.
        (You may have to call Material.random_material more than <amount> times.)
        """
        materials_generated = []
        material_names = []
        material_mining_times = []
        number = 0
        while number < amount:
            material_to_add = Material.random_material()
            if material_to_add.get_name() not in material_names and material_to_add.get_mining_rate() not in material_mining_times:
                materials_generated.append(material_to_add)
                material_names.append(material_to_add.get_name())
                material_mining_times.append(material_to_add.get_mining_rate())
                number += 1
        self.set_materials(materials_generated)

    def generate_random_caves(self, amount):
        """
        Generates <amount> random caves using Cave.random_cave
        Generated caves must all have different names
        (You may have to call Cave.random_cave more than <amount> times.)
        """
        random_caves = []
        cave_names = []
        number = 0
        while number < amount:
            cave_to_add = Cave.random_cave(self.materials)
            if cave_to_add.get_name() not in cave_names:
                random_caves.append(cave_to_add)
                cave_names.append(cave_to_add.get_name())
                number += 1

        self.set_caves(random_caves)

    def generate_random_traders(self, amount):
        """
        Generates <amount> random traders by selecting a random trader class
        and then calling <TraderClass>.random_trader()
        and then calling set_all_materials with some subset of the already generated materials.
        Generated traders must all have different names
        (You may have to call <TraderClass>.random_trader() more than <amount> times.)
        """
        random_traders = []
        for _ in range(amount):
            trader = Trader.random_trader()
            random_traders.append(trader)
            trader.set_all_materials(self.materials)
        self.set_traders(random_traders)

    def finish_day(self):
        """
        DO NOT CHANGE
        Affects test results.
        """
        for cave in self.get_caves():
            if cave.quantity > 0 and RandomGen.random_chance(0.2):
                cave.remove_quantity(RandomGen.random_float() * cave.quantity)
            else:
                cave.add_quantity(round(RandomGen.random_float() * 10, 2))
            cave.quantity = round(cave.quantity, 2)

class SoloGame(Game):

    def initialise_game(self) -> None:
        """
            Initialises the game for one player.
            A player is randomly generated and all game objects are initialised
            based on the game's random generation.
        """
        super().initialise_game()
        self.player = Player.random_player()
        self.player.set_materials(self.get_materials())
        self.player.set_caves(self.get_caves())
        self.player.set_traders(self.get_traders())

    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader], player_names: list[int], emerald_info: list[float]):
        """
            Initialises game using specific data.
            Sets all game objects to the data passed through.
        """
        super().initialise_with_data(materials, caves, traders)
        self.player = Player(player_names[0], emeralds=emerald_info[0])
        self.player.set_materials(self.get_materials())
        for x in self.get_materials():
            print(x)
        self.player.set_caves(self.get_caves())
        for x in self.get_caves():
            print(x)
        self.player.set_traders(self.get_traders())
        for x in self.get_traders():
            print(x)

    def simulate_day(self):
        """
            Simulates a single day in the game, in which specific traders generate their
            own deals based on the game's objects.
        """
        # 1. Traders make deals    
        # Each trader from the trader list will generate a deal
        for trader in self.traders:
            trader.generate_deal()
        self.player.set_traders(self.get_traders())
        print("Traders Deals:\n\t", end="")
        print("\n\t".join(map(str, self.get_traders())))
        # 2. Food is offered
        food_num = RandomGen.randint(self.MIN_FOOD, self.MAX_FOOD)
        foods = []
        for _ in range(food_num):
            foods.append(Food.random_food())
        print("\nFoods:\n\t", end="")
        print("\n\t".join(map(str, foods)))
        self.player.set_foods(foods)
        # 3. Select one food item to purchase
        food, balance, caves = self.player.select_food_and_caves()
        print(food, balance, caves)
        # 4. Quantites for caves is updated, some more stuff is added.
        self.verify_output_and_update_quantities(food, balance, caves)

    def verify_output_and_update_quantities(self, food: Food | None, balance: float, caves: list[tuple[Cave, float]]) -> None:
        """
            Verifies that the food bought by the player is purchasable.
            Calculates the expected balance based on the list of materials that the player has mined
            and verifies that the balance is the same as the expected balance.
            Updates the quantities of materials in caves by referencing the quantities
            in the list of materials mined

            Parameters:
                - food: food that the player bought
                - balance: player's balance after mining
                - caves: list of caves player visited and quantities that the player mined
            
            :complexity: O(n*m) where n is the length of materials and m is the length of self.traders
        """
        materials = self.player.get_materials_mined()
        expected_balance = self.player.get_original_hunger_bars() - food.item.get_price()
        for index in range(len(materials)):
            the_material = materials[index][0].get_material() #get the material from the cave
            for trader in range(len(self.traders)):
                if self.traders[trader].get_material_selected() == the_material: #checks whether it is the same material
                    expected_balance += self.traders[trader].get_buy_price() * materials[index][1]

        for cave in range(len(caves)):
            original_cave = caves[cave]
            original_caves_quantity = caves[cave][1]
            quantity_to_check = materials[cave][1]
            if (original_caves_quantity >= quantity_to_check):
                cave_index = self.caves.index(original_cave[0])
                self.caves[cave_index].remove_quantity(quantity_to_check)
            else:
                raise ValueError("The quantities are wrong.")
        print("The quantities are correct.")

        if food != None:
            print("The food is purchasable.")
        else:
            raise ValueError("The food is not purchasable.")

        if (expected_balance == balance):
            print("The balance is correct.")
        else:
            raise ValueError("The balance is wrong.")
            
class MultiplayerGame(Game):

    MIN_PLAYERS = 2
    MAX_PLAYERS = 5

    def __init__(self) -> None:
        super().__init__()
        self.players = []
        for player in self.players:
            self.player = player

    def initialise_game(self) -> None:
        super().initialise_game()
        N_PLAYERS = RandomGen.randint(self.MIN_PLAYERS, self.MAX_PLAYERS)
        self.generate_random_players(N_PLAYERS)
        for player in self.players:
            player.set_materials(self.get_materials())
            player.set_caves(self.get_caves())
            player.set_traders(self.get_traders())
        print("Players:\n\t", end="")
        print("\n\t".join(map(str, self.players)))

    def generate_random_players(self, amount) -> None:
        """Generate <amount> random players. Don't need anything unique, but you can do so if you'd like."""
        self.players_generated = []
        player_names = []
        players_balance = []
        number = 0
        while number < amount:
            player_to_add = Player.random_player()
            if player_to_add.get_name() not in player_names and player_to_add.get_balance() not in players_balance:
                self.players_generated.append(player_to_add)
                player_names.append(player_to_add.get_name())
                players_balance.append(player_to_add.get_balance())
                number += 1

    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader], player_names: list[int], emerald_info: list[float]):
        super().initialise_with_data(materials, caves, traders)
        for player, emerald in zip(player_names, emerald_info):
            self.players.append(Player(player, emeralds=emerald))
            self.players[-1].set_materials(self.get_materials())
            self.players[-1].set_caves(self.get_caves())
            self.players[-1].set_traders(self.get_traders())
        print("Players:\n\t", end="")
        print("\n\t".join(map(str, self.players)))

    def simulate_day(self):
        # 1. Traders make deals
        self.trader_material_list = []
        for trader in self.traders:
            # trader = self.traders.__getitem__(trader_key)
            trader.generate_deal()
            self.trader_material_list.append(trader.get_material_selected())
        self.set_traders(self.traders)
        print("Traders Deals:\n\t", end="")
        print("\n\t".join(map(str, self.get_traders())))
        # 2. Food is offered
        offered_food = Food.random_food()
        print(f"\nFoods:\n\t{offered_food}")
        # 3. Each player selects a cave - The game does this instead.
        foods, balances, caves = self.select_for_players(offered_food)
        # 4. Quantites for caves is updated, some more stuff is added.
        self.verify_output_and_update_quantities(foods, balances, caves)

    def select_for_players(self, food: Food) -> tuple[list[Food|None], list[float], list[tuple[Cave, float]|None]]:
        """
        """
        food_list = []
        for player in self.players:
            if player.get_balance() >= food.get_price():
                food_list.append(food)
            else:
                food_list.append(None)

        # highest_bidding_trader = self.traders_list.get_maximal(self.traders_list.get_root())
        # material_to_mine = highest_bidding_trader.item.get_material_selected()

        # 1. match trader profits to cave profits
        # 2. calculate max profit based on what traders are selling
        # 3. add the max profits to an avl
        # 4. from the bottom of avl, push to stack

        emeralds_key = []
        emeralds_avl = AVLTree()
        for cave in self.caves:
            material_in_cave = cave.get_material() #each material
            quantity_in_cave = cave.get_quantity()
            if material_in_cave in self.trader_material_list:
                print("here", material_in_cave)
                index = self.trader_material_list.index(material_in_cave)
                print(self.trader_material_list[index])
                print("the trader",self.traders[index])
                profit = self.traders[index].get_buy_price() * quantity_in_cave
                if profit not in emeralds_key:
                    emeralds_avl.__setitem__(profit, cave)
                    emeralds_key.append(profit)
        
        cave_stack = LinkedStack()
        while emeralds_avl.is_empty() == False:
            the_smallest = emeralds_avl.get_minimal(emeralds_avl.get_root())
            print("smallest",the_smallest)
            emeralds_avl.__delitem__(the_smallest.key)
            cave_stack.push(the_smallest)
        
        profit_list = []
        cave_list = []
        for player in self.players:
            if cave_stack.is_empty() == False:
                big_cave = cave_stack.pop().item
                cave_list.append((big_cave, big_cave.get_quantity()))
                number_of_hunger_bars = big_cave.get_material().get_mining_rate() * big_cave.get_quantity()
                if player.get_hunger_bars() >= number_of_hunger_bars:
                    player.set_hunger_bars(number_of_hunger_bars)
                    profit_list.append(number_of_hunger_bars)
                else:
                    profit_list.append(0)

        return tuple((food_list, profit_list, cave_list))
        
    def verify_output_and_update_quantities(self, foods: Food | None, balances: float, caves: list[tuple[Cave, float]|None]) -> None:
        for 
        
        materials = self.player.get_materials_mined()
        expected_balance = self.player.get_original_hunger_bars() - food.item.get_price()
        for index in range(len(materials)):
            the_material = materials[index][0].get_material() #get the material from the cave
            for trader in range(len(self.traders)):
                if self.traders[trader].get_material_selected() == the_material: #checks whether it is the same material
                    expected_balance += self.traders[trader].get_buy_price() * materials[index][1]

        for cave in range(len(caves)):
            original_cave = caves[cave]
            original_caves_quantity = caves[cave][1]
            quantity_to_check = materials[cave][1]
            if (original_caves_quantity >= quantity_to_check):
                cave_index = self.caves.index(original_cave[0])
                self.caves[cave_index].remove_quantity(quantity_to_check)
            else:
                raise ValueError("The quantities are wrong.")
        print("The quantities are correct.")

        if food != None:
            print("The food is purchasable.")
        else:
            raise ValueError("The food is not purchasable.")

        if (expected_balance == balance):
            print("The balance is correct.")
        else:
            raise ValueError("The balance is wrong.")

if __name__ == "__main__":
    # RandomGen.set_seed(1239087123)
    # g = SoloGame()
    # g.initialise_game()
    # # I'm going to assume you have a `name` attribute on the Materials.
    # print(len(set(map(lambda m: m.name, g.get_materials()))))
    # print(len(g.get_materials()))
    # # Same deal with caves
    # print(len(set(map(lambda c: c.name, g.get_caves()))))
    # print(len(g.get_caves()))
    # # and Traders
    # print(len(set(map(lambda t: t.name, g.get_traders()))))
    # print(len(g.get_traders()))

    # RandomGen.set_seed(1234)
    # g = SoloGame()
    # g.initialise_game()
    # # Spend some time in minecraft
    # # Note that this will crash if you generate a HardTrader with less than 3 materials.
    # for _ in range(3):
    #     g.simulate_day()
    #     g.finish_day()

    # RandomGen.set_seed(16)
    # gold = Material("Gold Nugget", 27.24)
    # netherite = Material("Netherite Ingot", 20.95)
    # fishing_rod = Material("Fishing Rod", 26.93)
    # ender_pearl = Material("Ender Pearl", 13.91)
    # prismarine = Material("Prismarine Crystal", 11.48)

    # materials = [
    #     gold,
    #     netherite,
    #     fishing_rod,
    #     ender_pearl,
    #     prismarine,
    # ]

    # caves = [
    #     Cave("Boulderfall Cave", prismarine, 10),
    #     Cave("Castle Karstaag Ruins", netherite, 4),
    #     Cave("Glacial Cave", gold, 3),
    #     Cave("Orotheim", fishing_rod, 6),
    #     Cave("Red Eagle Redoubt", fishing_rod, 3),
    # ]

    # waldo = RandomTrader("Waldo Morgan")
    # waldo.add_material(fishing_rod)     # Now selling for 7.57
    # orson = RandomTrader("Orson Hoover")
    # orson.add_material(gold)            # Now selling for 4.87
    # lea = RandomTrader("Lea Carpenter")
    # lea.add_material(prismarine)        # Now selling for 5.65
    # ruby = RandomTrader("Ruby Goodman")
    # ruby.add_material(netherite)        # Now selling for 8.54
    # mable = RandomTrader("Mable Hodge")
    # mable.add_material(gold)            # Now selling for 6.7
    
    # traders = [
    #     waldo,
    #     orson,
    #     lea,
    #     ruby,
    #     mable,
    # ]
    
    # for trader in traders:
    #     trader.generate_deal()

    # g = SoloGame()
    # g.initialise_with_data(materials, caves, traders, ["Jackson"], [50])

    # # Avoid simulate_day - This regenerates trader deals and foods.
    # foods = [
    #     Food("Cabbage Seeds", 106, 30),
    #     Food("Fried Rice", 129, 24),
    #     Food("Cooked Chicken Cuts", 424, 19),
    # ]

    # g.player.set_foods(foods)
    # food, balance, caves = g.player.select_food_and_caves()
    
    # print(balance) # 185.01974749350165 - pow(10, -4))
    # # Actual tests will also check your output is possible.

    RandomGen.set_seed(1234)
    materials = [
        Material.random_material()
        for _ in range(400)
    ]
    mat_set = set()
    mining_set = set()
    materials = list(filter(lambda x: (x.name not in mat_set and x.mining_rate not in mining_set) and (mat_set.add(x.name) or mining_set.add(x.mining_rate)) is None, materials))
    caves = [
        Cave.random_cave(materials)
        for _ in range(400)
    ]
    cave_set = set()
    caves = list(filter(lambda x: x.name not in cave_set and cave_set.add(x.name) is None, caves))        
    traders = [
        RandomGen.random_choice([RangeTrader, RandomTrader]).random_trader()
        for _ in range(50)
    ]
    trade_set = set()
    traders = list(filter(lambda x: x.name not in trade_set and trade_set.add(x.name) is None, traders))
    for trader in traders:
        trader.set_all_materials(materials)
    players = [
        RandomGen.random_choice(PLAYER_NAMES)
        for _ in range(20)
    ]
    balances = [
        RandomGen.randint(20, 100)
        for _ in range(20)
    ]
    RandomGen.set_seed(12345)
    g = MultiplayerGame()
    g.initialise_with_data(
        materials,
        caves,
        traders,
        players,
        balances,
    )
    
    # Live a year in minecraft
    for _ in range(365):
        g.simulate_day()
        g.finish_day()