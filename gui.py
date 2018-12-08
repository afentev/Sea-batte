import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox
from form import Ui_MainWindow


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.complexity_factor = 2.8
        self.used = []
        self.ii_fleet = []
        self.localUi()

    def localUi(self):
        self.generate(1)
        print(self.ii_fleet)

    def generate(self, difficult):  # 0 <= difficult <= 2
        prob = difficult / self.complexity_factor
        for ship in range(10):
            gen = random.random()
            size = 5 - int(ship <= 3) - int(ship <= 6) - int(ship <= 8) - int(ship <= 9)
            # x, y, x1, y1 = self.all_(size, gen, prob)
            res = self.intersection(size, gen, prob)
            while not res:
                res = self.intersection(size, gen, prob)
            self.ii_fleet.append(Ship(*res))
            print(res[-1])
            for pair in res[-1]:
                eval('self.pushButton_1{}{}.setStyleSheet("background-color: red")'.format(str(pair[0]), str(pair[1])))

    @staticmethod
    def generate_cords(d):
        if d:
            if random.random() > 0.5:
                x = random.randint(0, 1) * 9
                y = random.randint(0, 9)
            else:
                y = random.randint(0, 1) * 9
                x = random.randint(0, 9)
        else:
            x, y = random.randint(0, 9), random.randint(0, 9)
        return x, y

    def all_(self, size, gen, prob):
        x, y = self.generate_cords(gen <= prob)
        size -= 1
        if x + size >= 10 or x - size <= -1:
            if y + size >= 10:
                x_end, y_end = x, y - size
            else:
                x_end, y_end = x, y + size
        elif y + size >= 10 or y - size:
            if x + size >= 10:
                x_end, y_end = x - size, y
            else:
                x_end, y_end = x + size, y
        else:
            sign = -1 if random.random() < 0.5 else 1
            if random.random() > 0.5:
                x_end = x + sign * size
                y_end = y
            else:
                y_end = y + sign * size
                x_end = x
        return x, y, x_end, y_end

    def intersection(self, size, gen, prob):
        x, y, x1, y1 = self.all_(size, gen, prob)
        tmp = []
        for i in range(min(x, x1), max(x1, x) + 1):
            for j in range(min(y1, y), max(y1, y) + 1):
                if (i, j) in self.used:
                    break
                tmp.append((i, j,))
            else:
                continue
            break
        else:
            self.used.extend(tmp)
            return x, y, x1, y1, tmp
        return ()


class Ship:
    def __init__(self, x_start, y_start, x_end, y_end, field):
        self.status = 1  # -1 - damaged; 0 - killed; 1 - alive
        self.field = field
        self.size = len(field)
        self.x_start, self.y_start, self.x_end, self.y_end = x_start, y_start, x_end, y_end
        self.borders = []

    def __repr__(self):
        return 'Ship({}): {}'.format(self.size, str(self.field))

    def get_borders(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
