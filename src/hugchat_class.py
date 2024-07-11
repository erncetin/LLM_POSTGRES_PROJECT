from hugchat import hugchat
from hugchat.login import Login

SYSTEM_PROMPT = """     
You're a pizza delivery guy. Greet the customer as a pizza deliverer. Ask for what kind of pizza he likes etc
"""

class chatbot:

    def __init__(self) -> None:
        EMAIL = "jefec54605@qiradio.com"
        PASWRD = "1234a567@A"
        cookie_path_dir = "./cookies/" 
        sign = Login(EMAIL, PASWRD)
        cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
        self.chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        
    

    # Returns available models for dropdown menu
    def llm_models(self):
        return self.chatbot.get_available_llm_models()
    
    # Returns current model
    def get_current_llm_model(self):
        return self.chatbot.get_conversation_info().model
    
    # Create a new conversation
    def new_conversation(self, model_index, prompt):
        self.chatbot.new_conversation(
            switch_to=True, modelIndex=model_index, system_prompt=prompt
        )