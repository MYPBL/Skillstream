import sqlite3
import json
from datetime import datetime

DB_PATH = "c:/samiksha/ps4_xenia/backend/pdp_dev.db"

def migrate():
    print("🚀 Starting Phase 8 Migration...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Add Columns
    try:
        cursor.execute("ALTER TABLE asset ADD COLUMN quiz_data JSON")
        print("✅ Added 'quiz_data' column.")
    except sqlite3.OperationalError:
        print("ℹ️ 'quiz_data' column likely already exists.")

    try:
        cursor.execute("ALTER TABLE asset ADD COLUMN cheatsheet TEXT")
        print("✅ Added 'cheatsheet' column.")
    except sqlite3.OperationalError:
        print("ℹ️ 'cheatsheet' column likely already exists.")
        
    conn.commit()

    # 2. Seed Data for Python & React
    # Python Quiz
    python_quiz = [
        {
            "id": 1,
            "question": "What is the correct file extension for Python files?",
            "options": [".pt", ".py", ".pyt", ".p"],
            "correct_index": 1
        },
        {
            "id": 2,
            "question": "Which keyword is used to create a function in Python?",
            "options": ["func", "def", "function", "create"],
            "correct_index": 1
        },
        {
            "id": 3,
            "question": "How do you print 'Hello World' in Python 3?",
            "options": ["echo 'Hello World'", "print('Hello World')", "console.log('Hello World')", "printf('Hello World')"],
            "correct_index": 1
        },
        {
            "id": 4,
            "question": "Which data type is immutable?",
            "options": ["List", "Dictionary", "Set", "Tuple"],
            "correct_index": 3
        },
        {
            "id": 5,
            "question": "What does PIP stand for?",
            "options": ["Pip Install Packages", "Preferred Installer Program", "Python Package Index", "Pip Installs Packages"],
            "correct_index": 3
        }
    ]
    
    python_cheatsheet = """
# Python Basics Cheatsheet

## Syntax
- **Print**: `print("Hello")`
- **Variables**: `x = 5`, `name = "Alice"` (Dynamic typing)

## Data Structures
- **List**: `[1, 2, 3]` (Mutable)
- **Tuple**: `(1, 2, 3)` (Immutable)
- **Dictionary**: `{"key": "value"}` (Key-Value pairs)

## Functions
```python
def my_function(arg):
    return arg * 2
```

## loops
- `for i in range(5):`
- `while x < 10:`
    """

    # React Quiz
    react_quiz = [
        {
            "id": 1,
            "question": "What is the primary building block of React?",
            "options": ["function", "class", "Component", "element"],
            "correct_index": 2
        },
        {
            "id": 2,
            "question": "Which hook is used for side effects?",
            "options": ["useState", "useEffect", "useContext", "useReducer"],
            "correct_index": 1
        },
        {
            "id": 3,
            "question": "What syntax does React use to describe UI?",
            "options": ["HTML", "XML", "JSX", "Markdown"],
            "correct_index": 2
        },
         {
            "id": 4,
            "question": "How do you pass data to child components?",
            "options": ["State", "Props", "Context", "Redux"],
            "correct_index": 1
        },
        {
            "id": 5,
            "question": "Which method is used to update state in a functional component?",
            "options": ["this.setState", "updateState", "Using the setter from useState", "forceUpdate"],
            "correct_index": 2
        }
    ]
    
    react_cheatsheet = """
# React Basics Cheatsheet

## Components
- **Functional**: `function MyComponent() { return <div>Hi</div>; }`
- **JSX**: HTML-like syntax inside JavaScript.

## Hooks
- **useState**: Manage local state.
  `const [count, setCount] = useState(0);`
- **useEffect**: Side effects (fetching data, subscriptions).
  `useEffect(() => { ... }, [dependencies]);`

## Props
- Pass data *down* component tree.
- Read-only (immutable).
    """

    # Update Assets based on Title Keywords OR Skill Tag
    cursor.execute("UPDATE asset SET quiz_data = ?, cheatsheet = ? WHERE title LIKE '%Python%' OR skill_tag = 'Python'", (json.dumps(python_quiz), python_cheatsheet))
    print(f"✅ Updated Python assets (Rows affected: {cursor.rowcount})")

    cursor.execute("UPDATE asset SET quiz_data = ?, cheatsheet = ? WHERE title LIKE '%React%' OR title LIKE '%Frontend%' OR skill_tag = 'React' OR skill_tag = 'Frontend'", (json.dumps(react_quiz), react_cheatsheet))
    print(f"✅ Updated React assets (Rows affected: {cursor.rowcount})")

    conn.commit()
    conn.close()
    print("✨ Migration Complete!")

if __name__ == "__main__":
    migrate()
