from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# List available models
for model in genai.list_models():
    print(model.name, model.supported_generation_methods)
# Function to load Google Gemini model and provide query as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('models/gemini-2.5-flash-preview-05-20')
    
    full_prompt = f"{prompt}\n\n{question}"
    response = model.generate_content(full_prompt)
    return response.text.strip()

# Function to retrieve query from SQL database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
    except Exception as e:
        rows = [("Error executing SQL:", str(e))]
    conn.close()
    return rows

# Define our prompt (NOT a list)
prompt = """You are an expert in converting English questions to SQL query!
The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION.

For example:
Example 1 - How many entries of records are present?
→ SELECT COUNT(*) FROM STUDENT;

Example 2 - Tell me all the students studying in Data Science class?
→ SELECT * FROM STUDENT WHERE CLASS = "Data Science";

Do not include the word 'sql' in the output and avoid using triple quotes in the response.
Only return a valid SQL query that can run on the STUDENT table.
"""

# Streamlit app
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App to Retrieve SQL Data")

question = st.text_input("Input your question in plain English:", key="input")
submit = st.button("Ask the question")

# If submit is clicked
if submit and question:
    with st.spinner("Generating SQL from your question..."):
        sql_query = get_gemini_response(question, prompt)
        st.code(sql_query, language='sql')

        with st.spinner("Querying database..."):
            data = read_sql_query(sql_query, "student.db")
            st.subheader("The response is:")
            st.write(data)
