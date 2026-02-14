"""
Comprehensive Quiz Data Generator
Adds quizzes with Easy, Moderate, and Hard difficulty levels to all assets.
"""
from sqlmodel import Session, select
from app.core.database import engine
from app.models.models import Asset

# ============================================
# QUIZ QUESTIONS BY TOPIC AND DIFFICULTY
# ============================================

PYTHON_QUIZZES = {
    "easy": [
        {
            "id": "py_e1",
            "question": "What is the correct way to create a list in Python?",
            "options": ["list = (1, 2, 3)", "list = [1, 2, 3]", "list = {1, 2, 3}", "list = <1, 2, 3>"],
            "correct_index": 1,
            "difficulty": "easy"
        },
        {
            "id": "py_e2",
            "question": "Which keyword is used to define a function in Python?",
            "options": ["function", "def", "func", "define"],
            "correct_index": 1,
            "difficulty": "easy"
        },
        {
            "id": "py_e3",
            "question": "What does the 'print()' function do?",
            "options": ["Saves data to a file", "Displays output to the console", "Creates a new variable", "Deletes a variable"],
            "correct_index": 1,
            "difficulty": "easy"
        },
        {
            "id": "py_e4",
            "question": "How do you start a comment in Python?",
            "options": ["//", "/*", "#", "--"],
            "correct_index": 2,
            "difficulty": "easy"
        },
        {
            "id": "py_e5",
            "question": "What is the output of: type([])?",
            "options": ["<class 'dict'>", "<class 'list'>", "<class 'tuple'>", "<class 'set'>"],
            "correct_index": 1,
            "difficulty": "easy"
        }
    ],
    "moderate": [
        {
            "id": "py_m1",
            "question": "What is the difference between a list and a tuple in Python?",
            "options": ["Lists are immutable, tuples are mutable", "Lists are mutable, tuples are immutable", "No difference", "Tuples can only store strings"],
            "correct_index": 1,
            "difficulty": "moderate"
        },
        {
            "id": "py_m2",
            "question": "What does the 'lambda' keyword create?",
            "options": ["A class", "An anonymous function", "A loop", "A variable"],
            "correct_index": 1,
            "difficulty": "moderate"
        },
        {
            "id": "py_m3",
            "question": "Which method adds an element to the end of a list?",
            "options": ["add()", "append()", "insert()", "push()"],
            "correct_index": 1,
            "difficulty": "moderate"
        },
        {
            "id": "py_m4",
            "question": "What is list comprehension?",
            "options": ["A way to read lists", "A concise way to create lists", "A type of loop", "A debugging tool"],
            "correct_index": 1,
            "difficulty": "moderate"
        },
        {
            "id": "py_m5",
            "question": "What does 'self' represent in a Python class?",
            "options": ["The class itself", "The instance of the class", "A global variable", "A function parameter"],
            "correct_index": 1,
            "difficulty": "moderate"
        },
        {
            "id": "py_m6",
            "question": "Which of these is NOT a valid Python data type?",
            "options": ["int", "float", "char", "str"],
            "correct_index": 2,
            "difficulty": "moderate"
        },
        {
            "id": "py_m7",
            "question": "What does the 'with' statement do?",
            "options": ["Creates a loop", "Handles context management", "Defines a function", "Imports a module"],
            "correct_index": 1,
            "difficulty": "moderate"
        }
    ],
    "hard": [
        {
            "id": "py_h1",
            "question": "What is a decorator in Python?",
            "options": ["A function that modifies another function", "A type of loop", "A data structure", "A comment style"],
            "correct_index": 0,
            "difficulty": "hard"
        },
        {
            "id": "py_h2",
            "question": "What is the difference between __str__ and __repr__?",
            "options": ["No difference", "__str__ is for users, __repr__ is for developers", "__repr__ is deprecated", "__str__ is faster"],
            "correct_index": 1,
            "difficulty": "hard"
        },
        {
            "id": "py_h3",
            "question": "What does the GIL (Global Interpreter Lock) do?",
            "options": ["Speeds up code", "Allows only one thread to execute Python bytecode at a time", "Manages memory", "Handles exceptions"],
            "correct_index": 1,
            "difficulty": "hard"
        },
        {
            "id": "py_h4",
            "question": "What is a generator in Python?",
            "options": ["A random number creator", "A function that returns an iterator using yield", "A class constructor", "A type of loop"],
            "correct_index": 1,
            "difficulty": "hard"
        },
        {
            "id": "py_h5",
            "question": "What is metaclass in Python?",
            "options": ["A class of classes", "A deprecated feature", "A type of function", "A module"],
            "correct_index": 0,
            "difficulty": "hard"
        },
        {
            "id": "py_h6",
            "question": "What does *args and **kwargs allow?",
            "options": ["Variable number of arguments", "Fixed arguments only", "No arguments", "Only keyword arguments"],
            "correct_index": 0,
            "difficulty": "hard"
        },
        {
            "id": "py_h7",
            "question": "What is the purpose of __init__.py?",
            "options": ["Initialize variables", "Mark directory as Python package", "Start the program", "Import modules"],
            "correct_index": 1,
            "difficulty": "hard"
        },
        {
            "id": "py_h8",
            "question": "What is monkey patching?",
            "options": ["Debugging technique", "Dynamically modifying a class or module at runtime", "Error handling", "Code optimization"],
            "correct_index": 1,
            "difficulty": "hard"
        },
        {
            "id": "py_h9",
            "question": "What does the @property decorator do?",
            "options": ["Creates a class", "Allows method to be accessed like an attribute", "Defines a constant", "Imports a module"],
            "correct_index": 1,
            "difficulty": "hard"
        },
        {
            "id": "py_h10",
            "question": "What is the difference between deepcopy and copy?",
            "options": ["No difference", "deepcopy creates recursive copies, copy creates shallow copies", "copy is faster", "deepcopy is deprecated"],
            "correct_index": 1,
            "difficulty": "hard"
        }
    ]
}

REACT_QUIZZES = {
    "easy": [
        {
            "id": "react_e1",
            "question": "What is React?",
            "options": ["A database", "A JavaScript library for building UIs", "A CSS framework", "A backend framework"],
            "correct_index": 1,
            "difficulty": "easy"
        },
        {
            "id": "react_e2",
            "question": "What is JSX?",
            "options": ["A database query language", "JavaScript XML syntax extension", "A CSS preprocessor", "A testing framework"],
            "correct_index": 1,
            "difficulty": "easy"
        },
        {
            "id": "react_e3",
            "question": "What is a component in React?",
            "options": ["A CSS file", "A reusable piece of UI", "A database table", "A server"],
            "correct_index": 1,
            "difficulty": "easy"
        },
        {
            "id": "react_e4",
            "question": "How do you create a React component?",
            "options": ["Using function or class", "Only with classes", "Only with functions", "Using HTML only"],
            "correct_index": 0,
            "difficulty": "easy"
        },
        {
            "id": "react_e5",
            "question": "What is the virtual DOM?",
            "options": ["A database", "A lightweight copy of the actual DOM", "A CSS framework", "A testing tool"],
            "correct_index": 1,
            "difficulty": "easy"
        }
    ],
    "moderate": [
        {
            "id": "react_m1",
            "question": "What is the purpose of useState hook?",
            "options": ["To fetch data", "To manage component state", "To style components", "To route pages"],
            "correct_index": 1,
            "difficulty": "moderate"
        },
        {
            "id": "react_m2",
            "question": "What is useEffect used for?",
            "options": ["Styling", "Side effects and lifecycle methods", "Routing", "State management"],
            "correct_index": 1,
            "difficulty": "moderate"
        },
        {
            "id": "react_m3",
            "question": "What are props in React?",
            "options": ["CSS properties", "Data passed from parent to child components", "Database fields", "Server endpoints"],
            "correct_index": 1,
            "difficulty": "moderate"
        },
        {
            "id": "react_m4",
            "question": "What is the difference between state and props?",
            "options": ["No difference", "State is mutable, props are immutable", "Props are mutable, state is immutable", "Both are immutable"],
            "correct_index": 1,
            "difficulty": "moderate"
        },
        {
            "id": "react_m5",
            "question": "What is React Router used for?",
            "options": ["State management", "Navigation between pages", "API calls", "Styling"],
            "correct_index": 1,
            "difficulty": "moderate"
        },
        {
            "id": "react_m6",
            "question": "What is the key prop used for?",
            "options": ["Styling", "Helping React identify which items changed", "API authentication", "Routing"],
            "correct_index": 1,
            "difficulty": "moderate"
        },
        {
            "id": "react_m7",
            "question": "What is conditional rendering?",
            "options": ["Rendering based on conditions", "Always rendering everything", "Never rendering", "Rendering CSS"],
            "correct_index": 0,
            "difficulty": "moderate"
        }
    ],
    "hard": [
        {
            "id": "react_h1",
            "question": "What is React Context API used for?",
            "options": ["Routing", "Global state management without prop drilling", "Styling", "API calls"],
            "correct_index": 1,
            "difficulty": "hard"
        },
        {
            "id": "react_h2",
            "question": "What is the purpose of useMemo?",
            "options": ["To store data", "To memoize expensive calculations", "To make API calls", "To style components"],
            "correct_index": 1,
            "difficulty": "hard"
        },
        {
            "id": "react_h3",
            "question": "What is useCallback used for?",
            "options": ["API calls", "Memoizing callback functions", "Routing", "Styling"],
            "correct_index": 1,
            "difficulty": "hard"
        },
        {
            "id": "react_h4",
            "question": "What is React.memo()?",
            "options": ["A hook", "A higher-order component for performance optimization", "A routing function", "A styling tool"],
            "correct_index": 1,
            "difficulty": "hard"
        },
        {
            "id": "react_h5",
            "question": "What is the difference between useEffect and useLayoutEffect?",
            "options": ["No difference", "useLayoutEffect fires synchronously after DOM mutations", "useEffect is deprecated", "useLayoutEffect is for styling only"],
            "correct_index": 1,
            "difficulty": "hard"
        },
        {
            "id": "react_h6",
            "question": "What is React Fiber?",
            "options": ["A CSS framework", "React's reconciliation algorithm", "A routing library", "A testing tool"],
            "correct_index": 1,
            "difficulty": "hard"
        },
        {
            "id": "react_h7",
            "question": "What is code splitting in React?",
            "options": ["Dividing CSS files", "Lazy loading components to reduce bundle size", "Splitting databases", "Dividing teams"],
            "correct_index": 1,
            "difficulty": "hard"
        },
        {
            "id": "react_h8",
            "question": "What is the purpose of useReducer?",
            "options": ["To reduce file size", "Complex state management with actions", "To make API calls", "To style components"],
            "correct_index": 1,
            "difficulty": "hard"
        },
        {
            "id": "react_h9",
            "question": "What are custom hooks?",
            "options": ["Built-in hooks", "Reusable stateful logic extracted into functions", "CSS hooks", "Database hooks"],
            "correct_index": 1,
            "difficulty": "hard"
        },
        {
            "id": "react_h10",
            "question": "What is React Suspense used for?",
            "options": ["Styling", "Handling asynchronous operations and code splitting", "Routing", "State management"],
            "correct_index": 1,
            "difficulty": "hard"
        }
    ]
}

# Cheatsheets
PYTHON_CHEATSHEET_EASY = """Python Basics Cheatsheet:

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

PYTHON_CHEATSHEET_MODERATE = """Python Intermediate Cheatsheet:

1. List Comprehension: [x*2 for x in range(10)]
2. Lambda: lambda x: x + 1
3. Classes: class MyClass:
4. Inheritance: class Child(Parent):
5. Exception Handling: try/except/finally

Key Concepts:
- Tuples are immutable: (1, 2, 3)
- Dictionaries: {"key": "value"}
- List methods: append(), extend(), pop()
- String methods: split(), join(), replace()
"""

PYTHON_CHEATSHEET_HARD = """Python Advanced Cheatsheet:

1. Decorators: @decorator_name
2. Generators: yield keyword
3. Context Managers: with statement
4. Metaclasses: type() and __metaclass__
5. *args, **kwargs for variable arguments

Key Concepts:
- GIL limits threading
- __str__ vs __repr__
- Monkey patching for runtime modifications
- @property for getter/setter
- deepcopy vs copy for objects
"""

REACT_CHEATSHEET_EASY = """React Basics Cheatsheet:

1. Components: function MyComponent() {}
2. JSX: <div>Hello</div>
3. Props: <Component name="value" />
4. Rendering: ReactDOM.render()
5. Virtual DOM: Efficient updates

Key Concepts:
- Components are reusable
- JSX combines HTML and JavaScript
- Props pass data down
- State manages component data
"""

REACT_CHEATSHEET_MODERATE = """React Intermediate Cheatsheet:

1. useState: const [state, setState] = useState()
2. useEffect: useEffect(() => {}, [])
3. Props vs State: Props immutable, State mutable
4. Conditional Rendering: {condition && <Component />}
5. Lists: map() with key prop

Key Concepts:
- Hooks replace class lifecycle
- useEffect for side effects
- Keys help React identify changes
- React Router for navigation
"""

REACT_CHEATSHEET_HARD = """React Advanced Cheatsheet:

1. Context API: createContext(), useContext()
2. useMemo: Memoize expensive calculations
3. useCallback: Memoize functions
4. useReducer: Complex state management
5. Custom Hooks: Reusable logic

Key Concepts:
- React Fiber: Reconciliation algorithm
- Code Splitting: React.lazy() and Suspense
- useLayoutEffect: Synchronous effects
- React.memo(): Component memoization
- Performance optimization techniques
"""

def add_comprehensive_quizzes():
    with Session(engine) as session:
        assets = session.exec(select(Asset)).all()
        print(f"Found {len(assets)} assets in database\n")
        
        updated_count = 0
        
        for asset in assets:
            title_lower = asset.title.lower()
            
            # Determine quiz type and difficulty
            if "python" in title_lower:
                if asset.difficulty_level <= 2:
                    asset.quiz_data = PYTHON_QUIZZES["easy"]
                    asset.cheatsheet = PYTHON_CHEATSHEET_EASY
                    difficulty = "Easy"
                elif asset.difficulty_level <= 4:
                    asset.quiz_data = PYTHON_QUIZZES["moderate"]
                    asset.cheatsheet = PYTHON_CHEATSHEET_MODERATE
                    difficulty = "Moderate"
                else:
                    asset.quiz_data = PYTHON_QUIZZES["hard"]
                    asset.cheatsheet = PYTHON_CHEATSHEET_HARD
                    difficulty = "Hard"
                    
            elif "react" in title_lower or "javascript" in title_lower or "js" in title_lower:
                if asset.difficulty_level <= 2:
                    asset.quiz_data = REACT_QUIZZES["easy"]
                    asset.cheatsheet = REACT_CHEATSHEET_EASY
                    difficulty = "Easy"
                elif asset.difficulty_level <= 4:
                    asset.quiz_data = REACT_QUIZZES["moderate"]
                    asset.cheatsheet = REACT_CHEATSHEET_MODERATE
                    difficulty = "Moderate"
                else:
                    asset.quiz_data = REACT_QUIZZES["hard"]
                    asset.cheatsheet = REACT_CHEATSHEET_HARD
                    difficulty = "Hard"
            else:
                # Default to Python quizzes for other topics
                if asset.difficulty_level <= 2:
                    asset.quiz_data = PYTHON_QUIZZES["easy"]
                    asset.cheatsheet = PYTHON_CHEATSHEET_EASY
                    difficulty = "Easy"
                elif asset.difficulty_level <= 4:
                    asset.quiz_data = PYTHON_QUIZZES["moderate"]
                    asset.cheatsheet = PYTHON_CHEATSHEET_MODERATE
                    difficulty = "Moderate"
                else:
                    asset.quiz_data = PYTHON_QUIZZES["hard"]
                    asset.cheatsheet = PYTHON_CHEATSHEET_HARD
                    difficulty = "Hard"
            
            session.add(asset)
            updated_count += 1
            print(f"✅ [{difficulty:8}] {asset.title} - {len(asset.quiz_data)} questions")
        
        session.commit()
        print(f"\n🎉 Successfully added quiz data to {updated_count} assets!")
        
        # Summary by difficulty
        print("\n📊 Summary:")
        easy_count = sum(1 for a in assets if a.difficulty_level <= 2)
        moderate_count = sum(1 for a in assets if 2 < a.difficulty_level <= 4)
        hard_count = sum(1 for a in assets if a.difficulty_level > 4)
        
        print(f"  Easy (5Q):     {easy_count} assets")
        print(f"  Moderate (7Q): {moderate_count} assets")
        print(f"  Hard (10Q):    {hard_count} assets")

if __name__ == "__main__":
    add_comprehensive_quizzes()
