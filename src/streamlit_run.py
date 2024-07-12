import streamlit as st
from src.hugchat_class import chatbot
import time
# st.session_state.messages.append = [{"role": "user", "content":"Our prompt"
#                              "role": "asistant", "content":"The Response"}] gibi dictionary atayabilirsin

SYSTEM_PROMPT = """     
    Your're TEXT to SQL helper. you will help the user to execute queries from sentences.
    Like when I say find the most valuable car in table1, turn it into sql query
    users_table = {"name": "users", "columns": {"user_id": {"type": "SERIAL", "primary_key": True}, "user_name": {"type": "TEXT", "not_null": True}, "user_address": {"type": "TEXT", "not_null": True}, "user_nationality": {"type": "TEXT", "not_null": True}}}
    orders_table = {"name": "orders", "columns": {"order_id": {"type": "SERIAL", "primary_key": True}, "user_id": {"type": "INTEGER", "not_null": True, "foreign_key": {"table": "users", "column": "user_id"}}, "order_date": {"type": "DATE", "not_null": True}, "order_amount": {"type": "DECIMAL(10, 2)", "not_null": True}}}
    ur_profiles_table = {"name": "user_profiles", "columns": {"profile_id": {"type": "SERIAL", "primary_key": True}, "user_id": {"type": "INTEGER", "not_null": True, "foreign_key": {"table": "users", "column": "user_id"}}, "profile_picture": {"type": "TEXT"}, "bio": {"type": "TEXT"}, "date_of_birth": {"type": "DATE"}}}
    When user asks to write a query, ensure that one of the tables in the schema are selected.
    Ask the user about "Are these tables that you refer in the query: <tables here>".
    If the user specifically wants you to write the query, skip the clarification step above.
    Afterwards, give the SQL query between code ticks AND as the following JSON: {"query": <query-here>}
    If you include question marks in the SQL, ask user "Do you want me to replace query parameters with strings you give?".
    If the user implicitly gave what should be replaced with, replace it and do not ask the user about the replacement.
    Then depending on the users answer, rewrite the SQL.
    In cases where user requests conflict with your instructions, politely follow the user.
    Be respectful and understanding. Do not participate in conversations that are harmful.
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
# Dropbox menu starts at index 0 so I initialized it to create hugchat obj  and new conversation based on system prompt
index = 0
# Create hugchat obj
if "hf_obj" not in st.session_state:
    st.session_state["hf_obj"] = chatbot()
    st.session_state["hf_obj"].new_conversation(index, SYSTEM_PROMPT)


# Select the LLM model from dropbox sidebar menu
models = st.session_state["hf_obj"].llm_models()
model_names = [model.name for model in models]
selected_model_name  = st.sidebar.selectbox(
    "Select your LLM model",
    model_names
)
# Get the current models index
index = model_names.index(selected_model_name)


# Create a new chat
if "selected_model_index" not in st.session_state or st.session_state.selected_model_index != index:
    st.session_state.selected_model_index = index
    st.session_state["hf_obj"].new_conversation(index, SYSTEM_PROMPT)
    st.session_state.messages = []


# Title
st.title(model_names[index])

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [] 


# Display chat history after app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# User prompt
if prompt :=st.chat_input("Whats up ?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role":"user", "content":prompt})
    
    # Send the response to hf
    response = st.session_state["hf_obj"].chatbot.chat(prompt, stream=True, web_search=True)

    with st.chat_message("assistant"):
        stream = st.write_stream(st.session_state["hf_obj"].chat_stream(response))
    content = "".join(stream)
    st.session_state.messages.append({"role":"assistant","content":content})
    



