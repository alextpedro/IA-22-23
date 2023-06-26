from ga.individual_int_vector import IntVectorIndividual
from warehouse.cell import Cell
import heapq


class WarehouseIndividual(IntVectorIndividual):

    def __init__(self, problem: "WarehouseProblem", num_genes: int):
        super().__init__(problem, num_genes)

    def compute_fitness(self) -> float:
        # TODO: Compute fitness of WarehouseIndividual
        forklifts = []
        for forklift in self.problem.agent_search.forklifts:
            forklifts.append([])

        current_forklift = 0
        len_products = len(self.problem.products)
        for gene in self.genome:
            if gene <= len_products:
                forklifts[current_forklift].append(gene)
            else:
                current_forklift += 1

        # print(forklifts)

        distances = []
        current_forklift = self.problem.agent_search.forklifts[0]
        for forklift in forklifts:
            previous_cell = forklift
            distance = 0

            for product in forklift:
                product_cell = self.problem.products[
                    product - 1]  # produtos numerados a partir de 1, mas o índice começa no 0
                distance += self.obtain_all_path(previous_cell, product_cell)
                previous_cell = product_cell

            distance += self.obtain_all_path(previous_cell, self.problem.agent_search.exit)

            distances.append(distance)

        distances.sort()
        longest_distance = distances[-1]  # último índice
        sum_distances = 0
        for i in distances:
            sum_distances += i

        # mais penalizado por ter uma distância maior muito alta
        # por exemplo:
        #   ind 1 tem distancias 17 e 5, soma 22
        #   ind 2 tem distancias 11 e 11, soma 22
        #   fitness 1: (17 + 5) + 17 = 39
        #   fitness 2: (11 + 11) + 11 = 33 <- melhor individuo
        self.fitness = sum_distances + longest_distance
        return self.fitness

    def obtain_all_path(self, cell1: Cell, cell2: Cell):  # tem de receber a cell1 e cell2?
        # TODO Obtain all path - distância entre as produtos do pedido
        # Percorre os pares de células:
        for pair in self.problem.agent_search.pairs:
            if (pair.cell1 == cell1 and pair.cell2 == cell2) or (cell2 == pair.cell1 and cell1 == pair.cell2):
                # return self.problem.agent_search.pairs.value
                return pair.value
        return -1

    def __str__(self):
        string = 'Fitness: ' + f'{self.fitness}' + '\n'
        string += str(self.genome) + "\n\n"

        return string

    def better_than(self, other: "WarehouseIndividual") -> bool:
        return True if self.fitness < other.fitness else False

    # __deepcopy__ is implemented here so that all individuals share the same problem instance
    def __deepcopy__(self, memo):
        new_instance = self.__class__(self.problem, self.num_genes)
        new_instance.genome = self.genome.copy()
        new_instance.fitness = self.fitness

        return new_instance
