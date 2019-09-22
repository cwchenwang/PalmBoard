from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QLabel
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor
from PyQt5.QtCore import QTimer, Qt
import sys
sys.path.append('../')


class Bikey(QWidget):
    def __init__(self):
        super(Bikey, self).__init__()
        self.setPalette(QPalette(QColor(255, 255, 255)))
        self.resize(900,800)
        self.init_labels()

    def init_labels(self):
        self.font = QFont("Fonseca", 24, QFont.Bold)
        self.qw = QLabel(self)
        self.qw.setGeometry(50, 50, 100, 50)
        self.qw.setText("QW")
        self.qw.setStyleSheet("border:2px solid black;")
        self.qw.setAlignment(Qt.AlignCenter)
        self.qw.setFont(self.font)

        self.er = QLabel(self)
        self.er.setGeometry(150, 50, 100, 50)
        self.er.setText("ER")
        self.er.setStyleSheet("border:2px solid black;")
        self.er.setAlignment(Qt.AlignCenter)
        self.er.setFont(self.font)

        self.ty = QLabel(self)
        self.ty.setGeometry(250, 50, 100, 50)
        self.ty.setText("TY")
        self.ty.setStyleSheet("border:2px solid black;")

        self.ui = QLabel(self)
        self.ui.setGeometry(350, 50, 100, 50)
        self.ui.setText("UI")
        self.ui.setStyleSheet("border:2px solid black;")

        self.op = QLabel(self)
        self.op.setGeometry(450, 50, 100, 50)
        self.op.setText("OP")
        self.op.setStyleSheet("border:2px solid black;")

        self.mas = QLabel(self)
        self.mas.setGeometry(62.5, 100, 100, 50)
        self.mas.setText("AS")
        self.mas.setStyleSheet("border:2px solid black;")
    
        self.df = QLabel(self)
        self.df.setGeometry(162.5, 100, 100, 50)
        self.df.setText("DF")
        self.df.setStyleSheet("border:2px solid black;")

        self.gh = QLabel(self)
        self.gh.setGeometry(262.5, 100, 100, 50)
        self.gh.setText("GH")
        self.gh.setStyleSheet("border:2px solid black;")

        self.jk = QLabel(self)
        self.jk.setGeometry(362.5, 100, 100, 50)
        self.jk.setText("JK")
        self.jk.setStyleSheet("border:2px solid black;")

        self.l = QLabel(self)
        self.l.setGeometry(462.5, 100, 50, 50)
        self.l.setText("L")
        self.l.setStyleSheet("border:2px solid black;")

        self.zx = QLabel(self)
        self.zx.setGeometry(87.5, 150, 100, 50)
        self.zx.setText("ZX")
        self.zx.setStyleSheet("border:2px solid black;")

        self.cv = QLabel(self)
        self.cv.setGeometry(87.5+100, 150, 100, 50)
        self.cv.setText("CV")
        self.cv.setStyleSheet("border:2px solid black;")

        self.bn = QLabel(self)
        self.bn.setGeometry(87.5+200, 150, 100, 50)
        self.bn.setText("BN")
        self.bn.setStyleSheet("border:2px solid black;")

        self.m = QLabel(self)
        self.m.setGeometry(87.5+300, 150, 50, 50)
        self.m.setText("M")
        self.m.setStyleSheet("border:2px solid black;")

        self.ty.setAlignment(Qt.AlignCenter)
        self.ty.setFont(self.font)

        self.qw.setAlignment(Qt.AlignCenter)
        self.qw.setFont(self.font)

        self.ui.setAlignment(Qt.AlignCenter)
        self.ui.setFont(self.font)

        self.op.setAlignment(Qt.AlignCenter)
        self.op.setFont(self.font)

        self.mas.setAlignment(Qt.AlignCenter)
        self.mas.setFont(self.font)

        self.df.setAlignment(Qt.AlignCenter)
        self.df.setFont(self.font)

        self.gh.setAlignment(Qt.AlignCenter)
        self.gh.setFont(self.font)

        self.jk.setAlignment(Qt.AlignCenter)
        self.jk.setFont(self.font)

        self.l.setAlignment(Qt.AlignCenter)
        self.l.setFont(self.font)

        self.zx.setAlignment(Qt.AlignCenter)
        self.zx.setFont(self.font)

        self.cv.setAlignment(Qt.AlignCenter)
        self.cv.setFont(self.font)

        self.bn.setAlignment(Qt.AlignCenter)
        self.bn.setFont(self.font)

        self.m.setAlignment(Qt.AlignCenter)
        self.m.setFont(self.font)

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Bikey()
    win.show()
    sys.exit(app.exec_())

