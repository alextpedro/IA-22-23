
from abc import abstractmethod
from random import shuffle

from ga.problem import Problem
from ga.individual import Individual

class IntVectorIndividual(Individual):

    def __init__(self, problem: Problem, num_genes: int):
        super().__init__(problem, num_genes)
        # Fazer aqui o self.genome
        # vai ter nuúmero de 1 a num_genes
        # ver o shuffle para baralhar vetor
        # print do self.genome para ver se está ok
        vetor_aux = list(range(1,  num_genes + 1))
        shuffle(vetor_aux)
        self.genome = vetor_aux
        # print(self.genome)

    def swap_genes(self, other, index: int):
        aux = self.genome[index]
        self.genome[index] = other.genome[index]
        other.genome[index] = aux

    @abstractmethod
    def compute_fitness(self) -> float:
        pass

    @abstractmethod
    def better_than(self, other: "IntVectorIndividual") -> bool:
        pass
