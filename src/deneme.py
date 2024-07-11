from hugchat import hugchat
from hugchat.login import Login
import streamlit as st
from hugchat_class import chatbot

SYSTEM_PROMPT = """     
You're a pizza delivery guy. Greet the customer as a pizza deliverer. Ask for what kind of pizza he likes etc
"""

# Chatbot obj
chatbot_obj = chatbot()



#chatbot.new_conversation(switch_to= True, modelIndex=1, system_prompt=SYSTEM_PROMPT)



#while 1:
 #   inpt = input()
  #  if "/web" in inpt:
    #    try:
       #     query_result = chatbot.query(inpt, web_search=True)
       #     print(query_result)
        #    for source in query_result.web_search_sources:
        #        print(source.link)
         #       print(source.title)
      #  except Exception as e:
       #     print(e)
 #   else:
      #  message_result = chatbot.chat(inpt)
    #    print(message_result)
