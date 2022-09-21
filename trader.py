from __future__ import annotations

from abc import abstractmethod, ABC
from material import Material
from random_gen import RandomGen

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
        raise NotImplementedError()

    @classmethod
    def random_trader(cls):
        raise NotImplementedError()
    
    def set_all_materials(self, mats: list[Material]) -> None:
        raise NotImplementedError()
    
    def add_material(self, mat: Material) -> None:
        raise NotImplementedError()
    
    def is_currently_selling(self) -> bool:
        raise NotImplementedError()

    def current_deal(self) -> tuple[Material, float]:
        raise NotImplementedError()
    
    def generate_deal(self) -> None:
        raise NotImplementedError()

    def stop_deal(self) -> None:
        raise NotImplementedError()
    
    def __str__(self) -> str:
        raise NotImplementedError()

class RandomTrader(Trader):
    
    pass

class RangeTrader(Trader):
    
    def materials_between(self, i: int, j: int) -> list[Material]:
        raise NotImplementedError()

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

