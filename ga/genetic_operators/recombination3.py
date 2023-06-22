from random import random

from ga.genetic_operators.recombination import Recombination
from ga.individual import Individual

class Recombination3(Recombination):

    def __init__(self, probability: float):
        super().__init__(probability)

    def recombine(self, ind1: Individual, ind2: Individual) -> None:
        # TODO Recombine 3
        child1 = len([0] * ind1.genome)
        child2 = len([0] * ind2.genome)
        visited = {}
        position1 = position2 = 0

        while position1 == position2:
            position1 = random.randint(0, ind1.genome.length - 1)
            position2 = random.randint(0, ind1.genome.length - 1)

        if position1 > position2:
            position1, position2 = position2, position1

        self.createSegment(ind1, child1, visited, position1, position2)
        self.reorder(ind1, ind2, child1, visited, True, position2)
        self.createSegment(ind2, child2, visited, position1, position2)
        self.reorder(ind1, ind2, child2, visited, False, position2)

        self.changePositions(ind1, child1)
        self.changePositions(ind2, child2)

        visited.clear()

    def createSegment(ind: Individual, child, visited, position1, position2):
        for i in range(position1 + 1, position2 + 1):
            value = ind.genome[i]
            child[i] = value
            visited[value] = value

    def reorder(ind1: Individual, ind2: Individual, child, visited, isImpar: bool, position2, position1):
        fatherPos = position2 + 1
        childPos = position2 + 1
        count = position2 - position1
        value = 0
        while count < len(child):
            if fatherPos > ind1.genome.length() - 1:
                fatherPos = 0

            if childPos > len(child) - 1:
                childPos = 0

            if isImpar:
                value = ind2.genome[fatherPos]
                if value not in visited:
                    child[childPos] = value
                    visited[value] = value
                    childPos += 1
                    count += 1
            else:
                value = ind1.genome[fatherPos]
                if value not in visited:
                    child[childPos] = value
                    visited[value] = value
                    childPos += 1
                    count += 1

            fatherPos += 1

        visited.clear()

    def changePositions(ind: Individual, child: Individual):
        for i in range(ind.num_genes):
            ind.swap_genes(i, child[i])

    def __str__(self):
        return "Recombination Order One (" + f'{self.probability}' + ")"