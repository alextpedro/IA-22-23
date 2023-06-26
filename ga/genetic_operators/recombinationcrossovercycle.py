from ga.individual import Individual
from ga.genetic_operators.recombination import Recombination

class RecombinationCrossoverCycle(Recombination):

    def __init__(self, probability: float):
        super().__init__(probability)
        indexes = []

    def recombine(self, ind1: Individual, ind2: Individual) -> None:
        # TODO Recombine 2
        idx = 0
        item = 0
        aux = 0
        indexes = []

        while True:
            indexes.append(idx)
            item = ind2.genome[idx]
            idx = ind1.index(item)
            if idx in indexes:
                break

        for i in range(len(indexes)):
            aux = ind1.genome[indexes[i]]
            ind1.genome[indexes[i]] = ind2.genome[indexes[i]]
            ind2.genome[indexes[i]] = aux

        indexes.clear()

    def __str__(self):
        return "Recombination 2 (" + f'{self.probability}' + ")"
