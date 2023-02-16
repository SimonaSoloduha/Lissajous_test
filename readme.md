# Lissajous

Генератор фигур Лиссажу с графическим интерфейсом.

Возможности:
* Генерация фигур Лиссажу с заданными частотами по X и Y.
* Установка цвета фигуры.
* Установка толщины линии.
* Экспорт фигур в виде изображений.

Запуск:

* Скачайте программу с формате ZIP
* Скопируйте путь к папке Lissajous_test-main (далее "путь к папке")
* Установите необходимые компоненты и программу через консоль:

```
cd "путь к папке" 
(Например cd "путь к папке" /Users/apple/Downloads/Lissajous_test-main)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install --upgrade pip
python main.py

```

Для дальнейшего запуска используйте: 
```
cd "путь к папке" 
(Например cd "путь к папке" /Users/apple/Downloads/Lissajous_test-main)
source venv/bin/activate
python main.py
```

Для удобства работы имеет смысл использовать виртуальные окружения.

### Замечание

Иногда частоты по X и Y обозначают буквами $a$ и $b$.