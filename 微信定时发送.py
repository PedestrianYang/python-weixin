#coding=utf8
import datetime
import sys
import time

import itchat
import threading

class weixin(object):

    def __init__(self):
        self.contactName = ''
        self.msgcContent = ''
        self.isGourp = True

    def sendMessage(self):
        userName = ''
        if self.isGourp:
            itchat.get_chatrooms(update=True)
            iRoom = itchat.search_chatrooms(self.contactName)
            for room in iRoom:
                if room['NickName'] == self.contactName:
                    userName = room['UserName']
                    break

        else:
            users=itchat.search_friends(self.contactName)
            userName= users[0]['UserName']

        itchat.send_msg(self.msgcContent, userName)
        doReSend = input("发送完毕，是否重新设置？y/n")
        if doReSend == "y":
            self.timer()
        else:
            doLogout = input("是否退出？y/n")
            if doLogout == "y":
                itchat.logout()
                time.sleep(2)
                sys.exit()
            else:
                self.timer()


    def timer(self):
        tempStr = self.checkTimeFormet()

        year = tempStr[0]
        month = tempStr[1]
        day = tempStr[2]
        hour = tempStr[3]
        minit = tempStr[4]
        second = tempStr[5]
        sched_time = datetime.datetime(int(year), int(month), int(day), int(hour), int(minit), int(second))

        type = input("发送对象是群么？y/n")
        self.isGourp = type == "y"
        self.contactName = input("请输入发送对象的名称：")
        self.msgcContent = input("请输入定时发送内容：")
        print("设置成功，坐等发送！！！！！！")

        loopflag = 0
        while True:
            now = datetime.datetime.now()
            if sched_time<now<(sched_time+datetime.timedelta(seconds=1)):
                loopflag = 1
                time.sleep(1)
            if loopflag == 1:
                self.sendMessage()
                loopflag = 0


    def checkTimeFormet(self):
        dateinput = input("请输入预约时间（24小时制，例如2018年1月1日1点1分1秒：2018-1-1-1-1-1）：")
        tempStr = dateinput.split("-")
        if len(tempStr) == 6:
            return tempStr
        else:
            print("时间格式输入有误，请重新输入：")
            self.checkTimeFormet()


    def starWeixin(self):
        itchat.auto_login()
        # 获取自己的UserName
        myUserName = itchat.get_friends(update=True)[0]["UserName"]
        self.timer()
        itchat.run()


aa = weixin()
aa.starWeixin()
