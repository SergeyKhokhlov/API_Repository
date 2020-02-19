import os
import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def getImage(self):
        self.zoom = 0.001
        self.coords = [59.935789, 30.325904]
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.coords[1]}," \
            f"{self.coords[0]}8&spn={self.zoom},{self.zoom}&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_PageUp:
            if self.zoom != 0.1:
                self.zoom -= 0.1
        elif QKeyEvent.key() == Qt.Key_PageDown:
            if self.zoom != 1:
                self.zoom += 0.1
        self.map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.coords[1]}," \
            f"{self.coords[0]}8&spn={self.zoom},{self.zoom}&l=map"
        response = requests.get(self.map_request)
        if response:
            self.map_file = "map.png"
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
