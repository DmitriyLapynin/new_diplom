from PyQt5 import QtGui, QtCore

from interpretator import Interpretator
import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLineEdit, QLabel, QPlainTextEdit, QAction, \
    QComboBox, QTextEdit, QMenuBar
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot, QCoreApplication
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal as Signal
import Tensorflow


class OutputLogger(QObject):
    emit_write = Signal(str, int)


    class Severity:
        DEBUG = 0
        ERROR = 1

    def __init__(self, io_stream, severity):
        super().__init__()

        self.io_stream = io_stream
        self.severity = severity

    def write(self, text):
        self.io_stream.write(text)
        self.emit_write.emit(text, self.severity)

    def flush(self):
        self.io_stream.flush()


OUTPUT_LOGGER_STDOUT = OutputLogger(sys.stdout, OutputLogger.Severity.DEBUG)
OUTPUT_LOGGER_STDERR = OutputLogger(sys.stderr, OutputLogger.Severity.ERROR)
sys.stdout = OUTPUT_LOGGER_STDOUT
sys.stderr = OUTPUT_LOGGER_STDERR


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        combo = ["Язык линейных вычислений",
                 "Язык условных вычислений",
                 "Язык циклических вычислений",
                 "Язык вычислений с одномерными массивами",
                 "Язык вычислений с одномерными массивами и циклами",
                 "Язык функциональных вычислений",
                 "Язык вычислений со сложными типами и функциями",
                 "Язык функциональных и циклических вычислений",
                 "Язык Мини-Паскаль"
                 ]

        self.setWindowTitle("Система учебных языков программирования")
        self.setGeometry(100, 100, 1100, 700)
        self.label_type = QLabel(self)
        self.label_type.setText('Выбранный язык системы:')
        self.label_type.setFont(QFont("Times", 11, QFont.Bold))
        self.label_type.move(750, 160)
        self.label_type.adjustSize()


        self.combo = QComboBox(self)
        self.combo.addItems(combo)
        self.combo.setGeometry(700, 200, 350, 40)
        self.button_start = QPushButton(self)
        self.button_start.setGeometry(0, 0, 450, 70)
        self.button_start.setText("Сборник задач")
        self.button_start.clicked.connect(self.onClickTasks)
        self.button_start.setFont(QFont("Times", 15))
        self.button_show_grammar = QPushButton(self)
        self.button_show_grammar.setGeometry(450, 0, 450, 70)
        self.button_show_grammar.setText("Инструкция")
        self.button_show_grammar.setFont(QFont("Times", 15))
        self.button_exit = QPushButton(self)
        self.button_exit.setGeometry(900, 0, 200, 70)
        self.button_exit.setFont(QFont("Arial", 15))
        self.button_exit.setText("Выход")
        self.button_exit.clicked.connect(QCoreApplication.instance().quit)
        self.label1 = QLabel(self)
        self.label1.setText('Код:')
        self.label1.setFont(QFont("Times", 11, QFont.Bold))
        self.label1.move(60, 100)
        self.label1.adjustSize()
        self.plainText1 = QTextEdit(self)
        self.plainText1.setGeometry(50, 150, 600, 460)
        self.plainText1.setFont(QFont("Times", 15))
        self.plainText1.setReadOnly(False)
        self.button_run = QPushButton(self)
        self.button_run.setGeometry(220, 630, 200, 50)
        self.button_run.setFont(QFont("Arial", 15))
        self.button_run.setText("Запуск")
        self.button_run.clicked.connect(self.onClickRun)
        self.label2 = QLabel(self)
        self.label2.setText('Вывод:')
        self.label2.setFont(QFont("Times", 11, QFont.Bold))
        self.label2.move(680, 270)
        self.label2.adjustSize()
        self.plainText2 = QTextEdit(self)
        self.plainText2.setGeometry(670, 310, 400, 370)
        self.plainText2.setFont(QFont("Times", 15))
        self.plainText2.setWordWrapMode(QtGui.QTextOption.NoWrap)

        OUTPUT_LOGGER_STDOUT.emit_write.connect(self.append_log)
        OUTPUT_LOGGER_STDERR.emit_write.connect(self.append_log)

    def append_log(self, text, severity):
        text = text
        if severity == OutputLogger.Severity.ERROR:
            text = '<b>{}</b>'.format(text)
        self.plainText2.append(text)

    def onClickTasks(self):
        print("")


    def onClickRun(self):
        self.plainText2.clear()
        text = self.plainText1.toPlainText()
        # print(text)
        with open('test_save.txt', 'w', encoding='UTF-8') as out_file:
            print(f"{text}", file=out_file)
        try:
            i = Interpretator('test_save.txt', 5)
            i.interpretation()
            # print("Работа анализатора заверешена успешно!")
        except Exception as error:
            print(error)
        except FileNotFoundError:
            print("The file is not exist")

if __name__ == '__main__':
    app = QApplication([])
    mw = MainWindow()
    mw.show()
    app.exec()


'''try:
    print("Подмножества языка Паскаль:")
    print("1 – Язык линейных вычислений")
    print("2 – Язык условных вычислений")
    print("3 – Язык циклических вычислений")
    print("4 - Язык вычислений с одномерными массивами")
    print("5 - Язык вычислений с одномерными массивами и циклами")
    print("6 - Язык функциональных вычислений")
    print("7 - Язык вычислений со сложными типами и функциями")
    print("8 - Язык функциональных и циклических вычислений")
    print("9 - Язык Паскаль")
    while 1:
        print("Выберите номер языка, на котором написана программа")
        mode = int(input())
        if mode > 9 or mode < 1:
            print("Номер языка должен быть в отрезке [1, 9]")
        else:
            break
    print("Введите название файла с программой")
    f = input()
    i = Interpretator('test3.txt', 8)
    i.interpretation()
    print("Работа анализатора заверешена успешно!")
except Exception as error:
    print(error)
except FileNotFoundError:
    print("The file is not exist")'''