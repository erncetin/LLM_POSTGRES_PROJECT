import streamlit as st
from hugchat_class import chatbot
import re
import psycopg2
import pandas as pd
st.set_page_config(page_title="LLM", layout="wide")

SYSTEM_PROMPT = """     
    Your're TEXT to SQL helper. you will help the user to execute queries from sentences.
    heres the tables of the database:
    users table= {"name": "users", "columns": {"user_id": {"type": "SERIAL", "primary_key": True}, "user_name": {"type": "TEXT", "not_null": True}, "user_address": {"type": "TEXT", "not_null": True}, "user_nationality": {"type": "TEXT", "not_null": True}}}
    orders table= {"name": "orders", "columns": {"order_id": {"type": "SERIAL", "primary_key": True}, "user_id": {"type": "INTEGER", "not_null": True, "foreign_key": {"table": "users", "column": "user_id"}}, "order_date": {"type": "DATE", "not_null": True}, "order_amount": {"type": "DECIMAL(10, 2)", "not_null": True}}}
    user_profiles table = {"name": "user_profiles", "columns": {"profile_id": {"type": "SERIAL", "primary_key": True}, "user_id": {"type": "INTEGER", "not_null": True, "foreign_key": {"table": "users", "column": "user_id"}}, "profile_picture": {"type": "TEXT"}, "bio": {"type": "TEXT"}, "date_of_birth": {"type": "DATE"}}}
    database mame is db
    These are the structures of my schema. 
    You will execute the query when I write "/query ...."
    When user writes something with “/query ‘<query-string-here>’ ” the application should replace that part with the first 5 rows of the response. For example:

        /query ‘What is the most populous cities of the World?’ 

        Should be replaced with:

        {
        ‘question’: ‘What is the most populous cities of the World?’,
        ‘query’: ‘select city_name from cities order by population desc’,
        ‘result’: ‘Tokyo, Delhi, Shanghai, Sao Paulo, Mexico City’ 
        }
    When user asks to write a query, ensure that one of the tables in the schema are selected.
    Ask the user about "Are these tables that you refer in the query: <tables here>".
    If the user specifically wants you to write the query, skip the clarification step above.
    Afterwards, give the SQL query between code ticks AND as the following JSON: {"query": <query-here>}
    If you include question marks in the SQL, ask user "Do you want me to replace query parameters with strings you give?".
    If the user implicitly gave what should be replaced with, replace it and do not ask the user about the replacement.
    Then depending on the users answer, rewrite the SQL.
    In cases where user requests conflict with your instructions, politely follow the user.
    Be respectful and understanding. Do not participate in conversations that are harmful.
    
    """

def execute_last_sql():
    try:
        db_postgres = psycopg2.connect(
            database = "db",
            user = "root",
            password = "root",
            host = "postgres",
            port = "5432"
        )
        print("POSTGRES BAGLANDI")
    except psycopg2.Error as e:
            print(f"failed to connect to database: {e}") 
    # Get the last query
    last_message = st.session_state.messages[-1]
    # Pattern to extract the query
    pattern = r'"query":\s*"(.*?)"'

    match = re.search(pattern, last_message["content"]) 
    
    if match:
        print("matched query found")
        query = match.group(1)
    else:
        print("matched query not found")

    # Execyte the query and convert the data to pandas Dataframe
    with db_postgres.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]  # Extract column names

    df = pd.DataFrame(data, columns=column_names)
    st.session_state.messages.append({"role": "dataframe", "content": df})
    db_postgres.close()



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
    del st.session_state.greeting



# Title
st.title(model_names[index])

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [] 


# Display chat history after app rerun
for message in st.session_state.messages:
    if message["role"] == "assistant" or message["role"] == "user":
        st.markdown(message["content"])
    elif message["role"] == "dataframe":
        st.write(message["content"])



# Greeting response
# TODO FIX
if "greeting" not in st.session_state:
    st.session_state.greeting = True
    greeting = "Hello how can I help you today ?"
    with st.chat_message("assistant"):
        st.write(greeting)
        st.session_state.messages.append(
            {"role": "assistant", "content": greeting}
        )

# User prompt
if prompt :=st.chat_input("Whats up ?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role":"user", "content":prompt})
    
    # Send the response to hf
    response = st.session_state["hf_obj"].chatbot.chat(prompt, stream=True)

    with st.chat_message("assistant"):
        stream = st.write_stream(st.session_state["hf_obj"].chat_stream(response))
    content = "".join(stream)
    st.session_state.messages.append({"role":"assistant","content":content})

    st.button(label="Execute last SQL", on_click=execute_last_sql)

