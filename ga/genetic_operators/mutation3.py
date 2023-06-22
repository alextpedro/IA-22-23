import copy
from random import random

from ga.individual_int_vector import IntVectorIndividual
from ga.genetic_operators.mutation import Mutation

class Mutation3(Mutation):
    def __init__(self, probability):
        super().__init__(probability)

    def mutate(self, ind: IntVectorIndividual) -> None:
        # TODO Mutate 3
        numGenes = ind.num_genes
        random1 = random.randint(0, numGenes - 1)
        random2 = random.randint(0, numGenes - 1)
        j = 0

        ind2 = copy.deepcopy(ind)

        while random1 == random2:
            random1 = random.randint(0, numGenes - 1)
            random2 = random.randint(0, numGenes - 1)

        minVal = j = min(random1, random2)
        maxVal = max(random1, random2)

        for i in range(maxVal, minVal - 1, -1):
            ind.genome[j] = ind2.genome[i]
            j += 1

    def __str__(self):
        return "Mutation 3 (" + f'{self.probability}' + ")"
