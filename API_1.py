import os
import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QLineEdit

SCREEN_SIZE = [600, 600]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def getImage(self):
        self.text = "Москва"
        self.temp = "map"
        self.zoom = ["0.001", "0.001"]
        self.params_search = {
            "apikey": '40d1649f-0493-4b70-98ba-98533de7710b',
            "geocode": self.text,
            "format": "json"
        }
        map_request = "http://geocode-maps.yandex.ru/1.x/"
        response = requests.get(map_request, self.params_search)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        self.coords = toponym_coodrinates.split()
        print(toponym_coodrinates)
        self.params_image = {
            "ll": ','.join(self.coords),
            "spn": ','.join(self.zoom),
            "l": self.temp,
        }
        url = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(url, params=self.params_image)
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
        self.btn_search = QPushButton("Искать", self)
        self.btn_search.resize(100, 40)
        self.btn_search.setStyleSheet("QPushButton {border-radius: 10px; "
                                      "border: 4px solid darkgreen; font-size: 20px; color: yellow;"
                                      "background-color: green} QPushButton:hover "
                                      "{background-color: black; border: 4px solid black;}"
                                      ";}")
        self.btn_search.move(420, 465)
        self.line_search = QLineEdit(self)
        self.line_search.resize(300, 40)
        self.line_search.move(80, 465)
        self.line_search.setStyleSheet("QLineEdit {background-color: green; color: yellow;"
                                       "border-radius: 10px; border: 4px solid darkgreen;"
                                       "font-size: 20px;}")
        self.btn_search.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_map.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_gib.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_sat.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
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
        self.params_image = {
            "ll": ','.join(self.coords),
            "spn": ','.join(self.zoom),
            "l": self.temp,
        }
        self.map_request = f"http://static-maps.yandex.ru/1.x/"
        response = requests.get(self.map_request, params=self.params_image)
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
        print(type(self.coords[0]))
        if event.key() == Qt.Key_PageUp:
            if float(self.zoom[1]) >= 0.1:
                self.zoom[1] = str(float(self.zoom[1]) - 0.1)
        elif event.key() == Qt.Key_PageDown:
            if float(self.zoom[1]) <= 1:
                self.zoom[1] = str(float(self.zoom[1]) + 0.1)
        elif event.key() == Qt.Key_Right:
            self.coords[0] = str(float(self.coords[0]) + 0.001)
        elif event.key() == Qt.Key_Left:
            self.coords[0] = str(float(self.coords[0]) - 0.001)
        elif event.key() == Qt.Key_Up:
            self.coords[1] = str(float(self.coords[1]) + 0.001)
        elif event.key() == Qt.Key_Down:
            self.coords[1] = str(float(self.coords[1]) - 0.001)
        print(self.coords)
        self.params_image = {
            "ll": ','.join(self.coords),
            "spn": ','.join(self.zoom),
            "l": self.temp,
        }
        self.map_request = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(self.map_request, self.params_image)
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
