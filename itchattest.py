import itchat

itchat.auto_login()
# itchat.run()

author = itchat.search_chatrooms(name='琪琪快乐买货宝')[0]
author.send('新的发送消息测试!')
