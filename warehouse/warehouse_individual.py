from ga.individual_int_vector import IntVectorIndividual

class WarehouseIndividual(IntVectorIndividual):

    def __init__(self, problem: "WarehouseProblem", num_genes: int):
        super().__init__(problem, num_genes)

    def compute_fitness(self) -> float:
        # TODO: Compute fitness of WarehouseIndividual
        # Colocar a fitness a 0
        self.fitness = 0

        # obter a fitness: será a distância do caminho entre a cell1 e cell2

        # percorrer o genoma
            # fitness =

        # Variáveis
        # cellAgent = problem.                      # celula do fk ou agente
        # shelves = problem.                        # onde tem shelves
        # exit = problem.                           # saida

        # Obter a fitness
        # fitness = obtain_all_path(cellAgent, shelves[genome[0] - 1])
        #
        # for i in range(len(genome) - 1):
        #     fitness += obtain_all_path(shelves[genome[i] - 1], shelves[genome[i + 1] - 1])
        #
        # fitness += obtain_all_path(shelves[genome[len(genome) - 1] - 1], exit)

        # 1 - percorrer genoma e separar produtos

        return 0 #fitness

    def obtain_all_path(self): # tem de receber a cell1 e cell2?
        # TODO Obtain all path - distância entre as prateleiras do pedido?
        # Percorre os pares de células:
        # for pair in self.agent.pairs:
        #     if (pair.cell1 == cell1 and pair.cell2 == cell2) or ( cell2 == pair.cell1 and cell1 == pair.cell2):
        #         return self.agent.pairs.value
        # return -1
        pass

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