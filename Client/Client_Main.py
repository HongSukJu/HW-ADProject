import sys

from Client_UI import *

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = Ktalk()
    w.show()
    sys.exit(app.exec_())
    