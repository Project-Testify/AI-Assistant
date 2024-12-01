import re

def handle_mcq(response):
    try:
        question = dict(response)
        # Extract question, options, and correct answer from the dictionary
        question = response.get('question', 'No question provided')
        options = response.get('options', [])
        # correct_answer = response.get('correct_answer', 'No correct answer provided') 
        # # or 
        # correct_answer = response.get('answer', 'No correct answer provided')
        # correct_answer = response.get('correct_answer', response.get('answer', 'No correct answer provided'))
# correctAnswer
        correct_answer = response.get('answer', response.get('correctAnswer', response.get('correct_answer', 'No correct answer provided')))

        # If correct answer is not provided, return None
        if not options:
            return None
                


        # Print the options
        for option in options:
            print(option)
        
        # Get index of correct answer
        try:
            correct_answer_index = options.index(correct_answer)
        except:
            # if correct answer is given as a letter, convert it to index. support for uppercase and lowercase
            # if correct answer is given by number, convert it to index
            if correct_answer.isdigit():
                correct_answer_index = int(correct_answer) - 1
            elif correct_answer.isalpha() and len(correct_answer) == 1:
                correct_answer_index = ord(correct_answer.lower()) - 97
            else:
                correct_answer_index = None

            
            



        # Remove option letter from options, it can be A) or A. using regex
        cleaned_options = [re.sub(r'^[A-Za-z]\)\s*|^[A-Za-z]\.\s*', '', option).strip() for option in options]

        # Return as dictionary
        # return {
        #     "question": question,
        #     "options": cleaned_options,
        #     "correct_answer": correct_answer_index
        # }
        print(correct_answer_index)
        response_options = []
        for index, option in enumerate(options):
            response_options.append({
                "optionText": option,
                "marks": 1 if index == correct_answer_index else 0,
                "correct": index == correct_answer_index
            })

        response = {
            "questionText": question,
            "difficultyLevel": "EASY",  # Or determined dynamically based on your criteria
            "options": response_options
        }
        return response

    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
# response = {
#   "question": "Which of the following best describes the role of the lexical analyzer (lexical analysis) in a compiler?",
#   "options": [
#     "A) It checks the source program for semantic consistency with the language definition.",
#     "B) It reads the stream of characters making up the source program and groups the characters into meaningful sequences called lexemes.",
#     "C) It converts the intermediate representation of the source program into machine code.",
#     "D) It creates a tree-like intermediate representation of the grammatical structure of the token stream."
#   ],
#   "correct_answer": "B) It reads the stream of characters making up the source program and groups the characters into meaningful sequences called lexemes."
# }

# parsed_data = handle_mcq(response)
# print(parsed_data)


def handle_essay(original_question):
    # Original data format
    question = original_question["question"]
    answers = original_question["answers"]

    # New data structure
    new_question = {
        "questionText": question,
        "difficultyLevel": "MEDIUM",  # Static value, change as needed
        "coveringPoints": []
    }

    # Convert each answer to a covering point
    for answer in answers:
        new_question["coveringPoints"].append({
            "coveringPointText": answer,
            "marks": 5  # Assuming each point is worth 5 marks
        })

    return new_question



