from ga.individual_int_vector import IntVectorIndividual

SEPARATOR = 0

class WarehouseIndividual(IntVectorIndividual):

    def __init__(self, problem: "WarehouseProblem", num_genes: int):
        super().__init__(problem, num_genes)
        self.genome = []
        self.fitness = 0

    def initialize(self):
        # Ideia: agente - produtos - separador e repete
        for forklift in range(len(self.problem.forklifts)):
            self.genome.append(forklift)
            self.genome.append(self.problem.products) # talvez randomizar ordem?
            self.genome.append(SEPARATOR)
        pass

    def compute_fitness(self) -> float:
        # TODO: Compute fitness of WarehouseIndividual
        return 1

    def obtain_all_path(self):
        # TODO Obtain all path
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