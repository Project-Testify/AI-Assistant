import re

def handle_mcq(response):
    try:
        question = dict(response)
        # Extract question, options, and correct answer from the dictionary
        question = response.get('question', 'No question provided')
        options = response.get('options', [])
        correct_answer = response.get('correct_answer', 'No correct answer provided')

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
            else:
                correct_answer_index = ord(correct_answer.lower()) - 97
            



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
