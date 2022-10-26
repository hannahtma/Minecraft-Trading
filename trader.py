from __future__ import annotations

from abc import abstractmethod, ABC
from material import Material
from random_gen import RandomGen
from avl import AVLTree

# Generated with https://www.namegenerator.co/real-names/english-name-generator
TRADER_NAMES = [
    "Pierce Hodge",
    "Loren Calhoun",
    "Janie Meyers",
    "Ivey Hudson",
    "Rae Vincent",
    "Bertie Combs",
    "Brooks Mclaughlin",
    "Lea Carpenter",
    "Charlie Kidd",
    "Emil Huffman",
    "Letitia Roach",
    "Roger Mathis",
    "Allie Graham",
    "Stanton Harrell",
    "Bert Shepherd",
    "Orson Hoover",
    "Lyle Randall",
    "Jo Gillespie",
    "Audie Burnett",
    "Curtis Dougherty",
    "Bernard Frost",
    "Jeffie Hensley",
    "Rene Shea",
    "Milo Chaney",
    "Buck Pierce",
    "Drew Flynn",
    "Ruby Cameron",
    "Collie Flowers",
    "Waldo Morgan",
    "Winston York",
    "Dollie Dickson",
    "Etha Morse",
    "Dana Rowland",
    "Eda Ryan",
    "Audrey Cobb",
    "Madison Fitzpatrick",
    "Gardner Pearson",
    "Effie Sheppard",
    "Katherine Mercer",
    "Dorsey Hansen",
    "Taylor Blackburn",
    "Mable Hodge",
    "Winnie French",
    "Troy Bartlett",
    "Maye Cummings",
    "Charley Hayes",
    "Berta White",
    "Ivey Mclean",
    "Joanna Ford",
    "Florence Cooley",
    "Vivian Stephens",
    "Callie Barron",
    "Tina Middleton",
    "Linda Glenn",
    "Loren Mcdaniel",
    "Ruby Goodman",
    "Ray Dodson",
    "Jo Bass",
    "Cora Kramer",
    "Taylor Schultz",
]

class Trader(ABC):
    
    def __init__(self, name: str) -> None:
        if name not in TRADER_NAMES:
            self.name = Trader.random_trader()
        else:
            self.name = name

    @classmethod
    def random_trader(cls):
        return RandomGen.random_choice(TRADER_NAMES)
    
    def set_all_materials(self, mats: list[Material]) -> None:
        self.materials = AVLTree()
        for material in mats:
            self.materials.insert_aux(None,material.get_mining_rate(),material)
    
    def add_material(self, mat: Material) -> None:
        self.materials.insert_aux(None,mat.get_mining_rate(),mat)
    
    def is_currently_selling(self) -> bool:
        pass

    def current_deal(self) -> tuple[Material, float]:
        return tuple(self.material_selected)
    
    @abstractmethod
    def generate_deal(self) -> None:
        pass

    def stop_deal(self) -> None:
        raise NotImplementedError()
    
    def __str__(self) -> str:
        raise NotImplementedError()

class RandomTrader(Trader):
    
    def generate_deal(self) -> None:
        self.material_selected =  RandomGen.random_choice(self.materials)
        self.buy_price = round(2 + 8 * RandomGen.random_float(), 2)

class RangeTrader(Trader):

    def sortFn(self, material_list):
        return material_list

    def generate_deal(self) -> None:
        i = RandomGen.randint(1,len(self.materials))
        j = RandomGen.randint(i,len(self.materials))
        self.material_selected = RandomGen.random_choice(RangeTrader.materials_between(i,j))
        self.buy_price = round(2 + 8 * RandomGen.random_float(), 2)
    
    def materials_between(self, i: int, j: int) -> list[Material]:
        return self.materials.range_between(i,j)

class HardTrader(Trader):
    
    pass

if __name__ == "__main__":
    trader = RangeTrader("Jackson")
    print(trader)
    trader.set_materials([
        Material("Coal", 4.5),
        Material("Diamonds", 3),
        Material("Redstone", 20),
    ])
    trader.generate_deal()
    print(trader)
    trader.stop_deal()
    print(trader)

