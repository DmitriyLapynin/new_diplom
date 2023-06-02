import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QComboBox, QPlainTextEdit, QAction, \
    QMenuBar
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot, QCoreApplication
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal as Signal


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


'''OUTPUT_LOGGER_STDOUT = OutputLogger(sys.stdout, OutputLogger.Severity.DEBUG)
OUTPUT_LOGGER_STDERR = OutputLogger(sys.stderr, OutputLogger.Severity.ERROR)
sys.stdout = OUTPUT_LOGGER_STDOUT
sys.stderr = OUTPUT_LOGGER_STDERR'''

class Ui_MainWindow(object):

    def setupUi(self, windowMain):
        combo = ["Язык линейных вычислений",
                 "Язык условных вычислений",
                 "Язык циклических вычислений",
                 "Язык вычислений с одномерными массивами",
                 "Язык вычислений с одномерными массивами и циклами",
                 "Язык функциональных вычислений",
                 "Язык вычислений со сложными типами и функциями",
                 "Язык функциональных и циклических вычислений",
                 "Язык Паскаль"
                 ]
        windowMain.setWindowTitle("Система учебных языков программирования")
        windowMain.setGeometry(100, 100, 1100, 700)
        self.label_type = QLabel(windowMain)
        self.label_type.setText('Типы языков системы:')
        self.label_type.setFont(QFont("Times", 11, QFont.Bold))
        self.label_type.move(750, 160)
        self.label_type.adjustSize()
        self.combo = QComboBox(self)
        self.combo.addItems(combo)
        self.combo.setGeometry(700, 200, 350, 40)
        self.button_start = QPushButton(windowMain)
        self.button_start.setGeometry(0, 0, 450, 70)
        self.button_start.setText("Примеры задач с решениями")
        self.button_start.setFont(QFont("Times", 15))
        self.button_show_grammar = QPushButton(windowMain)
        self.button_show_grammar.setGeometry(450, 0, 450, 70)
        self.button_show_grammar.setText("Инструкция")
        self.button_show_grammar.setFont(QFont("Times", 15))
        self.button_exit = QPushButton(windowMain)
        self.button_exit.setGeometry(900, 0, 200, 70)
        self.button_exit.setFont(QFont("Arial", 15))
        self.button_exit.setText("Выход")
        self.button_exit.clicked.connect(QCoreApplication.instance().quit)
        self.label1 = QLabel(windowMain)
        self.label1.setText('Код:')
        self.label1.setFont(QFont("Times", 11, QFont.Bold))
        self.label1.move(60, 100)
        self.label1.adjustSize()
        self.plainText1 = QPlainTextEdit(windowMain)
        self.plainText1.setGeometry(50, 150, 600, 460)
        self.plainText1.setReadOnly(False)
        self.button_run = QPushButton(windowMain)
        self.button_run.setGeometry(220, 630, 200, 50)
        self.button_run.setFont(QFont("Arial", 15))
        self.button_run.setText("Запуск")
        self.label2 = QLabel(windowMain)
        self.label2.setText('Вывод:')
        self.label2.setFont(QFont("Times", 11, QFont.Bold))
        self.label2.move(680, 270)
        self.label2.adjustSize()
        self.plainText2 = QPlainTextEdit(windowMain)
        self.plainText2.setGeometry(670, 310, 400, 370)

        OUTPUT_LOGGER_STDOUT.emit_write.connect(self.append_log)
        OUTPUT_LOGGER_STDERR.emit_write.connect(self.append_log)
        '''menu_bar = QMenuBar()
        menu = menu_bar.addMenu('Say')
        menu.addAction('hello', lambda: print('Hello!'))
        menu.addAction('fail', lambda: print('Fail!', file=sys.stderr))
        self.setMenuBar(menu_bar)

        self.setCentralWidget(self.plainText2)'''

    def append_log(self, text, severity):
        text = repr(text)
        if severity == OutputLogger.Severity.ERROR:
            text = '<b>{}</b>'.format(text)
        self.plainText2.append(text)