""""""

from __future__ import annotations

__author__ = ''
__docformat__ = 'reStructuredText'

class LargestPrimeIterator():
    def __init__(self, upper_bound, factor):
        self.upper_bound = upper_bound
        self.factor = factor
        self.largest_prime = 0

    def __next__(self):
        for number in range(2, self.upper_bound):
            i = 2
            prime_flag = True
            while (i <= number/2 and prime_flag == True):
                if (number % i == 0):
                    prime_flag = False
                i += 1

            if prime_flag == True:
                self.largest_prime = number

        self.upper_bound = self.largest_prime * self.factor

        return self.largest_prime
    
    def __iter__(self):
        return self
