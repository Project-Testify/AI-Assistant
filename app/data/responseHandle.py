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
        return {
            "question": question,
            "options": cleaned_options,
            "correct_answer": correct_answer_index
        }

    except Exception as e:
        print(f"Error: {e}")
        return None


def handle_grade(response):
    print("Handling grade response")
    print(response)
    
    # Try to get the points with the first key format
    correct_points = response.get('correct')
    incorrect_points = response.get('incorrect')
    
    # If the first format keys are not found, try the second format
    if correct_points is None and incorrect_points is None:
        correct_points = response.get('correct_points')
        incorrect_points = response.get('incorrect_points')
    
    # If the second format keys are not found, try the third format
    if correct_points is None and incorrect_points is None:
        correct_points = response.get('correctPoints', [])
        incorrect_points = response.get('incorrectPoints', [])
    
    return {
        "correct_points": correct_points,
        "incorrect_points": incorrect_points
    }

    
       



# {
#   "correct_points": [
#     "The discontent among Indian soldiers due to cultural insensitivity"
#   ],
#   "incorrect_points": [
#     "The introduction of Western-style education",
#     "The establishment of the Indian National Congress"
#   ]
# }


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
