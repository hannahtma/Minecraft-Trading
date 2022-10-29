from __future__ import annotations
from abc import abstractmethod
from xml.etree.ElementPath import xpath_tokenizer_re
from hash_table import LinearProbeTable
from node import TreeNode

from player import Player
from trader import Trader
from material import Material
from cave import Cave
from food import Food
from random_gen import RandomGen
from avl import AVLTree
from trader import RandomTrader, RangeTrader, HardTrader

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
        self.materials = AVLTree()
        self.traders = AVLTree()

    def initialise_game(self) -> None:
        """Initialise all game objects: Materials, Caves, Traders."""
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
        self.set_materials(materials)
        self.set_caves(caves)
        self.set_traders(traders)
    
    def set_materials(self, mats: list[Material]) -> None:
        self.materials_key_list = []
        for material in mats:
            self.materials.__setitem__(material.get_mining_rate(), material)
            self.materials_key_list.append(material.get_mining_rate())

    def set_caves(self, caves: list[Cave]) -> None:
        self.caves = LinearProbeTable(len(caves))
        # print("we are here",caves)
        # print("THIS IS LEN(CAVES)", len(caves))
        for cave in caves:
            # print("THIS IS OUR CAVE: ",cave)
            # self.caves.__setitem__(cave.get_quantity(), cave)
            # print(cave.get_name())
            self.caves.__setitem__(cave.get_name(), cave)
        
        # print("this is self.caves: ",str(self.caves))

    def set_traders(self, traders: list[Trader]) -> None:
        self.traders_key_list = []
        for trader in traders:
            trader.generate_deal()
            # print(trader)
            self.traders.__setitem__(trader.get_buy_price(), trader)
            self.traders_key_list.append(trader.get_buy_price())
        # print(self.traders_key_list)
        
    def get_materials(self) -> list[Material]:
        return self.materials

    def get_caves(self) -> list[Cave]:
        return self.caves.values()

    def get_traders(self) -> list[Trader]:
        return self.traders

    def generate_random_materials(self, amount):
        """
        Generates <amount> random materials using Material.random_material
        Generated materials must all have different names and different mining_rates.
        (You may have to call Material.random_material more than <amount> times.)
        """
        self.materials_generated = []
        material_names = []
        material_mining_times = []
        number = 0
        while number < amount:
            material_to_add = Material.random_material()
            if material_to_add.get_name() not in material_names and material_to_add.get_mining_rate() not in material_mining_times:
                self.materials_generated.append(material_to_add)
                material_names.append(material_to_add.get_name())
                material_mining_times.append(material_to_add.get_mining_rate())
                number += 1

    def generate_random_caves(self, amount):
        """
        Generates <amount> random caves using Cave.random_cave
        Generated caves must all have different names
        (You may have to call Cave.random_cave more than <amount> times.)
        """
        random_caves = []
        for _ in range(amount):
            cave = Cave.random_cave(self.materials_generated)
            random_caves.append(cave)
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
            trader.set_all_materials(self.materials_generated)
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
        super().initialise_game()
        self.player = Player.random_player()
        self.player.set_materials(self.get_materials())
        self.player.set_caves(self.get_caves())
        self.player.set_traders(self.get_traders())

    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader], player_names: list[int], emerald_info: list[float]):
        super().initialise_with_data(materials, caves, traders)
        self.player = Player(player_names[0], emeralds=emerald_info[0])
        self.player.set_materials(self.get_materials())
        self.player.set_caves(self.get_caves())
        self.player.set_traders(self.get_traders())

    def simulate_day(self):
        # 1. Traders make deals
        for trader_key in self.traders_key_list:
            trader = self.traders.__getitem__(trader_key)
            trader.generate_deal()
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
        if food == self.player.get_foods().get_maximal(self.player.get_foods().root):
            food_purchasable = True
        
        materials = self.player.get_materials_sold()

        for cave in range(len(caves)):
            the_cave = caves[cave]
            print("we are here",the_cave)
            # the_cave.get_quantity() = the_cave.get_quantity() - materials.index(caves[cave][0])[1]
        print(caves)

class MultiplayerGame(Game):

    MIN_PLAYERS = 2
    MAX_PLAYERS = 5

    def __init__(self) -> None:
        super().__init__()
        self.players = []

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
                self.materials_generated.append(player_to_add)
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
        for trader_key in self.traders_key_list:
            trader = self.traders.__getitem__(trader_key)
            trader.generate_deal()
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
            player.select_food_and_caves()

    def verify_output_and_update_quantities(self, foods: Food | None, balances: float, caves: list[tuple[Cave, float]|None]) -> None:
        raise NotImplementedError()

if __name__ == "__main__":
    RandomGen.set_seed(1239087123)
    g = SoloGame()
    g.initialise_game()
    # I'm going to assume you have a `name` attribute on the Materials.
    print(len(set(map(lambda m: m.name, g.get_materials()))))
    print(len(g.get_materials()))
    # Same deal with caves
    print(len(set(map(lambda c: c.name, g.get_caves()))))
    print(len(g.get_caves()))
    # and Traders
    print(len(set(map(lambda t: t.name, g.get_traders()))))
    print(len(g.get_traders()))

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
    
    # self.assertGreaterEqual(balance, 185.01974749350165 - pow(10, -4))
    # # Actual tests will also check your output is possible.
