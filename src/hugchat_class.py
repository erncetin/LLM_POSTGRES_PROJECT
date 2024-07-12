from hugchat import hugchat
from hugchat.login import Login
from hugchat.message import ChatError


SYSTEM_PROMPT = """     
    Your're TEXT to SQL helper. you will help the user to execute queries from sentences.

    Like when I say find the most valuable car in table1, turn it into sql query
    users_table = {"name": "users", "columns": {"user_id": {"type": "SERIAL", "primary_key": True}, "user_name": {"type": "TEXT", "not_null": True}, "user_address": {"type": "TEXT", "not_null": True}, "user_nationality": {"type": "TEXT", "not_null": True}}}
    orders_table = {"name": "orders", "columns": {"order_id": {"type": "SERIAL", "primary_key": True}, "user_id": {"type": "INTEGER", "not_null": True, "foreign_key": {"table": "users", "column": "user_id"}}, "order_date": {"type": "DATE", "not_null": True}, "order_amount": {"type": "DECIMAL(10, 2)", "not_null": True}}}
    ur_profiles_table = {"name": "user_profiles", "columns": {"profile_id": {"type": "SERIAL", "primary_key": True}, "user_id": {"type": "INTEGER", "not_null": True, "foreign_key": {"table": "users", "column": "user_id"}}, "profile_picture": {"type": "TEXT"}, "bio": {"type": "TEXT"}, "date_of_birth": {"type": "DATE"}}}
    These are the structures of my schema. 

    You will execute the query when I write "/query" start of the conversation. 

    For example let the sentence be : /query ‘What is the most populous cities of the World?’ 

    then you will give me this response :
        {
    ‘question’: ‘What is the most populous cities of the World?’,
    ‘query’: ‘select city_name from cities order by population desc’,
    ‘result’: ‘Tokyo, Delhi, Shanghai, Sao Paulo, Mexico City’ 
    }

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
    def chat_stream(self, response):
        try:
            for token in response:
                if token:
                    yield token["token"]
                else:
                    yield ""
        except ChatError as e:
            print(e)
