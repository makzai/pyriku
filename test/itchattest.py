import itchat

itchat.auto_login()
# itchat.run()

# author = itchat.search_chatrooms(name='琪琪快乐买货宝')[0]
author1 = itchat.search_chatrooms(name='琪琪快乐买货宝')
print(author1)

# @@611260dfdfc43cc5949a69b30fc7eadafcabdb65b165c4cd257da8ab98895207
# @@843ecc1b14d52193cf143f33c5c8967644a28cd9d1df9a2a68ea2d58c2878fc2
author2 = itchat.search_chatrooms(userName='@@611260dfdfc43cc5949a69b30fc7eadafcabdb65b165c4cd257da8ab98895207')
print(author2)
# 冇料!

# author.send('新的发送消息测试!')
