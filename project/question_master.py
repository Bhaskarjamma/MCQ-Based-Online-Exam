import csv
import os
import logging

# Setup logging
logging.basicConfig(filename='question_master.log', level=logging.INFO)


class QuestionManager:
    def __init__(self, filename='questions.csv'):
        self.questions = []
        self.filename = filename
        self.load_questions()

    #Adding Question to the csv File
    def add_question(self, question_text, options, correct_option):
        num = len(self.questions) + 1
        question = Question(num, question_text, options, correct_option)
        self.questions.append(question)
        self.save_questions()
        logging.info(f"Question added: {question_text}")

    def search_question(self, num):
        for question in self.questions:
            if question.num == num:
                return question
        return None
    
    def delete_question(self, num):
        self.questions = [q for q in self.questions if q.num != num]
        self.save_questions()
        logging.info(f"Deleted question number: {num}")

    def modify_question(self, num, new_question_text, new_options, new_correct_option):
    # Ensure new_options is a non-empty list with valid options
        if not new_options or not isinstance(new_options, list) or len(new_options) == 0:
            logging.error("New options must be a non-empty list.")
            raise ValueError("Options must not be null or empty.")

        # Check that all options are non-null and non-empty strings
        for option in new_options:
            if option is None or not isinstance(option, str) or option.strip() == "":
                logging.error("All options must be valid (non-null and non-empty strings).")
                raise ValueError("All options must be valid (non-null and non-empty strings).")

        # Check if the question number exists
        for question in self.questions:
            if question.num == num:
                question.question = new_question_text
                question.options = new_options
                question.correct_option = new_correct_option
                self.save_questions()
                logging.info(f"Modified question number: {num} to '{new_question_text}' with options {new_options}.")
                return

        logging.warning(f"Question number {num} not found for modification.")
        raise ValueError(f"Question number {num} does not exist.")




    def display_questions(self):
        for question in self.questions:
            print(f"{question.num}) {question.question}")
            for idx, option in enumerate(question.options, start=1):
                print(f"   opt {idx}) {option}")

    def load_questions(self):
        if os.path.exists(self.filename):
            with open(self.filename, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    num = int(row['num'])
                    question = row['question']
                    options = [row['option1'], row['option2'], row['option3'], row['option4']]
                    correct_option = row['correctoption']
                    self.questions.append(Question(num, question, options, correct_option))
            logging.info("Loaded questions from CSV.")
        else:
            logging.warning("CSV file not found. Starting with an empty question list.")

    def save_questions(self):
        with open(self.filename, mode='w', newline='') as file:
            fieldnames = ['num', 'question', 'option1', 'option2', 'option3', 'option4', 'correctoption']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for q in self.questions:
                writer.writerow({
                    'num': q.num,
                    'question': q.question,
                    'option1': q.options[0],
                    'option2': q.options[1],
                    'option3': q.options[2],
                    'option4': q.options[3],
                    'correctoption': q.correct_option
                })
            logging.info("Saved questions to CSV.")

    
class Question:
    def __init__(self, num, question, options, correct_option):
        self.num = num
        self.question = question
        self.options = options
        self.correct_option = correct_option


def menu():
    manager = QuestionManager()
    while True:
        print("\n--- Question Management Menu ---")
        print("1) Add a question")
        print("2) Search for a question")
        print("3) Delete question")
        print("4) Modify question")
        print("5) Display all questions")
        print("6) Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            question_text = input("Enter the question: ")
            options = [input(f"Enter option {i+1}: ") for i in range(4)]
            correct_option = input("Enter the correct option to save(e.g., op1): ")
            manager.add_question(question_text, options, correct_option)
        
        elif choice == '2':
            num = int(input("Enter question number to search: "))
            question = manager.search_question(num)
            if question:
                print(f"{question.num}) {question.question}")
                for idx, option in enumerate(question.options, start=1):
                    print(f"   op{idx}) {option}")
            else:
                print("Question not found.")
        
        elif choice == '3':
            num = int(input("Enter question number to delete: "))
            manager.delete_question(num)
        
        elif choice == '4':
            num = int(input("Enter question number to modify: "))
            new_question_text = input("Enter the new question: ")
            new_options = [input(f"Enter new option {i+1}: ") for i in range(4)]
            new_correct_option = input("Enter the new correct option (e.g., op1): ")
            manager.modify_question(num, new_question_text, new_options, new_correct_option)
        
        elif choice == '5':
            manager.display_questions()
        
        elif choice == '6':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

            

if __name__ == "__main__":
    menu()