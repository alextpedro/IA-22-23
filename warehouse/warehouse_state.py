import numpy as np
from PIL.ImageEnhance import Color
from numpy import ndarray

import constants
from agentsearch.state import State
from agentsearch.action import Action
from warehouse.cell import Cell


class WarehouseState(State[Action]):

    def __init__(self, matrix: ndarray, rows, columns):
        super().__init__()

        self.rows = rows
        self.columns = columns
        self.matrix = matrix

        # for i in range(self.rows):
        #     for j in range(self.columns):
        #         self.matrix[i][j] = matrix[i][j]
        #         if self.matrix[i][j] == constants.FORKLIFT:
        #             self.line_forklift = i
        #             self.column_forklift = j
        #         if self.matrix[i][j] == constants.EXIT:
        #             self.line_exit = i
        #             self.column_exit = j


    def calculate_distance(self, goal_position: Cell): # Calcular distância entre objeto e saída
        return abs(goal_position.line - self.line_forklift) + abs(goal_position.column - self.column_forklift)

    def can_move_up(self) -> bool:
        line_up = self.line_forklift - 1
        if line_up >= 0:
            cell_up = self.matrix[line_up][self.column_forklift]
            if cell_up != constants.SHELF and cell_up != constants.PRODUCT:
                return True
        return False

    def can_move_right(self) -> bool:
        col_right = self.column_forklift + 1
        if col_right < self.columns:
            cell_right = self.matrix[self.line_forklift][col_right]
            if cell_right != constants.SHELF and cell_right != constants.PRODUCT:
                return True
        return False

    def can_move_down(self) -> bool:
        line_down = self.line_forklift + 1
        if line_down < self.rows:
            cell_down = self.matrix[line_down][self.column_forklift]
            if cell_down != constants.SHELF and cell_down != constants.PRODUCT:
                return True
        return False

    def can_move_left(self) -> bool:
        col_left = self.column_forklift - 1
        if col_left >= 0:
            cell_left = self.matrix[self.line_forklift][col_left]
            if cell_left != constants.SHELF and cell_left != constants.PRODUCT:
                return True
        return False

    def move_up(self) -> None:
        self.line_forklift -= 1

    def move_right(self) -> None:
        self.column_forklift += 1

    def move_down(self) -> None:
        self.line_forklift += 1

    def move_left(self) -> None:
        self.column_forklift -= 1

    def get_cell_color(self, row: int, column: int) -> Color:
        if self.matrix[row][column] == constants.EXIT:
            return constants.COLOREXIT

        if self.matrix[row][column] == constants.PRODUCT_CATCH:
            return constants.COLORSHELFPRODUCTCATCH

        if self.matrix[row][column] == constants.PRODUCT:
            return constants.COLORSHELFPRODUCT

        switcher = {
            constants.FORKLIFT: constants.COLORFORKLIFT,
            constants.SHELF: constants.COLORSHELF,
            constants.EMPTY: constants.COLOREMPTY
        }
        return switcher.get(self.matrix[row][column], constants.COLOREMPTY)

    def __str__(self):
        matrix_string = str(self.rows) + " " + str(self.columns) + "\n"
        for row in self.matrix:
            for column in row:
                matrix_string += str(column) + " "
            matrix_string += "\n"
        return matrix_string

    def __eq__(self, other):
        if isinstance(other, WarehouseState):
            return self.line_forklift == other.line_forklift and self.column_forklift == other.column_forklift
        return NotImplemented

    def __hash__(self):
        return hash(self.matrix.tostring())
