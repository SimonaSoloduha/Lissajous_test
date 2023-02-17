import os
import numpy as np
import time

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QPushButton, QComboBox, QLineEdit
from PyQt5 import uic, QtGui
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import pyplot
from config import DEFAULT_SETTINGS, COLORS, VERSION, WIDTH_VARIABLES, IMG_FORMATS


class LissajousWindow(QMainWindow):
    """ Окно приложения """

    def __init__(self):
        super().__init__()
        self.figure = None
        self.axes = None
        self.figure_canvas = None

        self.statusbar = None
        self.save_button = None
        self.update_button = None
        self.freq_x_lineedit = None
        self.freq_y_lineedit = None
        self.color_combobox = None
        self.width_combobox = None
        self.make_window()

    def make_window(self):
        """ Создание окна программы """
        # создание окна
        self.create_interface()
        # поле ввода 'Частота X (a)'
        self.create_freq_x_lineedit()
        # поле ввода 'Частота Y (b)'
        self.create_freq_y_lineedit()
        # поле выбора цвета
        self.create_color_combobox()
        # поле выбора толщины
        self.create_width_combobox()
        # кнопка 'Обновить фигуру'
        self.create_update_button()
        # кнопка 'Сохранить фигуру в файл'
        self.create_save_button()
        # Область построения фигуры
        self.create_figure_and_axes()
        self.create_figure_canvas()
        # Первичное построение фигуры
        self.draw_lissajous_figure()

    def create_interface(self):
        # Загружаем интерфейс окна из файла
        uic.loadUi("view/main_window.ui", self)
        # заголовок окна
        self.setWindowTitle(f"Генератор фигур Лиссажу. Версия {VERSION}. CC BY Soloduha S")
        # размеры
        self.setGeometry(200, 200, 650, 300)
        # иконка
        self.setWindowIcon(QtGui.QIcon("img/icon-2.png"))

    def create_freq_x_lineedit(self):
        """Создание поля ввода 'Частота X (a)'"""
        self.freq_x_lineedit = QLineEdit(self)
        self.formLayout.addRow('Частота X (a)', self.freq_x_lineedit)
        self.freq_x_lineedit.setText(str(DEFAULT_SETTINGS['freq_x']))

    def create_freq_y_lineedit(self):
        self.freq_y_lineedit = QLineEdit(self)
        """Создание поля ввода 'Частота Y (b)'"""
        self.formLayout.addRow('Частота Y (b)', self.freq_y_lineedit)
        self.freq_y_lineedit.setText(str(DEFAULT_SETTINGS['freq_y']))

    def create_color_combobox(self):
        self.color_combobox = QComboBox(self)
        self.color_combobox.addItems(COLORS.keys())

        default_color_val = DEFAULT_SETTINGS['color']
        reverse_color_map = dict(map(reversed, COLORS.items()))
        default_color = reverse_color_map.get(default_color_val)
        default_color_index = list(COLORS.keys()).index(default_color)

        self.color_combobox.setCurrentIndex(default_color_index)
        self.formLayout.addRow('Цвет линии', self.color_combobox)

    def create_width_combobox(self):
        default_width = WIDTH_VARIABLES.index(str(DEFAULT_SETTINGS['width']))
        self.width_combobox = QComboBox(self)
        self.width_combobox.addItems(WIDTH_VARIABLES)
        self.width_combobox.setCurrentIndex(default_width)
        self.formLayout.addRow('Толщина линии', self.width_combobox)

    def create_update_button(self):
        self.update_button = QPushButton(self)
        self.update_button.setText('Обновить фигуру')
        self.formLayout.addRow(self.update_button)
        self.update_button.clicked.connect(self.update_button_click_handler)

    def create_save_button(self):
        self.save_button = QPushButton(self)
        self.save_button.setText('Сохранить фигуру в файл')
        self.formLayout.addRow(self.save_button)
        self.save_button.clicked.connect(self.save_button_click_handler)

    def create_figure_and_axes(self):
        """Создание Figure с одной областью Axes"""
        self.figure, self.axes = pyplot.subplots()

    def create_figure_canvas(self):
        """Создание FigureCanvas """
        # Создаём qt-виджет холста для встраивания холста
        # matplotlib fig в окно Qt.
        self.figure_canvas = FigureCanvas(self.figure)
        # Связываем созданный холст c окном
        self.figure_canvas.setParent(self)
        # Настраиваем размер холста
        self.figure_canvas.resize(400, 270)

    def create_lissajous_figure(self, settings):
        t = np.linspace(0, 2 * np.pi, 100)
        x = settings["freq_x"]
        y = settings["freq_y"]
        color = settings["color"]
        width = settings["width"]
        self.axes.plot(np.sin(x * t), np.cos(y * t),
                       color=color, linewidth=width)
        # Эта задержка эмулирует процедуру инициализации следующей версии генератора.
        # Задержка будет убрана после обновления.
        # Пока не трогать.
        # P.S. В новом генераторе задержка будет только при инициализации.
        # Фигуры будут генерироваться так же быстро, как и сейчас.
        time.sleep(1)

    def draw_lissajous_figure(self, settings=DEFAULT_SETTINGS):
        """ Обновление/создание фигуры """
        # Очищам холст
        self.axes.cla()
        # Создаем фигуру
        self.create_lissajous_figure(settings)
        # Устанавливаем aspect ratio равный 1 (квадратный)
        self.axes.set_aspect(1)
        # Скрываем линейку
        pyplot.axis("off")
        # Обновляем холст в окне
        self.figure_canvas.draw()

    def get_settings(self):
        """ Получение данных из текстовых полей """
        figures_setting = {"freq_x": float(self.freq_x_lineedit.text()),
                           "freq_y": float(self.freq_y_lineedit.text()),
                           "color": COLORS[self.color_combobox.currentText()],
                           "width": int(self.width_combobox.currentText())}

        return figures_setting

    def update_button_click_handler(self):
        """ Обработчик кнопки 'Обновить фигуру' """
        # Получаем данные из текстовых полей
        settings = self.get_settings()
        # Перестраиваем график
        self.draw_lissajous_figure(settings)

    def save_button_click_handler(self):
        """ Обработчик кнопки 'Сохранить фигуру в файл' """
        # Путь сохранения файла по умолчанию (в загрузки)
        test_path_default = os.path.expanduser('~/Downloads')
        # Получаем данные из текстовых полей
        settings = self.get_settings()
        # Задаем имя файла по умолчанию
        file_name = f'lissajous_{settings["freq_x"]}_{settings["freq_y"]}_{settings["color"]}_{settings["width"]}'
        test_path_default = os.path.abspath(f'{test_path_default}/{file_name}')
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранение изображения", f"{test_path_default}",
                                                   ';;'.join(IMG_FORMATS))
        self.figure.savefig(file_path)
