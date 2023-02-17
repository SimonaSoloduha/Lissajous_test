import os
import numpy as np
import time

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QPushButton, QComboBox, QLineEdit
from PyQt5 import uic, QtGui
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from matplotlib import pyplot
from config import DEFAULT_SETTINGS, COLORS, VERSION


class LissajousWindow(QMainWindow):
    """ Окно приложения """

    def __init__(self):
        super().__init__()
        self.statusbar = None
        self.save_button = None
        self.update_button = None
        self.freq_x_lineedit = None
        self.freq_y_lineedit = None
        self.color_combobox = None
        self.width_combobox = None
        self._fc = None
        self._fig = None
        self._ax = None
        self.make_window()

    def make_window(self):
        """ Создание окна программы """
        # Загружаем интерфейс окна из файла
        uic.loadUi("view/main_window.ui", self)
        # заголовок окна
        self.setWindowTitle(f"Генератор фигур Лиссажу. Версия {VERSION}. CC BY Soloduha S")
        # размеры
        self.setGeometry(200, 200, 650, 300)
        # иконка
        self.setWindowIcon(QtGui.QIcon("img/icon-2.png"))

        # Создаём холст matplotlib
        self._fig = pyplot.figure(figsize=(4, 3), dpi=72)
        # Добавляем на холст matplotlib область для построения графиков.
        # В общем случае таких областей на холсте может быть несколько
        # Аргументы add_subplot() в данном случае:
        # ширина сетки, высота сетки, номер графика в сетке
        self._ax = self._fig.add_subplot(1, 1, 1)
        #
        # Создаём qt-виджет холста для встраивания холста
        # matplotlib fig в окно Qt.
        self._fc = FigureCanvas(self._fig)
        # Связываем созданный холст c окном
        self._fc.setParent(self)
        # Настраиваем размер холста
        self._fc.resize(400, 270)
        # Первичное построение фигуры
        self.plot_lissajous_figure()

        self.freq_x_lineedit = QLineEdit(self)
        self.formLayout.addRow('Частота X (a)', self.freq_x_lineedit)
        self.freq_x_lineedit.setText(str(DEFAULT_SETTINGS['freq_x']))

        self.freq_y_lineedit = QLineEdit(self)
        self.formLayout.addRow('Частота Y (b)', self.freq_y_lineedit)
        self.freq_y_lineedit.setText(str(DEFAULT_SETTINGS['freq_y']))

        self.color_combobox = QComboBox(self)
        self.color_combobox.addItems(COLORS.keys())

        default_color_val = DEFAULT_SETTINGS['color']
        reverse_color_map = dict(map(reversed, COLORS.items()))
        default_color = reverse_color_map.get(default_color_val)
        default_color_index = list(COLORS.keys()).index(default_color)

        self.color_combobox.setCurrentIndex(default_color_index)
        self.formLayout.addRow('Цвет линии', self.color_combobox)

        width_variables = [
            '1', '2', '3', '4'
        ]
        default_width = width_variables.index(str(DEFAULT_SETTINGS['width']))
        self.width_combobox = QComboBox(self)
        self.width_combobox.addItems(width_variables)
        self.width_combobox.setCurrentIndex(default_width)
        self.formLayout.addRow('Толщина линии', self.width_combobox)

        self.update_button = QPushButton(self)
        self.update_button.setText('Обновить фигуру')
        self.formLayout.addRow(self.update_button)

        self.save_button = QPushButton(self)
        self.save_button.setText('Сохранить фигуру в файл')
        self.formLayout.addRow(self.save_button)

        self.update_button.clicked.connect(self.update_button_click_handler)
        # self.update_button.clicked.connect(self.plot_button_click_handler)
        self.save_button.clicked.connect(self.save_button_click_handler)

    def plot_lissajous_figure(self, settings=None):
        """ Обновление/создание фигуры """
        if settings is None:
            settings = DEFAULT_SETTINGS
        # Удаляем устаревшие данные с графика
        for line in self._ax.lines:
            line.remove()

        # Создаем фигуру
        figure = LissajousFigure(settings["freq_x"], settings["freq_y"])

        # Строим график
        self._ax.plot(figure.x_arr, figure.y_arr,
                      color=settings["color"], linewidth=settings["width"])

        # Скрываем линейку
        pyplot.axis("off")

        # Обновляем холст в окне
        self._fc.draw()

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
        self.plot_lissajous_figure(settings)

    def save_button_click_handler(self):
        """ Обработчик кнопки 'Сохранить фигуру в файл' """
        # Задаем путь сохранения файла по умолчанию (в загрузки)
        test_path_default = os.path.expanduser('~/Downloads')
        # Получаем данные из текстовых полей
        settings = self.get_settings()
        # Задаем имя файла по умолчанию
        file_name = f'lissajous_{settings["freq_x"]}_{settings["freq_y"]}_{settings["color"]}_{settings["width"]}'
        test_path_default = os.path.abspath(f'{test_path_default}/{file_name}')
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранение изображения", f"{test_path_default}",
                                                   "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        self._fig.savefig(file_path)


class LissajousFigure:
    """
    Класс Фигуры Лиссажу.
    Задаётся набором точек с координатами x и y.

    """
    def __init__(self, x_array, y_array, resolution=20):
        self.resolution = resolution
        t = np.linspace(0, 2 * np.pi, self.resolution)
        self.x_arr = np.sin(x_array * t)
        self.y_arr = np.cos(y_array * t)
        # Эта задержка эмулирует процедуру инициализации следующей версии генератора.
        # Задержка будет убрана после обновления.
        # Пока не трогать.
        # P.S. В новом генераторе задержка будет только при инициализации.
        # Фигуры будут генерироваться так же быстро, как и сейчас.
        time.sleep(1)
