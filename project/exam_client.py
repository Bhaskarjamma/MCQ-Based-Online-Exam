import datetime
import logging
import random
from question_master import QuestionManager

# Setup logging
logging.basicConfig(filename='exam_client.log', level=logging.INFO)

def take_exam(manager, num_questions=5):
    name = input("Enter student name: ")
    university = input("Enter university: ")
    score = 0

    print(f"\nToday's date and time: {datetime.datetime.now().strftime('%d/%b/%Y %H.%M.%S')}\n")

    # Select a fixed number of random questions
    if len(manager.questions) < num_questions:
        logging.error("Not enough questions available.")
        print(f"Not enough questions available. Available: {len(manager.questions)}, Required: {num_questions}")
        return

    selected_questions = random.sample(manager.questions, num_questions)

    for idx, question in enumerate(selected_questions, start=1):
        print(f"{idx}) {question.question}")
        for option_idx, option in enumerate(question.options, start=1):
            print(f"   op{option_idx}) {option}")
        
        answer = input("Enter your choice: ")
        if answer == question.correct_option:
            score += 1

    print(f"\nStudent name: {name}")
    print(f"University: {university}")
    print(f"Marks scored: {score} correct out of {num_questions} questions")
    logging.info(f"Exam completed for {name}, Score: {score}")

if __name__ == "__main__":
    manager = QuestionManager()
    take_exam(manager, num_questions=5)  # Change the number of questions here if needed
