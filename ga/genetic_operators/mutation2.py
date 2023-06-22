from random import random

from ga.individual_int_vector import IntVectorIndividual
from ga.genetic_operators.mutation import Mutation

class Mutation2(Mutation):
    def __init__(self, probability):
        super().__init__(probability)

    def mutate(self, ind: IntVectorIndividual) -> None:
        # TODO: Mutate 2
        numGenes = ind.num_genes
        random1 = random.randint(0, numGenes - 1)
        random2 = random.randint(0, numGenes - 1)

        while random1 == random2:
            random1 = random.randint(0, numGenes - 1)
            random2 = random.randint(0, numGenes - 1)

        minVal = min(random1, random2)
        maxVal = max(random1, random2)

        geneAux = ind.genome[maxVal]

        for i in range(maxVal, minVal + 1, -1):
            ind.genome[maxVal] = ind.genome[i-1]

        ind.genome[minVal] = geneAux

    def __str__(self):
        return "Mutation 2 (" + f'{self.probability}' + ")"
