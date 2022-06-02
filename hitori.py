import pygame.constants


import time
import config as c
from game import Game
from input_box import InputBox
from button import Button
from solver import Solver
from text_object import TextObject


class Hitori(Game):
    def __init__(self):
        Game.__init__(self, 'Hitori',
                      c.screen_width,
                      c.screen_height,
                      c.frame_rate)
        self.input_boxes = None
        self.button_size = None
        self.solve_button = None
        self.solution = None
        self.field_size = 3
        self.create_objects()

    def create_boxes(self):
        boxes = []
        for i in range(0, self.field_size):
            boxes_row = []
            for j in range(0, self.field_size):
                box = InputBox(j*c.input_box_width, i*c.input_box_height, c.input_box_width, c.input_box_height, self.field_size)
                self.objects.append(box)
                boxes_row.append(box)
                x = box.handle
                self.mouse_handlers[pygame.MOUSEBUTTONDOWN].append(box.handle)
                self.keydown_handlers[pygame.K_1].append(box.handle)
                self.keydown_handlers[pygame.K_2].append(box.handle)
                self.keydown_handlers[pygame.K_3].append(box.handle)
                self.keydown_handlers[pygame.K_4].append(box.handle)
                self.keydown_handlers[pygame.K_5].append(box.handle)
                self.keydown_handlers[pygame.K_6].append(box.handle)
                self.keydown_handlers[pygame.K_7].append(box.handle)
                self.keydown_handlers[pygame.K_8].append(box.handle)
                self.keydown_handlers[pygame.K_9].append(box.handle)
                self.keydown_handlers[pygame.K_BACKSPACE].append(box.handle)
                self.keydown_handlers[pygame.K_RETURN].append(box.handle)
            boxes.append(boxes_row)
        self.input_boxes = boxes

    def create_buttons(self):
        button_size = Button(5, 530, 170, 35, (176, 196, 222), 'increase the field size')
        self.objects.append(button_size)
        self.button_size = button_size
        self.mouse_handlers[pygame.MOUSEBUTTONDOWN].append(button_size.handle)
        button_solve = Button(200, 530, 55, 35, (176, 196, 222), 'solve')
        self.objects.append(button_solve)
        self.solve_button = button_solve
        self.mouse_handlers[pygame.MOUSEBUTTONDOWN].append(button_solve.handle)

    def create_objects(self):
        self.create_boxes()
        self.create_buttons()

    def check_field_size(self):
        if self.button_size.count > 0:
            self.field_size += self.button_size.count
            if self.field_size > c.max_field_size:
                self.field_size = c.max_field_size
            self.button_size.count = 0
            for boxes_row in self.input_boxes:
                for box in boxes_row:
                    self.objects.remove(box)
            self.input_boxes = None
            self.create_boxes()

    def get_data(self):
        data = []
        for boxes_row in self.input_boxes:
            data_row = []
            for box in boxes_row:
                if box.text != '':
                    data_row.append(int(box.text))
                else:
                    self.solve_button.solve = False
                    return None
            data.append(data_row)
        return data

    def show_message(self, text, color=(255, 0, 255), font_name='Arial', font_size=20, centralized=False):
        """ Функция для отображения текста на экране """
        message = TextObject(c.screen_width // 2, c.screen_height // 2, lambda: text, color, font_name, font_size)
        self.draw()
        message.draw(self.surface, centralized)
        pygame.display.update()
        time.sleep(c.message_duration)

    def show_solution(self, solution):
        if self.solution.has_solution:
            for i in range(self.field_size):
                for j in range(self.field_size):
                    self.input_boxes[i][j].mark = solution[i][j]
        else:
            self.show_message('No solution', centralized=True)

    def check_solve_button(self):
        if self.solve_button.solve:
            data = self.get_data()
            if data is not None:
                self.solution = Solver(data)
                self.solution.run()
                solution = self.solution.get_solution()
                self.show_solution(solution)
            else:
                self.show_message('fill in the table completely', centralized=True)

    def check_game_over(self):
        if self.solution is not None:
            if self.solution.game_over:
                return True

    def update(self):
        self.check_field_size()
        self.check_solve_button()
        if self.check_game_over():
            #self.game_over = True
            pass
        super().update()


