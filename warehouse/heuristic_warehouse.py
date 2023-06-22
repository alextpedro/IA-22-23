from agentsearch.heuristic import Heuristic
from warehouse.warehouse_problemforSearch import WarehouseProblemSearch
from warehouse.warehouse_state import WarehouseState


class HeuristicWarehouse(Heuristic[WarehouseProblemSearch, WarehouseState]):

    def __init__(self):
        super().__init__()

    def compute(self, state: WarehouseState) -> float:
        # TODO: Warehouse heuristic. Temp return value.
        # Ir passar a posicao objtivo através do problem para o calculate?
        return state.calculate_distance(self.problem.goal_position)
        # return 1

    def __str__(self):
        return "Distancia entre a prateleira e a Exit \n"

