from Client_Window import *

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = user()
    sys.exit(app.exec_())