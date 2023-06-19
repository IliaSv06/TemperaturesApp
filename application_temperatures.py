from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from parsing_temp import load_data_temps
from make_graph import create_graph
from requests import head
import sys
import re

class ApplicationTemperatures(QWidget):
    def __init__(self):
        super().__init__()
        self.months = ("january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
        "november", "december") 
        self.setFixedSize(404, 482)
        self.setWindowTitle("Графики температур")
        self.create_widgets()
        self.show()

    def create_widgets(self):
        """Создает все виджеты приложения"""

        self.grid = QGridLayout()    
        self.setLayout(self.grid)

        self.first_message = QLabel("Укажите нужный вам месяц и город, чтобы\nпостроить график температур указанного\n\t    месяца и города!")
        self.first_message.setObjectName("first_message")

        # подсказки для пользователя какие данные нужно указать  
        self.notion_month = QLabel("Укажите нужный вам месяц") 
        self.notion_city = QLabel("Введите нужный вам город")
        self.warning = QLabel("") # предупреждение, которое будет появляться если пользователь укажет неверные данные
        self.warning.setObjectName("warning")

        # создаем виджеты для ввода и выбора данных от пользователя
        self.line_edit_city = QLineEdit() # для ввода города
        self.combo_box_month = QComboBox() # для выбора месяца
        self.combo_box_month.addItems(self.months)

        # создаюм кнопки для потверждения или отмены действий
        self.button_confirm = QPushButton("Потвердить")
        self.button_reset = QPushButton("Сбросить")

        # добавляем виджеты на экран приложения
        self.add_widgets_app()
        
        # Связываем функций с кнопками
        self.button_confirm.clicked.connect(self.process_creating_graph)
        self.button_reset.clicked.connect(self.clear_name_city)

    def add_widgets_app(self):
        """Добавляет все виджеты на окно приложения"""
        
        self.grid.addWidget(self.first_message, 0, 0, 1, -1, alignment = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

        self.grid.addWidget(self.notion_month, 1, 0, alignment = Qt.AlignmentFlag.AlignBottom)
        self.grid.addWidget(self.combo_box_month, 2, 0, alignment = Qt.AlignmentFlag.AlignTop)

        self.grid.addWidget(self.notion_city, 3, 0, alignment = Qt.AlignmentFlag.AlignBottom)
        self.grid.addWidget(self.line_edit_city, 4, 0, alignment = Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.warning, 5, 0, alignment = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

        self.grid.addWidget(self.button_confirm, 6, 0, alignment =  Qt.AlignmentFlag.AlignCenter)
        self.grid.setRowMinimumHeight(7, 14)
        self.grid.addWidget(self.button_reset, 8, 0, alignment = Qt.AlignmentFlag.AlignCenter)

        self.grid.setRowMinimumHeight(9, 30)

    def check_name_city(self, name_city, month):
        """Проверяет название города и предупреждает пользователя, если он введет неверные данные"""

        regex_name_city = r"[A-Za-z-]+" # нужно, чтобы проверить, что пользователь написал имя города на английском 
        url = f"https://yandex.ru/pogoda/{name_city}/month/{month}"
        warning_text = ""
        if not name_city:
            warning_text = "*обязательное поле для заполнения." # если пользователь не укажет город, то ему выведится это сообщение
        
        elif not re.search(regex_name_city, name_city):
            warning_text = "*имя города должно быть на английском." # если пользователь укажет город не на английском, то ему выведится это сообщение
        
        elif head(url).status_code == 404: # посалаем запрос на страницу с городом, чтобы проверить существует ли он
            warning_text = "*такого города нет или он неверно указан." # если пользователь укажет город которого нет, то ему выведится это сообщение
        
        self.warning.setText(warning_text) # посылаем полузователю предупреждение
        if warning_text:
            return False
        return True
    
    def process_creating_graph(self):
        """Запускает процесс создания грфафика температур"""
        month = self.combo_box_month.currentText()
        name_city = self.line_edit_city.text().strip().lower()
        if self.check_name_city(name_city, month):
            day_temps, night_temps = load_data_temps(month, name_city)
            create_graph(day_temps, night_temps, month, name_city)

    def clear_name_city(self):
        """Делает сброс текста виджетов (месяц и имя города), если пользователь нажмет на кнопку 'Сбросить' """
        self.combo_box_month.setCurrentText("january")
        self.line_edit_city.clear()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("styles.css", "r") as file:
        app.setStyleSheet(file.read())
    ex = ApplicationTemperatures()
    sys.exit(app.exec_())