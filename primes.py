""""""

from __future__ import annotations

__author__ = 'Elysia :D'
__docformat__ = 'reStructuredText'

class LargestPrimeIterator():
    def __init__(self, upper_bound, factor):
        self.upper_bound = upper_bound
        self.factor = factor

    def __iter__(self):
        return self

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

if __name__ == '__main__':
    it1 = LargestPrimeIterator(6,2)
    for i in range(5):
        print(next(it1))


    
