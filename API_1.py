import os
import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QLineEdit, QTextEdit, \
    QCheckBox, QLabel

SCREEN_SIZE = [1050, 670]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.deleteSearch = False
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

        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0][
                "GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
            self.coords = toponym_coodrinates.split()
            self.coords_pt = toponym_coodrinates.split()
            self.params_image = {
                "ll": ','.join(self.coords),
                "spn": ','.join(self.zoom),
                "l": self.temp,
            }
            if not self.deleteSearch:
                self.params_image = {
                    "ll": ','.join(self.coords),
                    "spn": ','.join(self.zoom),
                    "l": self.temp,
                    "pt": ','.join(self.coords_pt) + ",pm2gnl"
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
        self.btn_map.resize(560, 50)
        self.btn_map.setStyleSheet("QPushButton {border-radius: 10px; "
                                   "border: 4px solid darkgreen; font-size: 20px; color: yellow; "
                                   "background-color: green} QPushButton:hover "
                                   "{background-color: black; border: 4px solid black;}"
                                   ";}")
        self.btn_map.move(20, 470)

        self.btn_sat = QPushButton("Спутник", self)
        self.btn_sat.resize(560, 50)
        self.btn_sat.setStyleSheet("QPushButton {border-radius: 10px; "
                                   "border: 4px solid darkgreen; font-size: 20px; color: yellow; "
                                   "background-color: green} QPushButton:hover "
                                   "{background-color: black; border: 4px solid black;}"
                                   ";}")
        self.btn_sat.move(20, 530)

        self.btn_gib = QPushButton("Гибрид", self)
        self.btn_gib.resize(560, 50)
        self.btn_gib.setStyleSheet("QPushButton {border-radius: 10px; "
                                   "border: 4px solid darkgreen; font-size: 20px; color: yellow; "
                                   "background-color: green} QPushButton:hover "
                                   "{background-color: black; border: 4px solid black;}"
                                   ";}")
        self.btn_gib.move(20, 590)
        self.btn_search = QPushButton("Искать", self)
        self.btn_search.resize(100, 40)
        self.btn_search.setStyleSheet("QPushButton {border-radius: 10px; "
                                      "border: 4px solid darkgreen; font-size: 20px; color: yellow;"
                                      "background-color: green} QPushButton:hover "
                                      "{background-color: black; border: 4px solid black;}"
                                      ";}")
        self.btn_search.move(930, 20)
        self.line_search = QLineEdit(self)
        self.line_search.resize(300, 40)
        self.line_search.move(620, 20)
        self.line_search.setStyleSheet("QLineEdit {background-color: green; color: yellow;"
                                       "border-radius: 10px; border: 4px solid darkgreen;"
                                       "font-size: 20px;}")
        self.btn_delete_search = QPushButton("Сброс поискового результата", self)
        self.btn_delete_search.move(620, 80)
        self.btn_delete_search.resize(410, 40)
        self.btn_delete_search.setStyleSheet("QPushButton {background-color: green; color: yellow;"
                                             "border-radius: 10px; border: 4px solid darkgreen;"
                                             "font-size: 20px;} QPushButton:hover "
                                             "{background-color: black; border: 4px solid black;}"
                                             ";}")
        self.output_search = QTextEdit(self)
        self.output_search.move(620, 140)
        self.output_search.resize(410, 90)
        self.output_search.setStyleSheet("QTextEdit {background-color: green; color: yellow;"
                                         "border-radius: 10px; border: 4px solid darkgreen;"
                                         "font-size: 20px;}")
        self.checkBox = QCheckBox(self)
        self.checkBox.move(990, 260)
        self.checkBox.resize(40, 40)
        self.checkBox.setStyleSheet("QCheckBox {background-color: green; color: yellow;"
                                    "border-radius: 10px; border: 4px solid darkgreen;"
                                    "font-size: 20px; padding-left: 9px;} QPushButton:hover "
                                    "{background-color: black; border: 4px solid black;}"
                                    ";}")
        self.output_search.setReadOnly(True)
        self.text_checkBox = QLabel("Отобразить почтовый индекс", self)
        self.text_checkBox.move(620, 260)
        self.text_checkBox.resize(360, 40)
        self.text_checkBox.setStyleSheet(
            "QLabel {color: yellow; font-size: 20px; "
            "background-color: #339900; padding-left: 35px;}")
        self.image.setFocus()
        self.output_search.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.btn_search.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_map.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_gib.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_sat.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete_search.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_map.clicked.connect(self.change_map)
        self.btn_sat.clicked.connect(self.change_map)
        self.btn_gib.clicked.connect(self.change_map)
        self.btn_search.clicked.connect(self.search_place)
        self.btn_delete_search.clicked.connect(self.delete_search)

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
        if not self.deleteSearch:
            self.params_image = {
                "ll": ','.join(self.coords),
                "spn": ','.join(self.zoom),
                "l": self.temp,
                "pt": ','.join(self.coords_pt) + ",pm2gnl"
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

    def delete_search(self):
        self.deleteSearch = True
        self.params_image = {
            "ll": ','.join(self.coords),
            "spn": ','.join(self.zoom),
            "l": self.temp,
        }
        self.line_search.setText("")
        self.output_search.setPlainText("")
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

    def search_place(self):
        self.deleteSearch = False
        try:
            self.text = self.line_search.text()
            self.params_search = {
                "apikey": '40d1649f-0493-4b70-98ba-98533de7710b',
                "geocode": self.text,
                "format": "json"
            }
            map_request = "http://geocode-maps.yandex.ru/1.x/"
            response = requests.get(map_request, self.params_search)
            if response:
                json_response = response.json()
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0][
                    "GeoObject"]
                toponym_index = ""
                try:
                    toponym_index = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"][
                        "postal_code"]
                except:
                    pass
                toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]['text']
                self.output_search.setPlainText(toponym_address)
                if self.checkBox.isChecked() and toponym_index != "":
                    self.output_search.setPlainText(toponym_address + " Индекс: " + toponym_index)
                toponym_coodrinates = toponym["Point"]["pos"]
                self.coords = toponym_coodrinates.split()
                self.coords_pt = toponym_coodrinates.split()
                self.params_image = {
                    "ll": ','.join(self.coords),
                    "spn": ','.join(self.zoom),
                    "l": self.temp,
                }
                if not self.deleteSearch:
                    self.params_image = {
                        "ll": ','.join(self.coords),
                        "spn": ','.join(self.zoom),
                        "l": self.temp,
                        "pt": ','.join(self.coords_pt) + ",pm2gnl"
                    }
                url = "http://static-maps.yandex.ru/1.x/"
                response = requests.get(url, params=self.params_image)
                self.map_file = "map.png"
                if self.temp == "sat":
                    self.map_file = "map.jpg"
                with open(self.map_file, "wb") as file:
                    file.write(response.content)
                self.params_image = {
                    "ll": ','.join(self.coords),
                    "spn": ','.join(self.zoom),
                    "l": self.temp,
                }
                if not self.deleteSearch:
                    self.params_image = {
                        "ll": ','.join(self.coords),
                        "spn": ','.join(self.zoom),
                        "l": self.temp,
                        "pt": ','.join(self.coords_pt) + ",pm2gnl"
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
                self.image.setFocus()
        except Exception:
            pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if float(self.zoom[1]) >= 0.01:
                self.zoom[1] = str(float(self.zoom[1]) - 0.01)
        elif event.key() == Qt.Key_PageDown:
            if float(self.zoom[1]) <= 20:
                self.zoom[1] = str(float(self.zoom[1]) + 0.01)
        elif event.key() == Qt.Key_Right:
            self.coords[0] = str(float(self.coords[0]) + (0.1 * float(self.zoom[1])))
        elif event.key() == Qt.Key_Left:
            self.coords[0] = str(float(self.coords[0]) - (0.1 * float(self.zoom[1])))
        elif event.key() == Qt.Key_Up:
            self.coords[1] = str(float(self.coords[1]) + (0.1 * float(self.zoom[1])))
        elif event.key() == Qt.Key_Down:
            self.coords[1] = str(float(self.coords[1]) - (0.1 * float(self.zoom[1])))
        self.params_image = {
            "ll": ','.join(self.coords),
            "spn": ','.join(self.zoom),
            "l": self.temp,
        }
        if not self.deleteSearch:
            self.params_image = {
                "ll": ','.join(self.coords),
                "spn": ','.join(self.zoom),
                "l": self.temp,
                "pt": ','.join(self.coords_pt) + ",pm2gnl"
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
