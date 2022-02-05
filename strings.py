
welcome = """
*Hey Hi* ... ```user_name```
Welcome to _Assign bot_ 🔮
"""

intro = """
*1.* _my_ *Name* 🧑‍🎓 
*2.* random _joke_ 🤠
*3.* random _picture_ 🌄
*4.* random _document_ 📝
*5.* random _documents_ ( ~upto~ 10)📚

_say_  *Help* 🙋 
to get this ```message``` again
"""


response_xml =f"""
<?xml version="1.0" encoding="UTF-8"?><Response><Message>Body</Message></Response>
"""
empty_responce_xml = '<?xml version="1.0" encoding="UTF-8"?></Response>'

what_is_my_name = ('1',"say my name","what is my name", 'my name')
give_me_joke = ('2','joke','say joke','send a joke','tell me a joke','random joke')
picuture = ('random picture', 'random pic', 'pic','picuture','image','random image','photo','random photo','3')
documents = ('send a file','file','documents','send docoment','send docoments','random file','random files','random document', 'random thing','4')
help = ('help', 'help me', '/help', '\help')


max_files = "Sorry I have only *10* files "

picsum_link = "https://picsum.photos/200/300"