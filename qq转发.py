#coding=utf8
import threading

from qqbot import QQBotSlot as qqbotslot, RunBot, qqbotsched
from qqbot import _bot as bot

import itchat

@qqbotslot
def onQQMessage(bot, contact, member, content):
    print(contact, member, content)


    if bot.isMe(contact, member):
        print('自己发送的')
        return

    toUsers = bot.List('buddy', '*****')

    print('收到消息' + content)
    if toUsers:
        toUser = toUsers[0]
        bot.SendTo(toUser, u'[%s]：%s' % (contact,content) )
        itchat.send_msg(u"收到好友@%s 的信息：%s\n" %
                        (contact, content), toUserName='filehelper')



def starQQ():
    RunBot()

def starWeixin():
    itchat.auto_login()
    # 获取自己的UserName
    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    local_school.chat = itchat
    itchat.run()



threads = []
t1 = threading.Thread(target=starQQ, name='111')
threads.append(t1)
t2 = threading.Thread(target=starWeixin, name='222')
threads.append(t2)

local_school = threading.local()

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()


