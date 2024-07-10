from hugchat import hugchat
from hugchat.login import Login
import os


EMAIL = os.getenv("EMAIL")
PASWRD = os.getenv("PASWRD")

cookie_path_dir = "./cookies/" 
sign = Login(EMAIL, PASWRD)
cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)


chatbot = hugchat.ChatBot(cookies=cookies.get_dict())


while 1:
    inpt = input()
    message_result = chatbot.chat(inpt)
    print(message_result)
