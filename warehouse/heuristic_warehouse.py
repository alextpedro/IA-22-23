import constants
from agentsearch.heuristic import Heuristic
from warehouse.warehouse_problemforSearch import WarehouseProblemSearch
from warehouse.warehouse_state import WarehouseState


class HeuristicWarehouse(Heuristic[WarehouseProblemSearch, WarehouseState]):

    def __init__(self):
        super().__init__()

    def compute(self, state: WarehouseState) -> float:
        h = 0
        for i in range(state.rows):
            for j in range(state.columns):
                tile = state.matrix[i][j]
                # Blank is ignored so that the heuristic is admissible
                if tile != constants.FORKLIFT:
                    tile_goal_line = state.line_exit
                    tile_goal_column = state.column_exit
                    h += abs(i - tile_goal_line) + abs(j - tile_goal_column)
        return h

    def __str__(self):
        return "# TODO"

