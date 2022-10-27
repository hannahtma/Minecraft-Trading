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
    
    @abstractmethod
    def set_materials(self, mats: list[Material]) -> None:
        pass

    @abstractmethod
    def set_caves(self, caves: list[Cave]) -> None:
        pass

    @abstractmethod
    def set_traders(self, traders: list[Trader]) -> None:
        pass
        
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
        for _ in range(amount):
            Material.random_material() 

    def generate_random_caves(self, amount):
        """
        Generates <amount> random caves using Cave.random_cave
        Generated caves must all have different names
        (You may have to call Cave.random_cave more than <amount> times.)
        """
        for _ in range(amount):
            Cave.random_cave(self.get_materials())

    def generate_random_traders(self, amount):
        """
        Generates <amount> random traders by selecting a random trader class
        and then calling <TraderClass>.random_trader()
        and then calling set_all_materials with some subset of the already generated materials.
        Generated traders must all have different names
        (You may have to call <TraderClass>.random_trader() more than <amount> times.)
        """
        for _ in range(amount):
            trader = Trader.random_trader()
            self.traders.__setitem__(trader)
        
        return self.traders

    def finish_day(self):
        """
        DO NOT CHANGE
        Affects test results.
        """
        for cave in self.get_caves():
            if cave.quantity > 0 and RandomGen.random_chance(0.2):
                cave.remove_quantity(RandomGen.random_float() * cave.quantity)
            else:
                cave.add_quantity(RandomGen.random_float() * 10, 2)
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
        Trader.generate_deal()
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
        if self.player.get_balance() > food.get_price():
            food_purchasable = True

    def set_materials(self, mats: list[Material]) -> None:
        print("materials AAAAAAA")
        for material in mats:
            self.materials.__setitem__(material.get_mining_rate(), material)

    def set_caves(self, caves: list[Cave]) -> None:
        print("caves AAAAAAA")
        self.caves = LinearProbeTable(len(caves)-1)
        for cave in caves:
            print("THIS IS OUR CAVE: ",cave)
            # self.caves.__setitem__(cave.get_quantity(), cave)
            print(cave.get_material().get_name())
            self.caves.__setitem__(cave.get_material().get_name(), cave)
        
        print("this is self.caves: ",str(self.caves))

    def set_traders(self, traders: list[Trader]) -> None:
        print("traders AAAAA")
        for trader in traders:
            trader_object = TreeNode(trader.get_buy_price(), trader)
            self.traders.__setitem__(trader_object.key, trader_object.item)

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
        raise NotImplementedError()

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
        raise NotImplementedError()
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
        
            playe

    def verify_output_and_update_quantities(self, foods: Food | None, balances: float, caves: list[tuple[Cave, float]|None]) -> None:
        raise NotImplementedError()

if __name__ == "__main__":

    # r = RandomGen.seed # Change this to set a fixed seed.
    # RandomGen.set_seed(r)
    # print(r)

    # g = SoloGame()
    # g.initialise_game()

    # g.simulate_day()
    # g.finish_day()

    # g.simulate_day()
    # g.finish_day()

    print("this is money: 💰💰💰💰💰")
