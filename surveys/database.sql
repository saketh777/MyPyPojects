-- Create the database
CREATE DATABASE survey_db;

-- Connect to the database (you'll use this in your PostgreSQL shell or GUI)
\c survey_db

-- Create the Surveys table
CREATE TABLE Surveys (
    survey_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the Questions table
CREATE TABLE Questions (
    question_id SERIAL PRIMARY KEY,
    survey_id INT REFERENCES Surveys(survey_id),
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL
);

-- Create the Responses table
CREATE TABLE Responses (
    response_id SERIAL PRIMARY KEY,
    survey_id INT REFERENCES Surveys(survey_id),
    question_id INT REFERENCES Questions(question_id),
    response_text TEXT NOT NULL
);
