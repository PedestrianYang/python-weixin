
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from SetTimerSendMessage import *

class MainUI(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('微信登录')
        self.resize(300, 200)
        self.container()
        self.addClickAction()

    def container(self):
        self.loginBtn = QPushButton()
        self.loginBtn.setText('微信登录')
        self.boxlayout = QVBoxLayout()
        self.boxlayout.addWidget(self.loginBtn)

        self.setLayout(self.boxlayout)

        self.setView = MainUIaa()

    def addClickAction(self):
        self.loginBtn.clicked.connect(self.loginAction)



    def logined(self):
        self.setView.show()
        self.close()

    def loginAction(self):
        self.loginBtn.setText("请扫描二维码登录")
        itchat.auto_login(loginCallback=self.logined())



    def run(self):
        self.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainUI()
    ui.run()