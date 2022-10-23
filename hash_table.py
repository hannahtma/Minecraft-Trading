""" Hash Table ADT

Defines a Hash Table using Linear Probing for conflict resolution.
"""
from __future__ import annotations
__author__ = 'Brendon Taylor. Modified by Graeme Gange, Alexey Ignatiev, and Jackson Goerner'
__docformat__ = 'reStructuredText'
__modified__ = '21/05/2020'
__since__ = '14/05/2020'


from referential_array import ArrayR
from typing import TypeVar, Generic
T = TypeVar('T')

from primes import LargestPrimeIterator

class LinearProbeTable(Generic[T]):
    MIN_CAPACITY = 1
    PRIMES = [3, 7, 11, 17, 23, 29, 37, 47, 59, 71, 89, 107, 131, 163, 197, 239, 293, 353, 431, 521, 631, 761, 919,
              1103, 1327, 1597, 1931, 2333, 2801, 3371, 4049, 4861, 5839, 7013, 8419, 10103, 12143, 14591, 17519, 21023,
              25229, 30313, 36353, 43627, 52361, 62851, 75521, 90523, 108631, 130363, 156437, 187751, 225307, 270371,
              324449, 389357, 467237, 560689, 672827, 807403, 968897, 1162687, 1395263, 1674319, 2009191, 2411033,
              2893249, 3471899, 4166287, 4999559, 5999471, 7199369]
    """
        Linear Probe Table.

        attributes:
            count: number of elements in the hash table
            table: used to represent our internal array
            tablesize: current size of the hash table
    """

    def __init__(self, expected_size: int, tablesize_override: int = -1) -> None:
        """
            Initialiser.
            
        """
        self.current_prime = LargestPrimeIterator(tablesize_override, 13)

        self.conflict_count = 0
        self.probe_total = 0
        self.probe_max = 0
        self.rehash_count = 0

        self.count = 0
        self.tablesize = tablesize_override
        if self.tablesize == -1:
            self.tablesize = expected_size

        self.table = ArrayR(self.tablesize)
        
    def hash(self, key: str) -> int:
        """
            Hash a key for insertion into the hashtable.
        """
        alphabets = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

        first_alphabet = key[0]
        print("first alphabet",first_alphabet)
        value = alphabets.index(first_alphabet)
        value = value % len(self.table)

        return value

    def statistics(self) -> tuple:
        return (self.conflict_count, self.probe_total, self.probe_max, self.rehash_count)

    def __len__(self) -> int:
        """
            Returns number of elements in the hash table
            :complexity: O(1)
        """
        return self.count

    def _linear_probe(self, key: str, is_insert: bool) -> int:
        """
            Find the correct position for this key in the hash table using linear probing
            :complexity best: O(K) first position is empty
                            where K is the size of the key
            :complexity worst: O(K + N) when we've searched the entire table
                            where N is the tablesize
            :raises KeyError: When a position can't be found
        """
        position = self.hash(key)  # get the position using hash

        if is_insert and self.is_full():
            raise KeyError(key)

        probe_length = 0
        for _ in range(len(self.table)):  # start traversing
            if self.table[position] is None:  # found empty slot
                if is_insert:
                    self.is_linear_probe = True
                    return position
                else:
                    raise KeyError(key)  # so the key is not in
            if self.is_linear_probe == True:
                self.conflict_count += 1
            elif self.table[position][0] == key:  # found key
                return position
            else:  # there is something but not the key, try next
                position = (position + 1) % len(self.table)
                probe_length += 1
                self.probe_total += 1
            self.is_linear_probe = False

            if probe_length > self.probe_max:
                self.probe_max = probe_length

        raise KeyError(key)

    def keys(self) -> list[str]:
        """
            Returns all keys in the hash table.
        """
        res = []
        for x in range(len(self.table)):
            if self.table[x] is not None:
                res.append(self.table[x][0])
        return res

    def values(self) -> list[T]:
        """
            Returns all values in the hash table.
        """
        res = []
        for x in range(len(self.table)):
            if self.table[x] is not None:
                res.append(self.table[x][1])
        return res

    def __contains__(self, key: str) -> bool:
        """
            Checks to see if the given key is in the Hash Table
            :see: #self.__getitem__(self, key: str)
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: str) -> T:
        """
            Get the item at a certain key
            :see: #self._linear_probe(key: str, is_insert: bool)
            :raises KeyError: when the item doesn't exist
        """
        position = self._linear_probe(key, False)
        return self.table[position][1]

    def __setitem__(self, key: str, data: T) -> None:
        """
            Set an (key, data) pair in our hash table
            :see: #self._linear_probe(key: str, is_insert: bool)
            :see: #self.__contains__(key: str)
        """

        position = self._linear_probe(key, True)

        if self.__len__() > self.tablesize // 2:
            self._rehash()
        if self.table[position] is None:
            self.count += 1

        self.table[position] = (key, data)

    def is_empty(self):
        """
            Returns whether the hash table is empty
            :complexity: O(1)
        """
        return self.count == 0

    def is_full(self):
        """
            Returns whether the hash table is full
            :complexity: O(1)
        """
        return self.count == len(self.table)

    def insert(self, key: str, data: T) -> None:
        """
            Utility method to call our setitem method
            :see: #__setitem__(self, key: str, data: T)
        """
        
        self[key] = data

    def _rehash(self) -> None:
        """
            Need to resize table and reinsert all values
        """

        self.rehash_count += 1
        new_hash = LinearProbeTable(self.current_prime.__next__())

        for item in range(len(self.table)):
            if self.table.__getitem__(item) != None:
                new_hash[str(self.table[item][0])] = self.table[item][1]

        self.count = new_hash.count
        self.table = new_hash.table

    def __str__(self) -> str:
        """
            Returns all they key/value pairs in our hash table (no particular
            order).
            :complexity: O(N) where N is the table size
        """
        result = ""
        for item in self.table:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result

if __name__ == "__main__":
    table = LinearProbeTable(10, tablesize_override=19)
    print(table.__str__())
