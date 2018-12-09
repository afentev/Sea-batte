import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox
from form import Ui_MainWindow


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.complexity_factor = 2.8
        self.ii_used = []
        self.ii_fleet = []
        self.queue = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
        self.user_used = []
        self.user_fleet = []
        self.user_fleet_full = []
        self.user_fleet_temp = []
        self.localUi()

    def localUi(self):
        self.generate(0)
        for i in range(100, 200):
            eval('self.pushButton_{I}.clicked.connect(self.reaction)'.format(I=i))

    def reaction(self, _):
        sender_name = self.sender().objectName()
        sender = (int(sender_name[-2]), int(sender_name[-1],))
        if sender not in self.user_used:
            if sender in self.user_fleet_temp:
                self.user_fleet_temp.remove((int(sender[-2]), int(sender[-1])))
                eval('self.{}.setStyleSheet("background-color: none")'.format(sender_name))
            elif sender not in self.user_fleet_full:
                self.user_fleet_temp.append((int(sender[-2]), int(sender[-1])))
                eval('self.{}.setStyleSheet("background-color: gray")'.format(sender_name))

    def correct_enter(self, x0, x1, y0, y1, field):
        if x0 != x1 and y0 != y1:
            return False
        elif y0 == y1:
            if x1 - x0 + 1 not in self.queue:
                return False
            else:
                last = field[0][0]
                for pair in field[1:]:
                    if pair[0] - last != 1:
                        return False
                    last = pair[0]
                return True
        else:
            if y1 - y0 + 1 not in self.queue:
                return False
            else:
                last = field[0][1]
                for pair in field[1:]:
                    if pair[1] - last != 1:
                        return False
                    last = pair[1]
                return True

    def keyPressEvent(self, a0):
        if a0.key() == 16777220:
            self.user_fleet_temp = tuple(sorted(self.user_fleet_temp))
            xmin, xmax = self.user_fleet_temp[0][0], self.user_fleet_temp[-1][0]
            ymin, ymax = min(self.user_fleet_temp, key=lambda a: a[1])[1], max(self.user_fleet_temp, key=lambda a: a[1])[1]
            print(self.correct_enter(xmin, xmax, ymin, ymax, self.user_fleet_temp))
            if len(self.user_fleet_temp) in self.queue and self.correct_enter(xmin, xmax, ymin, ymax, self.user_fleet_temp):
                self.queue.remove(len(self.user_fleet_temp))
                self.user_fleet.append(Ship(xmin, ymin, xmax, ymax, tuple(self.user_fleet_temp)))
                self.user_fleet_full.extend(self.user_fleet_temp)
                self.user_used.extend(self.user_fleet_temp)
                self.user_used.extend(self.user_fleet[-1].get_borders())
                self.user_fleet_temp = []
                if not self.queue:
                    self.game()
            else:
                for sender in self.user_fleet_temp:
                    eval('self.pushButton_1{}.setStyleSheet("background-color: none")'.format(str(sender[0]) + str(sender[1])))
                self.user_fleet_temp = []

    def game(self):
        first_turn = random.random() > 0.5
        mes = QMessageBox(self)
        mes.setGeometry(350, 200, 100, 100)
        mes.setText('Вы начинаете' if first_turn else 'Я начинаю')
        if first_turn:
            mes.setText('Вы начинаете')
        else:
            mes.setText('Я начинаю')
        mes.show()

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
            # for pair in res[-1]:
            #     eval('self.pushButton_2{}{}.setStyleSheet("background-color: red")'.format(str(pair[0]), str(pair[1])))
            for pos in self.ii_fleet[-1].get_borders():
                self.ii_used.append(pos)
                # eval('self.pushButton_2{}{}.setStyleSheet("background-color: black")'.format(str(pos[0]), str(pos[1])))

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
                if (i, j) in self.ii_used:
                    break
                tmp.append((i, j,))
            else:
                continue
            break
        else:
            self.ii_used.extend(tmp)
            return x, y, x1, y1, tmp
        return ()


class Ship:
    def __init__(self, x_start, y_start, x_end, y_end, field):
        self.status = 1  # -1 - damaged; 0 - killed; 1 - alive
        self.field = field
        self.size = len(field)
        self.x_start, self.y_start, self.x_end, self.y_end = min(x_start, x_end), min(y_start, y_end),\
                                                             max(x_end, x_start), max(y_end, y_start)
        self.borders = []
        self.get_borders()

    def __repr__(self):
        return 'Ship({}): {}'.format(self.size, str(self.field))

    def __contains__(self, item):
        return item in self.field

    def get_borders(self):
        if self.x_start >= 1:
            xmin = self.x_start - 1
        else:
            xmin = 0
        if self.x_end <= 8:
            xmax = self.x_end + 1
        else:
            xmax = 9
        if self.y_start >= 1:
            ymin = self.y_start - 1
        else:
            ymin = 0
        if self.y_end <= 8:
            ymax = self.y_end + 1
        else:
            ymax = 9
        if ymin >= 0:
            for i in range(xmin, xmax + 1):
                if (i, ymin,) not in self.field:
                    self.borders.append((i, ymin,))
        if ymax <= 9:
            for i in range(xmin, xmax + 1):
                if (i, ymax,) not in self.field:
                    self.borders.append((i, ymax,))
        if xmin >= 0:
            for i in range(ymin, ymax + 1):
                if (xmin, i,) not in self.field:
                    self.borders.append((xmin, i,))
        if xmax <= 9:
            for i in range(ymin, ymax + 1):
                if (xmax, i,) not in self.field:
                    self.borders.append((xmax, i,))
        for i in ((xmax, ymax), (xmax, ymin), (xmin, ymax), (xmin, ymin)):
            if i not in self.field:
                self.borders.append(i)
        return tuple(set(self.borders))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

