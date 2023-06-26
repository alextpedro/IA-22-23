import copy

import constants
from experiments.experiments_factory import ExperimentsFactory
from experiments.experiment import Experiment
from experiments.experiment_listener import ExperimentListener
from ga.genetic_operators.mutationpartialinversion import MutationPartialInversion
from ga.genetic_operators.mutationswitchandshift import MutationSwitchandShift
from ga.selection_methods.tournament import Tournament
from ga.genetic_operators.recombinationcrossovercycle import RecombinationCrossoverCycle
from ga.genetic_operators.recombination_pmx import RecombinationPMX
from ga.genetic_operators.recombinationcrossoverorder1 import RecombinationCrossoverOrder1
from ga.genetic_operators.mutation_insert import MutationInsert
from ga.genetic_algorithm import GeneticAlgorithm
from experiments_statistics.statistic_best_in_run import StatisticBestInRun
from experiments_statistics.statistic_best_average import StatisticBestAverage
from warehouse.cell import Cell
from warehouse.warehouse_agent_search import read_state_from_txt_file, WarehouseAgentSearch
from warehouse.warehouse_problemforGA import WarehouseProblemGA
from warehouse.warehouse_problemforSearch import WarehouseProblemSearch
from warehouse.warehouse_state import WarehouseState


class WarehouseExperimentsFactory(ExperimentsFactory):

    def __init__(self, filename: str):
        super().__init__(filename)
        self.population_size = None
        self.max_generations = None
        self.selection_method = None
        self.recombination_method = None
        self.mutation_method = None
        self.problem = None
        self.experiment = None

    def build_experiment(self) -> Experiment:
        self.num_runs = int(self.get_parameter_value('Runs'))
        self.population_size = int(self.get_parameter_value('Population_size'))
        self.max_generations = int(self.get_parameter_value('Max_generations'))

        # SELECTION
        match self.get_parameter_value('Selection'):
            case 'tournament':
                tournament_size = int(self.get_parameter_value('Tournament_size'))
                self.selection_method = Tournament(tournament_size)

        # RECOMBINATION
        recombination_probability = float(self.get_parameter_value('Recombination_probability'))
        match self.get_parameter_value('Recombination'):
            case 'pmx':
                self.recombination_method = RecombinationPMX(recombination_probability)
            case 'recombinationCrossoverCycle':
                self.recombination_method = RecombinationCrossoverCycle(recombination_probability)
            case 'recombinationCrossoverOrder1':
                self.recombination_method = RecombinationCrossoverOrder1(recombination_probability)

        # MUTATION
        mutation_probability = float(self.get_parameter_value('Mutation_probability'))
        match self.get_parameter_value('Mutation'):
            case 'insert':
                self.mutation_method = MutationInsert(mutation_probability)
            case 'mutationSwitchandShift':
                self.mutation_method = MutationSwitchandShift(mutation_probability)
            case 'mutationPartialInversion':
                self.mutation_method = MutationPartialInversion(mutation_probability)

        # PROBLEM
        matrix, num_rows, num_columns = read_state_from_txt_file(self.get_parameter_value("Problem_file"))

        agent_search = WarehouseAgentSearch(WarehouseState(matrix, num_rows, num_columns))
        # TODO calculate pair distances
        self.calculate_pair_distances(agent_search)

        self.problem = WarehouseProblemGA(agent_search)

        experiment_textual_representation = self.build_experiment_textual_representation()
        experiment_header = self.build_experiment_header()
        experiment_configuration_values = self.build_experiment_values()

        self.experiment = Experiment(
                self,
                self.num_runs,
                self.problem,
                experiment_textual_representation,
                experiment_header,
                experiment_configuration_values)

        self.statistics.clear()
        for statistic_name in self.statistics_names:
            statistic = self.build_statistic(statistic_name, experiment_header)
            self.statistics.append(statistic)
            self.experiment.add_listener(statistic)

        return self.experiment

    def calculate_pair_distances(self, agent: WarehouseAgentSearch):
        for i in range(len(agent.pairs)):
            # Problem novo:
            # Em cada par colocar o fk na cell1
            fk: Cell = agent.pairs[i].cell1
            goal: Cell = copy.copy(agent.pairs[i].cell2)

            # fazer um deepcopy do estado inicial
            estado_inicial: WarehouseState = copy.copy(agent.initial_environment)
            if (fk in agent.forklifts):
                estado_inicial.line_forklift = fk.line
                estado_inicial.column_forklift = fk.column
            else:
                if fk.column +1 < estado_inicial.columns and estado_inicial.matrix[fk.line][fk.column + 1] == constants.EMPTY:
                    estado_inicial.line_forklift = fk.line
                    estado_inicial.column_forklift = fk.column + 1
                else:
                    estado_inicial.line_forklift = fk.line
                    estado_inicial.column_forklift = fk.column - 1

            if goal != agent.exit:
                if goal.column + 1 < estado_inicial.columns and estado_inicial.matrix[goal.line][goal.column + 1] == constants.EMPTY:
                    goal.column += 1
                else:
                    goal.column -= 1

            problem = WarehouseProblemSearch(estado_inicial, goal)
            # aplicar o shearch method com o goal_state
            solution = agent.solve_problem(problem)
            # na solução ir buscar o custo -> este custo vai ser a distancia entre as células dos pares
            agent.pairs[i].value = solution.cost
            agent.pairs[i].positions = solution.positions

    def generate_ga_instance(self, seed: int) -> GeneticAlgorithm:
        ga = GeneticAlgorithm(
                seed,
                self.population_size,
                self.max_generations,
                self.selection_method,
                self.recombination_method,
                self.mutation_method
        )

        for statistic in self.statistics:
            ga.add_listener(statistic)

        return ga

    def build_statistic(self, statistic_name: str, experiment_header: str) -> ExperimentListener:
        if statistic_name == 'BestIndividual':
            return StatisticBestInRun(experiment_header)
        if statistic_name == 'BestAverage':
            return StatisticBestAverage(self.num_runs, experiment_header)

    def build_experiment_textual_representation(self) -> str:
        string = 'Population size: ' + str(self.population_size) + '\r\n'
        string += 'Max generations: ' + str(self.max_generations) + '\r\n'
        string += 'Selection: ' + str(self.selection_method) + '\r\n'
        string += 'Recombination: ' + str(self.recombination_method) + '\r\n'
        string += 'Mutation:' + str(self.mutation_method) + '\r\n'
        return string

    def build_experiment_header(self) -> str:
        string = 'Population size:' + '\t'
        string += 'Max generations: ' + '\t'
        string += 'Selection: ' + '\t'
        string += 'Recombination: ' + '\t'
        string += 'Mutation:' + '\t'
        return string

    def build_experiment_values(self) -> str:
        string = str(self.population_size) + '\t'
        string += str(self.max_generations) + '\t'
        string += str(self.selection_method) + '\t'
        string += str(self.recombination_method) + '\t'
        string += str(self.mutation_method) + '\t'
        return string
