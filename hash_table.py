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

        self.conflict_count = 0
        self.probe_total = 0
        self.probe_max = 0
        self.rehash_count = 0

        self.count = 0
        self.expected_size = expected_size
        self.tablesize = tablesize_override

        if self.tablesize == -1:
            self.tablesize = self.expected_size
            self.iterator = LargestPrimeIterator(self.expected_size, self.tablesize)
            self.tablesize = next(self.iterator)
        else:
            self.iterator = LargestPrimeIterator(self.expected_size, self.tablesize)
        # self.tablesize = next(self.iterator)
        # print("what is it?",self.tablesize)

        self.table = ArrayR(max(self.MIN_CAPACITY, self.tablesize))
        
    def hash(self, key: str) -> int:
        """
            Hash a key for insertion into the hashtable.
            :complexity: O(1)
        """

        # value = 0

        # for char in key:
        #     value = (value * self.expected_size + ord(char)) % len(self.table)
        #     print(char, value)

        # return value

        # print(ord(key[0]))
        # print(self.tablesize)
        # print(ord(key[0]) % self.tablesize)

        return (ord(key[0]) % self.tablesize)


    def statistics(self) -> tuple:
        """
            Gets statistics for the hash table

            Returns a tuple containing:
                conflict_count - total number of conflicts
                probe_total - total distance probed throughout execution of code
                probe_max - length of longest probe chain
                rehash_count - total number of times rehashing is done

            :complexity: O(1)
        """
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
        # print("HASHED POSITION", key, position)
        # print("tablesize", self.tablesize)

        if is_insert and self.is_full():
            raise KeyError(key)

        probe_length = 0
        for _ in range(len(self.table)):  # start traversing
            if self.table[position] is None:  # found empty slot
                # print("this is the position",position)
                if is_insert:
                    self.is_linear_probe = True
                    return position
                else:
                    raise KeyError(key)  # so the key is not in
            elif self.table[position][0] == key:  # found key
                return position
            else:  # there is something but not the key, try next
                # print(key, "what")
                position = (position + 1) % len(self.table)
                # print("this is position",key, position)
                probe_length += 1
                self.probe_total += 1
            
            if self.is_linear_probe == True:
                self.conflict_count += 1
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
        # print("POSITION IS HERE:" ,position, key)

        if self.__len__() > self.tablesize // 2:
            self._rehash()
        if self.table[position] is None:
            self.count += 1

        self.table[position] = (key, data)
        # print(self.table[position])

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

            :complexity: O(N) where N is length of self.table
        """

        self.rehash_count += 1
        # print("REHASH COUNT?" ,self.rehash_count)
        self.tablesize = next(self.iterator)
        # print("DOES THE SELF PRIME INCREASE?",self.tablesize)
        new_hash = LinearProbeTable(self.expected_size, self.tablesize)

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
