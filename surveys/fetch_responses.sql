SELECT question_text, response_text
FROM Responses
JOIN Questions ON Responses.question_id = Questions.question_id
WHERE survey_id = %s;

INSERT INTO Responses (question_id, response_text)
VALUES (1, 'Very Satisfied');
INSERT INTO Responses (survey_id, question_id, response_text) 
VALUES 
    (9, 7, 'Very Satisfied'),
    (9, 7, 'Satisfied'),
    (9, 7, 'Neutral'),
    (9, 7, 'Dissatisfied'),
    (9, 7, 'Very Satisfied');
