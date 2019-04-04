from PySide2.QtWidgets import *
from PySide2.QtCore import *
import itchat
import sys
import datetime
import time
import threading

class MainUIaa(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('定时发送设置')
        self.resize(300, 200)
        self.container()
        self.msgcContentArr = []

    def container(self):
        b_layout = QVBoxLayout()

        v_layout1 = QHBoxLayout()
        lab1 = QLabel("发送时间")
        self.input1 = QLineEdit()
        self.input1.setInputMask("0000-00-00-00-00-00")
        v_layout1.addWidget(lab1)
        v_layout1.addWidget(self.input1)

        b_layout.addLayout(v_layout1)

        v_layout2 = QHBoxLayout()
        lab1 = QLabel("发送内容")
        self.input2 = QLineEdit()
        v_layout2.addWidget(lab1)
        v_layout2.addWidget(self.input2)

        b_layout.addLayout(v_layout2)


        v_layout3 = QHBoxLayout()
        lab3 = QLabel("发送对象")
        self.input3 = QLineEdit()
        v_layout3.addWidget(lab3)
        v_layout3.addWidget(self.input3)

        b_layout.addLayout(v_layout3)

        v_layout4 = QHBoxLayout()
        self.vquncheck = QRadioButton('发送给群')
        self.vquncheck.setChecked(True)
        self.vrencheck = QRadioButton('发送给人')
        v_layout4.addWidget(self.vquncheck)
        v_layout4.addWidget(self.vrencheck)
        b_layout.addLayout(v_layout4)


        commiteBtn = QPushButton("确定")

        commiteBtn.clicked.connect(self.commiteAction)
        b_layout.addWidget(commiteBtn)


        self.h_layout = QVBoxLayout()
        b_layout.addLayout(self.h_layout)



        self.setLayout(b_layout)

    def checkTimeFormet(self, dateinput):
        dateinputStr = dateinput.text()

        tempStr = dateinputStr.split("-")

        for aaa in tempStr:
            if aaa == '':
                QMessageBox.information(self, '提示', '发送时间格式输入有误，请重新输入！', QMessageBox.Yes)
                return False

        return True

    def precommiteAction(self):
        if self.checkTimeFormet(self.input1) == False:
            return False

        if len(self.input2.text()) == 0 or self.input2.text() == '':
            QMessageBox.information(self, '提示', '发送内容不能为空！', QMessageBox.Yes)
            return False

        if len(self.input3.text()) == 0 or self.input3.text() == '':
            renqun = ''
            if self.vquncheck.isChecked():
                renqun = '群'
            if self.vrencheck.isChecked():
                renqun = '人'
            QMessageBox.information(self, '提示', '请输入发送对象的 %s 名！' % renqun, QMessageBox.Yes)
            return False

        return True

    def commiteAction(self):
        if self.precommiteAction() == False:
            return

        tempStr = self.input1.text().split("-")

        year = tempStr[0]
        month = tempStr[1]
        day = tempStr[2]
        hour = tempStr[3]
        minit = tempStr[4]
        second = tempStr[5]

        if int(month) > 12 or int(month)< 1:
            QMessageBox.information(self, '提示', '月份必须在1-12之间！', QMessageBox.Yes)
            return

        if int(day) > 31 or int(day) < 1:
            QMessageBox.information(self, '提示', '天数必须在1-31之间！', QMessageBox.Yes)
            return

        if int(hour) > 24 or int(day) < 1:
            QMessageBox.information(self, '提示', '小时必须在1-24之间！', QMessageBox.Yes)
            return

        if int(minit) > 60 or int(minit) < 0 or int(second) > 60 or int(second) < 0:
            QMessageBox.information(self, '提示', '分钟与秒钟必须在0-60之间！', QMessageBox.Yes)
            return

        sched_time = datetime.datetime(int(year), int(month), int(day), int(hour), int(minit), int(second))

        now = datetime.datetime.now()
        if now > (sched_time+datetime.timedelta(seconds=1)):
            QMessageBox.information(self, '提示', '发送的时间小于当前时间，请检查！', QMessageBox.Yes)
            return


        self.isGourp = self.vquncheck.isChecked() == True
        contactName = self.input3.text()
        msgcContent = self.input2.text()

        contactNameTouserName = ''
        if self.isGourp:
            itchat.get_chatrooms(update=True)
            iRoom = itchat.search_chatrooms(contactName)
            for room in iRoom:
                if room['NickName'] == contactName:
                    contactNameTouserName = room['UserName']
                    break

        else:
            users=itchat.search_friends(contactName)
            contactNameTouserName= users[0]['UserName']

        if contactNameTouserName == None or len(contactNameTouserName) == 0:
            QMessageBox.information(self, '提示', '未找到联系人%s' % contactName, QMessageBox.Yes)
            return


        QMessageBox.information(self, '提示', '设置成功，坐等发送！', QMessageBox.Yes)

        timeLab = QLabel()
        sendStr = self.input1.text() + ':发送给[%s]%s' % (contactName, msgcContent)
        timeLab.setText(sendStr)
        self.h_layout.addWidget(timeLab)

        dict = {'time': sched_time, 'lab': timeLab, 'msg': msgcContent, 'person': contactNameTouserName}
        self.msgcContentArr.append(dict)

        print(self.msgcContentArr)

        if len(self.msgcContentArr) != 0:
            self.thread = threading.Thread(target=self.countTime, name="aaaa")
            self.thread.start()
            print('子线程开启')

        QTableView


    def countTime(self):

        if  len(self.msgcContentArr) == 0:
            return

        print('子线程运行')
        while len(self.msgcContentArr) > 0 :
            print('子线程运行111')
            now = datetime.datetime.now()
            print(now)
            for dic in self.msgcContentArr:
                sched_time = dic['time']
                print(sched_time)
                if sched_time<now<(sched_time+datetime.timedelta(seconds=1)):
                    print('时间到')
                    self.sendMessage(dic)
                    pass
            time.sleep(1)




    def sendMessage(self, dic):
        itchat.send_msg(dic['msg'], dic['person'])
        label = dic['lab']
        self.h_layout.removeWidget(label)
        label.deleteLater()

        self.msgcContentArr.remove(dic)



    def show(self, *args, **kwargs):
        QWidget.show(self, *args, **kwargs)


    def close(self, *args, **kwargs):
        itchat.logout()
        QWidget.close(self, *args, **kwargs)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = MainUIaa()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())





