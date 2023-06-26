from ga.individual_int_vector import IntVectorIndividual
from warehouse.cell import Cell
import heapq


class WarehouseIndividual(IntVectorIndividual):

    def __init__(self, problem: "WarehouseProblem", num_genes: int):
        super().__init__(problem, num_genes)

    def compute_fitness(self) -> float:
        # TODO: Compute fitness of WarehouseIndividual

        fk = self.problem.agent_search.forklifts
        products = self.problem.agent_search.products

        fitness = self.obtain_all_path(fk, self.genome[0] - 1)

        for i in range(len(self.genome)):
            fitness += self.obtain_all_path(self.problem.products[self.genome[i] - 1],
                                            self.problem.products[self.genome[i + 1] - 1])

        fitness += self.obtain_all_path(self.problem.products[self.genome[len(self.genome) - 1] - 1])

        return fitness

    def obtain_all_path(self, cell1: Cell, cell2: Cell): # tem de receber a cell1 e cell2?
        # TODO Obtain all path - distância entre as produtos do pedido
        # Percorre os pares de células:
        for pair in self.problem.agent_search.pairs:
            if (pair.cell1 == cell1 and pair.cell2 == cell2) or ( cell2 == pair.cell1 and cell1 == pair.cell2):
                return self.problem.agent_search.pairs.value
        return -1


    def __str__(self):
        string = 'Fitness: ' + f'{self.fitness}' + '\n'
        string += str (self.genome) + "\n\n"

        return string

    def better_than(self, other: "WarehouseIndividual") -> bool:
        return True if self.fitness < other.fitness else False

    # __deepcopy__ is implemented here so that all individuals share the same problem instance
    def __deepcopy__(self, memo):
        new_instance = self.__class__(self.problem, self.num_genes)
        new_instance.genome = self.genome.copy()
        new_instance.fitness = self.fitness

        return new_instance