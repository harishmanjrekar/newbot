from flask import Flask, request, jsonify
import openai
import pyodbc

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = "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"

# Database connection configuration
server = 'tcp:rihrih.database.windows.net'
database = 'dbChatbot'
username = 'rih'
password = 'Password1'
driver = '{ODBC Driver 18 for SQL Server'}  # Update to the appropriate driver

# Establish the connection
conn = pyodbc.connect(
    f'SERVER={server};DATABASE={database};UID={username};PWD={password};DRIVER={driver}'
)

@app.route('/get_answer', methods=['POST'])
def get_answer():
    user_input = request.json['user_input']
    
    response = openai.Completion.create(
        engine="davinci",
        prompt=user_input,
        max_tokens=150
    )
    
    answer = response.choices[0].text.strip()
    
    # Insert into database
    cursor = conn.cursor()
    query = "INSERT INTO ChatLogs (Question, Answer) VALUES (?, ?);"
    cursor.execute(query, user_input, answer)
    conn.commit()
    
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run()
