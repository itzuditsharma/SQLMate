from dotenv import load_dotenv
load_dotenv()  # Load all environment variables

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Gemini model once
model = genai.GenerativeModel('gemini-pro')

# Function to get SQL query (Natural text -> SQL query)
def get_gemini_response(question, prompt):
    try:
        response = model.generate_content([prompt[0], question])
        return response.text.strip()  # Strip extra spaces or newlines
    except Exception as e:
        st.error(f"Error in generating SQL query: {e}")
        return None

# Function to execute SQL query (SELECT, INSERT, UPDATE, DELETE)
def execute_sql_query(sql, db):
    try:
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            cur.execute(sql)
            if sql.lower().startswith("select"):
                rows = cur.fetchall()  # Fetch data for SELECT queries
                return rows
            else:
                conn.commit()  # Commit changes for INSERT/UPDATE/DELETE queries
                return None
    except Exception as e:
        st.error(f"Error executing SQL query: {e}")
        return None

# Prompt for Gemini model
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS,
    SECTION and MARKS. 
    
    Examples:
    1. "How many entries of records are present?" -> SELECT COUNT(*) FROM STUDENT;
    
    2. "Tell me all the students studying in Data Science class?" -> SELECT * FROM STUDENT WHERE CLASS = "Data Science";
    
    3. "Insert a new record with name John in class Science, section A with marks 85" 
    -> INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('John', 'Science', 'A', 85);
    
    4. "Update marks to 95 for student named John" -> UPDATE STUDENT SET MARKS = 95 WHERE NAME = 'John';
    
    5. "Delete the entry of Niall" -> DELETE FROM STUDENT WHERE NAME = 'Niall';
    
    Ensure the SQL code is clean and does not include unnecessary characters like `(`, `)` or `,`.
    """
]

# Streamlit app
st.set_page_config(page_title="Sql made easy APP", page_icon=":gem:")
st.header("SQL query app")

# Get user input
question = st.text_input("Enter your query in natural language:", key="input")

submit = st.button("Submit")

if submit and question:
    # Step 1: Generate SQL query based on the natural language prompt
    response = get_gemini_response(question, prompt)
    
    if response:
        # Display generated SQL query
        st.subheader("Generated SQL Query:")
        st.code(response)

        # Step 2: Execute the SQL query
        data = execute_sql_query(response, "student.db")

        # Step 3: Display results for SELECT query or success message for other operations
        if data:
            st.subheader("Query Results:")
            for row in data:
                formatted_row = ' '.join(map(str, row))
                st.text(formatted_row)
        else:
            st.success("Query executed successfully.")
