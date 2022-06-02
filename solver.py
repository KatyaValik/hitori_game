import numpy as np
import datetime


class Solver:
    def __init__(self, data):
        self.data = data
        self.value_array = None
        self.mark_array = None
        self.virtual_mark_array = None
        self.all_id_list = None
        self.row_count = 0
        self.column_count = 0
        self.time_diff = 0
        self.game_over = False
        self.has_solution = True

    def mark_unique(self, cell_id):
        """ Помечает все значения как circle, если они уникальны в строке и в столбце """
        if (self.value_array[cell_id[0], ...].tolist().count(self.value_array[cell_id]) == 1) and (
                self.value_array[..., cell_id[1]].tolist().count(self.value_array[cell_id]) == 1):
            self.mark_array[cell_id] = 'circle'

    def is_border_cell(self, cell_id):
        """ Возвращает значение True, если ячейка находится на границе игрового поля """
        if (cell_id[0] == 0 or cell_id[1] == 0) or (
                cell_id[0] == self.row_count - 1 or cell_id[1] == self.column_count - 1):
            return True
        else:
            return False

    def id_exists(self, cell_id):
        """ Проверяет, существует ли ячейка с переданным идентификатором """
        if (0 <= cell_id[0] < self.row_count) and (
                0 <= cell_id[1] < self.column_count):
            return True
        else:
            return False

    def get_diagonal_neighbour(self, cell_id, mark_array_copy, only_dark=False):
        """ Возвращает идентификатор(ы) ячейки диагонального соседа(cell_id) в виде списка
         Если флаг only_dark равен True, возвращает только dark соседей"""
        all_diagonal_id = [(cell_id[0] + 1, cell_id[1] - 1), (cell_id[0] + 1, cell_id[1] + 1),
                           (cell_id[0] - 1, cell_id[1] - 1), (cell_id[0] - 1, cell_id[1] + 1)]
        result = []
        for _id in all_diagonal_id:
            if self.id_exists(_id):
                if only_dark:
                    if mark_array_copy[_id] == 'dark':
                        result.append(_id)
                else:
                    result.append(_id)
        return result

    def mark_circle(self, cell_id):
        """ Помечает яцейку как circle в mark_array и помечает dark ячейки с таким же значением по горизонтали и
        вертикали """
        if self.mark_array[cell_id] != 'blank':
            return None

        self.mark_array[cell_id] = 'circle'
        circled_value = self.value_array[cell_id]

        for num in range(self.column_count):
            id_1 = (cell_id[0], num)
            if self.mark_array[id_1] == 'blank':
                if self.value_array[id_1] == circled_value:
                    self.mark_dark(id_1)
        for num_1 in range(self.row_count):
            id_2 = (num_1, cell_id[1])
            if self.mark_array[id_2] == 'blank':
                if self.value_array[id_2] == circled_value:
                    self.mark_dark(id_2)

    def mark_dark(self, cell_id):
        """ Помечает ячейку dark в mark_array, а всех ее соседей circle """
        if self.mark_array[cell_id] != 'blank':
            return None

        self.mark_array[cell_id] = 'dark'
        row_column_neighbour = [(cell_id[0], cell_id[1] - 1),
                                (cell_id[0], cell_id[1] + 1),
                                (cell_id[0] - 1, cell_id[1]),
                                (cell_id[0] + 1, cell_id[1])]

        for _id in row_column_neighbour:
            if self.id_exists(_id):
                self.mark_virtual_circle(_id)
                if not self.virtual_error_occured():
                    self.mark_circle(_id)
                else:
                    self.has_solution = False

    def mark_virtual_circle(self, cell_id):
        """ Помечает ячейку circle в virtual_mark_array и все ячейки с таким же значением в колонке и строке помечает
        dark в virtual_mark_array """
        if self.virtual_mark_array[cell_id] != 'blank':
            return None

        self.virtual_mark_array[cell_id] = 'circle'
        circled_value = self.value_array[cell_id]

        for num in range(self.column_count):
            id_1 = (cell_id[0], num)
            if self.virtual_mark_array[id_1] == 'blank':
                if self.value_array[id_1] == circled_value:
                    self.mark_virtual_dark(id_1)
                    if not self.virtual_error_occured():
                        self.mark_virtual_dark(id_1)

        for num_1 in range(self.row_count):
            id_2 = (num_1, cell_id[1])
            if self.virtual_mark_array[id_2] == 'blank':
                if self.value_array[id_2] == circled_value:
                    self.mark_virtual_dark(id_2)
                    if not self.virtual_error_occured():
                        self.mark_virtual_dark(id_2)

    def mark_virtual_dark(self, cell_id):
        """ Помечает ячейку dark в virtual_mark_array и всех ее соседей помечает circle в virtual_mark_array """
        if self.virtual_mark_array[cell_id] != 'blank':
            return None

        self.virtual_mark_array[cell_id] = 'dark'

        row_column_neighbour = [(cell_id[0], cell_id[1] - 1),
                                (cell_id[0], cell_id[1] + 1),
                                (cell_id[0] - 1, cell_id[1]),
                                (cell_id[0] + 1, cell_id[1])]
        for _id in row_column_neighbour:
            if self.id_exists(_id):
                self.mark_virtual_circle(_id)

    def virtual_error_occured(self):
        """ Проверяет каждую ошибку, которая может возникнуть в virtual_mark_array если неправильно отметили ячейку
        circle или dark """
        for _id in self.all_id_list:
            # проверяем, не нарушена ли связность circled ячеек
            if self.loop_form_if_darken(_id, self.virtual_mark_array) and self.virtual_mark_array[_id] == 'dark':
                return True
            # проверяем, нет ли соседних по вертикали или горизонтали ячеек, помеченных dark
            if self.virtual_mark_array[_id] == 'dark':
                row_column_neighbour = [(_id[0], _id[1] - 1),
                                        (_id[0], _id[1] + 1),
                                        (_id[0] - 1, _id[1]),
                                        (_id[0] + 1, _id[1])]
                for id_ in row_column_neighbour:
                    if self.id_exists(id_):
                        if self.virtual_mark_array[id_] == 'dark':
                            return True

        # проверяем, нет ли нескольких ячеек в одной колонке с одинаковыми значениями, помеченных circle
        for index in range(self.column_count):
            column_value_array = self.value_array[..., index]
            column_mark_array = self.virtual_mark_array[..., index]
            column_circled_values = column_value_array[
                column_mark_array == 'circle']
            if len(column_circled_values.tolist()) != len(
                    set(column_circled_values.tolist())):
                return True
        # проверяем, нет ли нескольких ячеек в одной строке с одинаковыми значениями, помеченных circle
        for index in range(self.row_count):
            row_value_array = self.value_array[index, ...]
            row_mark_array = self.virtual_mark_array[index, ...]
            row_circled_values = row_value_array[row_mark_array == 'circle']
            if len(row_circled_values.tolist()) != len(
                    set(row_circled_values.tolist())):
                return True

    def check_for_dark(self, cell_id):
        """ Проверяет, должа ли клетка быть помечена dark (в одной и той же строке (столбце) находятся одинаковые
        значения, равные значению cell_value. Если ячейка будет circle, будет две соседние клетки dark в одном
        ряду, что недопустимо, поэтому эта клетка должна быть dark) """
        if self.mark_array[cell_id] != 'blank':
            return None

        cell_value = self.value_array[cell_id]

        for i in range(self.column_count - 1):
            id_1 = (cell_id[0], i)
            id_right = (cell_id[0], i + 1)
            if id_1 == cell_id or id_right == cell_id:
                pass
            else:
                if (self.mark_array[id_1] == 'blank') and (
                        self.mark_array[id_right] == 'blank'):
                    if (self.value_array[id_1] == cell_value) and (
                            self.value_array[
                                id_right] == cell_value):
                        self.mark_dark(cell_id)

        for j in range(self.row_count - 1):
            id_2 = (j, cell_id[1])
            id_down = (j + 1, cell_id[1])
            if id_2 == cell_id or id_down == cell_id:
                pass
            else:
                if (self.mark_array[id_2] == 'blank') and (
                        self.mark_array[id_down] == 'blank'):
                    if (self.value_array[id_2] == cell_value) and (
                            self.value_array[
                                id_down] == cell_value):
                        self.mark_dark(cell_id)

    def check_for_dark_advanced(self, cell_id):

        if self.mark_array[cell_id] != 'blank':
            return None

        for _id in self.all_id_list:
            self.virtual_mark_array[_id] = self.mark_array[_id]

        self.mark_virtual_circle(cell_id)

        if self.virtual_error_occured():
            self.mark_dark(cell_id)

        for _id in self.all_id_list:
            if self.loop_form_if_darken(_id, self.virtual_mark_array) and self.virtual_mark_array[_id] == 'blank':
                self.mark_virtual_circle(_id)

            if self.virtual_error_occured():
                self.mark_dark(cell_id)

    def check_for_circle_advanced(self, cell_id):
        if self.mark_array[cell_id] != 'blank':
            return None

        for _id in self.all_id_list:
            self.virtual_mark_array[_id] = self.mark_array[
                _id]

        self.mark_virtual_dark(cell_id)

        if self.virtual_error_occured():
            self.mark_circle(cell_id)

        for _id in self.all_id_list:
            if self.loop_form_if_darken(_id, self.virtual_mark_array) and self.virtual_mark_array[_id] == 'blank':
                self.mark_virtual_circle(_id)

            if self.virtual_error_occured():
                self.mark_circle(cell_id)

    def loop_form_if_darken(self, cell_id, mark_array_copy):
        """ проверяет, прерываются ли значения, обведенные кружком, затемненными ячейками в mark_array_copy,
        если ячейка помечена dark """
        connected_blacks = [cell_id]
        checked_cells = []
        border_flag = self.is_border_cell(cell_id)

        while len(connected_blacks) > 0:
            new_black_connections = []
            for black_id in connected_blacks:
                neighbours = self.get_diagonal_neighbour(black_id, mark_array_copy, True)
                for _id in neighbours:
                    if _id not in checked_cells:
                        new_black_connections.append(_id)

            for id_ in new_black_connections:
                if self.is_border_cell(id_):
                    if border_flag:
                        return True
                    else:
                        border_flag = True
                if new_black_connections.count(id_) >= 2:
                    return True

            checked_cells += connected_blacks
            connected_blacks = new_black_connections

        return False

    def check_for_circle(self, cell_id):
        """ Проверяет, нужно ли пометить ячейку circle """
        if self.mark_array[cell_id] != 'blank':
            return None
        left_cell = (cell_id[0], cell_id[1] - 1)
        right_cell = (cell_id[0], cell_id[1] + 1)
        up_cell = (cell_id[0] - 1, cell_id[1])
        down_cell = (cell_id[0] + 1, cell_id[1])

        if self.id_exists(left_cell) and self.id_exists(right_cell):
            if self.value_array[left_cell] == self.value_array[right_cell]:
                self.mark_circle(cell_id)

        if self.id_exists(up_cell) and self.id_exists(down_cell):
            if self.value_array[up_cell] == self.value_array[down_cell]:
                self.mark_circle(cell_id)

        if self.loop_form_if_darken(cell_id, self.mark_array):
            self.mark_circle(cell_id)

    def check_angle_for_dark(self, cell_id):
        if (cell_id[0] == 0 and cell_id[1] == 0) or (
                cell_id[0] == self.row_count - 1 and cell_id[1] == self.column_count - 1) or (
                cell_id[0] == self.row_count - 1 and cell_id[1] == 0) or (
                cell_id[0] == 0 and cell_id[1] == self.column_count - 1):
            if self.mark_array[cell_id] != 'blank':
                return None

            for _id in self.all_id_list:
                self.virtual_mark_array[_id] = self.mark_array[_id]

            self.mark_virtual_dark(cell_id)

            if not self.virtual_error_occured():
                self.mark_dark(cell_id)
                return True
        return False

    def current_mark_unique(self, cell_id):
        for x in range(self.row_count):
            id_1 = (cell_id[0], x)
            if id_1 != cell_id:
                if self.value_array[id_1] == self.value_array[cell_id] and self.mark_array[id_1] == 'circle':
                    return False
        for x in range(self.column_count):
            id_1 = (x, cell_id[1])
            if id_1 != cell_id:
                if self.value_array[id_1] == self.value_array[cell_id] and self.mark_array[id_1] == 'circle':
                    return False
        self.mark_circle(cell_id)
        return True

    def print_solution(self):
        if self.has_solution:
            solution_string = '\n'
            print("\nSolution : \n")
            for sub_list in self.mark_array:
                for mark in sub_list:
                    if mark == 'dark':
                        print(u' X ', end='')
                        solution_string += u' • '
                    elif mark == 'circle':
                        print(' O ', end='')
                        solution_string += ' o '
                    else:
                        print(' ? ', end='')
                        solution_string += ' ? '
                print('')
                solution_string += '\n'
        else:
            print('No solution')
        print("\nTime taken to solve : ", self.time_diff)

    def get_solution(self):
        if self.has_solution:
            return self.mark_array
        else:
            return None

    def run(self):
        self.value_array = np.array(self.data)
        self.row_count = self.value_array.shape[0]
        self.column_count = self.value_array.shape[1]
        self.mark_array = np.array([['blank'] * self.column_count] * self.row_count,
                                   dtype='<U6')
        self.virtual_mark_array = np.array(self.mark_array)
        self.all_id_list = []
        angles_checked = False
        for i in range(self.row_count):
            for j in range(self.column_count):
                self.all_id_list.append((i, j))

        start_time = datetime.datetime.now()
        for i in self.all_id_list:
            self.mark_unique(i)
        while True:
            prev_mark_array = np.array(self.mark_array)
            stop_flag = True
            for i in self.all_id_list:
                self.check_for_circle(i)
            for i in self.all_id_list:
                self.check_for_dark(i)
            for i in self.all_id_list:
                self.check_for_dark_advanced(i)
            for i in self.all_id_list:
                self.check_for_circle_advanced(i)
            for i in self.all_id_list:
                if prev_mark_array[i] != self.mark_array[i]:
                    stop_flag = False
                    break
            if stop_flag:
                if not angles_checked:
                    for i in self.all_id_list:
                        self.check_angle_for_dark(i)
                        for j in self.all_id_list:
                            self.current_mark_unique(j)
                    angles_checked = True
                else:
                    self.has_solution = False
                    break
            if 'blank' not in self.mark_array.flatten().tolist():
                break

        self.time_diff = datetime.datetime.now() - start_time

        print('')
        self.print_solution()
        self.game_over = True

