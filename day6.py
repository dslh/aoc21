#!/usr/bin/env python3

from get_aoc import get_input_integers

population = [int(age) for age in get_input_integers(6, ',')]

# For efficiency, store the population as a list of the count
# of fish with a certain starting age.
adults = [population.count(i) for i in range(7)]

# Newborn fish spend two days in a juvenile state before joining
# the adult population. We store them in a separate list
juveniles = [0] * 7

def breed(adults, juveniles, day):
    weekday = day % 7
    juveniles[(weekday + 2) % 7] = adults[weekday]
    adults[weekday] += juveniles[weekday]
    juveniles[weekday] = 0

for day in range(80):
    breed(adults, juveniles, day)

print(sum(adults) + sum(juveniles))

for day in range(80, 256):
    breed(adults, juveniles, day)

print(sum(adults) + sum(juveniles))
