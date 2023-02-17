import sys
from PyQt5.QtWidgets import QApplication
from model.lissajous import LissajousWindow

if __name__ == "__main__":
    # Инициализируем приложение Qt
    app = QApplication(sys.argv)
    # Создаём и настраиваем главное окно
    window = LissajousWindow()
    # Показываем окно
    window.show()

    # Запуск приложения
    # На этой строке выполнение основной программы блокируется
    # до тех пор, пока пользователь не закроет окно.
    # Вся дальнейшая работа должна вестись либо в отдельных потоках,
    # либо в обработчиках событий Qt.
    sys.exit(app.exec_())
