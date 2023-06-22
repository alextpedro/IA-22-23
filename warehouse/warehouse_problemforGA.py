from ga.problem import Problem
from warehouse.warehouse_agent_search import WarehouseAgentSearch
from warehouse.warehouse_individual import WarehouseIndividual


class WarehouseProblemGA(Problem):
    def __init__(self, agent_search: WarehouseAgentSearch):
        self.forklifts = agent_search.forklifts
        self.products = agent_search.products
        self.agent_search = agent_search

    def generate_individual(self) -> "WarehouseIndividual":
        # TODO: Generate warehouse individuals for problem
        # acho que vou ao WarehouseIndividual e passo quantidade de produtos a ir buscar as prateleiras?
        return WarehouseIndividual(self, self.products.count()+self.forklifts.count()-1)

        # 1 3 5 2 4
        #
        # 1 7 2 3 4 5 6
        #
        # [1  - par/forklift - produto1)  + par(produto 1 - exit)
        # [2 3 4 5 - par/forklift - produto2)  +...+ par(produto 5 - exit)
        # [] - par (forklift - exit)


        # vetor de inteiro para representar genoma

        pass

    def __str__(self):
        string = "# of forklifts: "
        string += f'{len(self.forklifts)}'
        string = "# of products: "
        string += f'{len(self.products)}'
        return string

