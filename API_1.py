import os
import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QLineEdit

SCREEN_SIZE = [600, 600]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def getImage(self):
        self.zoom = 0.001
        self.temp = "map"
        self.coords = [59.935789, 30.325904]
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.coords[1]}," \
            f"{self.coords[0]}8&spn={self.zoom},{self.zoom}&l={self.temp}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        if self.temp == "sat":
            self.map_file = "map.jpg"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.setStyleSheet("QWidget {background-color: lightgreen;}")
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.setFocus()
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)
        self.btn_map = QPushButton("Схема", self)
        self.btn_map.resize(100, 50)
        self.btn_map.setStyleSheet("QPushButton {border-radius: 10px; "
                                   "border: 4px solid darkgreen; font-size: 20px; color: yellow; "
                                   "background-color: green} QPushButton:hover "
                                   "{background-color: black; border: 4px solid black;}"
                                   ";}")
        self.btn_map.move(80, 520)

        self.btn_sat = QPushButton("Спутник", self)
        self.btn_sat.resize(100, 50)
        self.btn_sat.setStyleSheet("QPushButton {border-radius: 10px; "
                                   "border: 4px solid darkgreen; font-size: 20px; color: yellow; "
                                   "background-color: green} QPushButton:hover "
                                   "{background-color: black; border: 4px solid black;}"
                                   ";}")
        self.btn_sat.move(250, 520)

        self.btn_gib = QPushButton("Гибрид", self)
        self.btn_gib.resize(100, 50)
        self.btn_gib.setStyleSheet("QPushButton {border-radius: 10px; "
                                   "border: 4px solid darkgreen; font-size: 20px; color: yellow; "
                                   "background-color: green} QPushButton:hover "
                                   "{background-color: black; border: 4px solid black;}"
                                   ";}")
        self.btn_gib.move(420, 520)
        self.btn_search = QPushButton("Поиск", self)
        self.btn_search.resize(100, 40)
        self.btn_search.setStyleSheet("QPushButton {border-radius: 10px; "
                                   "border: 4px solid darkgreen; font-size: 20px; color: yellow; "
                                   "background-color: green} QPushButton:hover "
                                   "{background-color: black; border: 4px solid black;}"
                                   ";}")
        self.btn_search.move(420, 465)
        self.font = QFont()
        self.font.setPointSize(20)
        self.line_search = QLineEdit(self)
        self.line_search.resize(300, 30)
        self.line_search.move(80, 470)
        self.line_search.setFont(self.font)
        self.btn_map.clicked.connect(self.change_map)
        self.btn_sat.clicked.connect(self.change_map)
        self.btn_gib.clicked.connect(self.change_map)




    def change_map(self):
        if self.sender().text() == "Схема":
            self.temp = "map"
        elif self.sender().text() == "Спутник":
            self.temp = "sat"
        elif self.sender().text() == "Гибрид":
            self.temp = "skl"
        self.map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.coords[1]}," \
            f"{self.coords[0]}8&spn={self.zoom},{self.zoom}&l={self.temp}"
        response = requests.get(self.map_request)
        if response:
            self.map_file = "map.png"
            if self.temp == "sat":
                self.map_file = "map.jpg"
            with open(self.map_file, "wb") as file:
                file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.image.setFocus()
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.zoom >= 0.1:
                self.zoom -= 0.1
        elif event.key() == Qt.Key_PageDown:
            if self.zoom <= 1:
                self.zoom += 0.1
        elif event.key() == Qt.Key_Right:
            self.coords[1] += 0.001
        elif event.key() == Qt.Key_Left:
            self.coords[1] -= 0.001
        elif event.key() == Qt.Key_Up:
            self.coords[0] += 0.001
        elif event.key() == Qt.Key_Down:
            self.coords[0] -= 0.001
        self.map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.coords[1]}," \
            f"{self.coords[0]}8&spn={self.zoom},{self.zoom}&l={self.temp}"
        response = requests.get(self.map_request)
        if response:
            self.map_file = "map.png"
            if self.temp == "sat":
                self.map_file = "map.jpg"
            with open(self.map_file, "wb") as file:
                file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
