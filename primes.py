""" Primes

A largest prime number generator and iterator
"""

from __future__ import annotations

__author__ = 'Elysia :D'
__docformat__ = 'reStructuredText'

class LargestPrimeIterator():
    def __init__(self, upper_bound, factor):
        """
        Initialises the 2 arguments needed in the whole class

        Parameters:
        upper_bound - sets the limit of where the loop goes to check the largest prime
        factor - largest prime number multiplies by this to get the next upper bound
        
        Best & Worst Complexity: O(1)
        """
        # makes the parameters into class variables
        self.upper_bound = upper_bound
        self.factor = factor

    def __iter__(self):
        """
        Returns the iterator object

        Best & Worst Complexity: O(1)
        """
        return self

    def __next__(self):
        """
        Returns the next largest prime number depending on the upper bound
        
        Best Complexity: O(n), n =self.upper_bound. When self.upper_bound = 3, does not enter while loop
        Worst Complexity: O(nlogn), n = self.upper_bound. All other times
        """
        for number in range(2, self.upper_bound): # loops from 2 because 1 is not a prime number until the upper bound 
            i = 2 
            prime_flag = True # sets the flag to True
            while (i <= number/2 and prime_flag == True): 
                # checks only the numbers less than equals to half of the number and stops when the number is not prime
                if (number % i == 0): 
                    # if number dividing i produces a remainder of 0, it means the number is divisible and is therefore not a prime
                    prime_flag = False 

                i += 1 # increments i

            if prime_flag == True: # if the number is prime, let largest_prime equals the number
                largest_prime = number    

        # allows the next upper bound to multiply the current largest prime and the factor
        self.upper_bound = largest_prime * self.factor

        return largest_prime

if __name__ == '__main__':
    it1 = LargestPrimeIterator(6,2)
    for i in range(5):
        print(next(it1))
