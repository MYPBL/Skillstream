"""
Add quiz data to existing assets in the database.
This script populates the quiz_data field for learning assets.
"""
from sqlmodel import Session, select
from app.core.database import engine
from app.models.models import Asset

def add_quiz_data():
    with Session(engine) as session:
        # Get all assets
        assets = session.exec(select(Asset)).all()
        
        print(f"Found {len(assets)} assets in database")
        
        # Quiz data for Python assets
        python_quiz = [
            {
                "id": "q1",
                "question": "What is the correct way to create a list in Python?",
                "options": [
                    "list = (1, 2, 3)",
                    "list = [1, 2, 3]",
                    "list = {1, 2, 3}",
                    "list = <1, 2, 3>"
                ],
                "correct_index": 1
            },
            {
                "id": "q2",
                "question": "Which keyword is used to define a function in Python?",
                "options": [
                    "function",
                    "def",
                    "func",
                    "define"
                ],
                "correct_index": 1
            },
            {
                "id": "q3",
                "question": "What does the 'print()' function do?",
                "options": [
                    "Saves data to a file",
                    "Displays output to the console",
                    "Creates a new variable",
                    "Deletes a variable"
                ],
                "correct_index": 1
            },
            {
                "id": "q4",
                "question": "How do you start a comment in Python?",
                "options": [
                    "//",
                    "/*",
                    "#",
                    "--"
                ],
                "correct_index": 2
            },
            {
                "id": "q5",
                "question": "What is the output of: type([])?",
                "options": [
                    "<class 'dict'>",
                    "<class 'list'>",
                    "<class 'tuple'>",
                    "<class 'set'>"
                ],
                "correct_index": 1
            }
        ]
        
        # Advanced Python quiz
        advanced_python_quiz = [
            {
                "id": "q1",
                "question": "What is a decorator in Python?",
                "options": [
                    "A function that modifies another function",
                    "A type of loop",
                    "A data structure",
                    "A comment style"
                ],
                "correct_index": 0
            },
            {
                "id": "q2",
                "question": "What does the '@' symbol indicate in Python?",
                "options": [
                    "Email address",
                    "Decorator syntax",
                    "String formatting",
                    "Mathematical operation"
                ],
                "correct_index": 1
            },
            {
                "id": "q3",
                "question": "Which of these is a higher-order function?",
                "options": [
                    "print()",
                    "len()",
                    "map()",
                    "type()"
                ],
                "correct_index": 2
            }
        ]
        
        # Cheatsheets
        python_cheatsheet = """
Python Basics Cheatsheet:

1. Variables: name = "value"
2. Lists: my_list = [1, 2, 3]
3. Functions: def my_function():
4. Comments: # This is a comment
5. Print: print("Hello World")

Key Concepts:
- Indentation matters in Python
- Use def to define functions
- Lists use square brackets []
- Strings can use " or '
"""
        
        decorator_cheatsheet = """
Decorators Cheatsheet:

1. Basic Syntax:
   @decorator_name
   def function():
       pass

2. Decorators are functions that modify other functions
3. Use @ symbol before function definition
4. Common decorators: @staticmethod, @property, @classmethod

Example:
def my_decorator(func):
    def wrapper():
        print("Before")
        func()
        print("After")
    return wrapper
"""
        
        # Update assets with quiz data
        updated_count = 0
        for asset in assets:
            if "Python" in asset.title or "python" in asset.title.lower():
                if "Decorator" in asset.title or asset.difficulty_level >= 3:
                    asset.quiz_data = advanced_python_quiz
                    asset.cheatsheet = decorator_cheatsheet
                else:
                    asset.quiz_data = python_quiz
                    asset.cheatsheet = python_cheatsheet
                
                session.add(asset)
                updated_count += 1
                print(f"✅ Added quiz to: {asset.title}")
        
        session.commit()
        print(f"\n✅ Successfully added quiz data to {updated_count} assets!")
        print("\nAssets with quiz data:")
        
        # Verify
        assets_with_quiz = session.exec(
            select(Asset).where(Asset.quiz_data != None)
        ).all()
        
        for asset in assets_with_quiz:
            print(f"  - {asset.title} ({len(asset.quiz_data)} questions)")

if __name__ == "__main__":
    add_quiz_data()
