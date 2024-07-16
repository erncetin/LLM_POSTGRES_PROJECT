LLM streamlit application with postgres server on Docker. 


1- Purpose of the project:
    a-This project, converts the text to SQL queries
    
    b-By writing /query ..... the ai will turn the text to query. You need to specify the table names and confirm then ai will give you the proper query.
    
    c-You can execute the the query by pressing execute last querry button. Alternatively, you can login to postgres server and try the query yourself.


2- To run:
    a-pull the project
    
    b-write command "docker compose up --build"
    
    c-open localhost/8501 on your web browser 

Preferably, use meta-llama/Meta-Llama-3-70B for better results.

Here's the schema of the database:
        USERS TABLE:{
    "name": "users",
    "columns": {
        "user_id": {
        "type": "SERIAL",
        "primary_key": true
        },
        "user_name": {
        "type": "TEXT",
        "not_null": true
        },
        "user_address": {
        "type": "TEXT",
        "not_null": true
        },
        "user_nationality": {
        "type": "TEXT",
        "not_null": true
        }
    }
    }
    
    ORDERS TABLE:{
    "name": "orders",
    "columns": {
        "order_id": {
        "type": "SERIAL",
        "primary_key": true
        },
        "user_id": {
        "type": "INTEGER",
        "not_null": true,
        "foreign_key": {
            "table": "users",
            "column": "user_id"
        }
        },
        "order_date": {
        "type": "DATE",
        "not_null": true
        },
        "order_amount": {
        "type": "DECIMAL(10, 2)",
        "not_null": true
        }
    }
    }

    USER_PROFILES TABLE:{
    "name": "user_profiles",
    "columns": {
        "profile_id": {
        "type": "SERIAL",
        "primary_key": true
        },
        "user_id": {
        "type": "INTEGER",
        "not_null": true,
        "foreign_key": {
            "table": "users",
            "column": "user_id"
        }
        },
        "profile_picture": {
        "type": "TEXT"
        },
        "bio": {
        "type": "TEXT"
        },
        "date_of_birth": {
        "type": "DATE"
        }
    }
    }


