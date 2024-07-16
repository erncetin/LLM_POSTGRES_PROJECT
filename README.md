LLM streamlit application with postgres server on Docker. 


1- Purpose of the project:
    This project, converts the text to SQL queries
    By writing /query ..... the ai will turn the text to query. You need to specify the table names and confirm then ai will give you the proper query.
    You can execute the the query by pressing execute last querry button. Alternatively, you can login to postgres server and try the query yourself.


2- To run:
    pull the project
    write command "docker compose up --build"
    open localhost/8501 on your web browser 



Here's the schema of the database:
    {
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
    {
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
    {
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


