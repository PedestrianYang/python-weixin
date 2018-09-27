#coding=utf8
import threading

from qqbot import QQBotSlot as qqbotslot, RunBot, qqbotsched


@qqbotslot
def onQQMessage(bot, contact, member, content):
    print(contact, member, content)


    if bot.isMe(contact, member):
        print('自己发送的')
        return

    toUsers = bot.List('buddy', '****')

    print('收到消息' + content)
    if toUsers:
        toUser = toUsers[0]
        bot.SendTo(toUser, u'[%s]：%s' % (contact,content) )



if __name__ == '__main__':
    RunBot()
