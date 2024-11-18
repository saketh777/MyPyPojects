import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, request, jsonify

# Function to connect to the database
def get_db_connection():
    return psycopg2.connect(
        dbname="survey_db",
        user="postgres",
        password="falconheavy",
        host="localhost",
        port="5432"
    )

# Function to create a survey
def create_survey(conn, title, description):
    query = "INSERT INTO Surveys (title, description) VALUES (%s, %s) RETURNING survey_id;"
    with conn.cursor() as cur:
        cur.execute(query, (title, description))
        survey_id = cur.fetchone()[0]
        conn.commit()
    return survey_id

# Function to add a question
def add_question(conn, survey_id, question_text, question_type):
    query = """
    INSERT INTO Questions (survey_id, question_text, question_type)
    VALUES (%s, %s, %s) RETURNING question_id;
    """
    with conn.cursor() as cur:
        cur.execute(query, (survey_id, question_text, question_type))
        question_id = cur.fetchone()[0]
        conn.commit()
    return question_id

# Function to add a response
def add_response(conn, survey_id, question_id, response_text):
    query = """
    INSERT INTO Responses (survey_id, question_id, response_text)
    VALUES (%s, %s, %s) RETURNING response_id;
    """
    with conn.cursor() as cur:
        cur.execute(query, (survey_id, question_id, response_text))
        response_id = cur.fetchone()[0]
        conn.commit()
    return response_id

# Function to get responses
def get_responses(conn, survey_id):
    query = """
    SELECT Questions.question_text, Responses.response_text
    FROM Responses
    JOIN Questions ON Responses.question_id = Questions.question_id
    WHERE Questions.survey_id = %s;
    """
    with conn.cursor() as cur:
        cur.execute(query, (survey_id,))
        responses = cur.fetchall()
    return responses

# Function to analyze responses
def analyze_responses(responses):
    response_counts = {}
    for _, response in responses:
        response_counts[response] = response_counts.get(response, 0) + 1
    
    # Visualization
    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(response_counts.keys()), y=list(response_counts.values()))
    plt.title("Survey Response Analysis")
    plt.xlabel("Responses")
    plt.ylabel("Frequency")
    plt.show()

# Flask Application
app = Flask(__name__)

@app.route("/create-survey", methods=["POST"])
def create_survey_endpoint():
    data = request.json
    conn = get_db_connection()
    survey_id = create_survey(conn, data['title'], data['description'])
    conn.close()
    return jsonify({"survey_id": survey_id})

if __name__ == "__main__":
    conn = get_db_connection()
    try:
        # Create survey and question
        survey_id = create_survey(conn, "Customer Feedback", "A survey to gather opinions.")
        print(f"Survey created with ID: {survey_id}")
        
        question_id = add_question(conn, survey_id, "How satisfied are you with our service?", "MCQ")
        print(f"Question added with ID: {question_id}")
        
        # Insert responses (Example)
        response_id = add_response(conn, survey_id, question_id, "Very Satisfied")
        print(f"Response added with ID: {response_id}")

        # Fetch responses for the survey
        responses = get_responses(conn, survey_id)
        for question, response in responses:
            print(f"Q: {question} | A: {response}")
        
        # Analyze responses (if any)
        if responses:
            analyze_responses(responses)
        else:
            print("No responses to analyze.")
    finally:
        conn.close()

