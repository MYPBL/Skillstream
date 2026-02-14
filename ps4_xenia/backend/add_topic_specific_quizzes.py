"""
Topic-Specific Quiz Generator
Updates assets with quizzes tailored to their specific content topic.
"""
from sqlmodel import Session, select
from app.core.database import engine
from app.models.models import Asset

# ============================================
# SPECIFIC QUIZZES BY ASSET TITLE
# ============================================

QUIZ_MAP = {
    # 1. Intro to Python
    "Intro to Python": {
        "questions": [
            {
                "id": "intro_1",
                "question": "Which function displays text to the screen?",
                "options": ["show()", "out()", "print()", "display()"],
                "correct_index": 2
            },
            {
                "id": "intro_2",
                "question": "How do you create a variable named x with value 5?",
                "options": ["x = 5", "int x = 5", "let x = 5", "var x = 5"],
                "correct_index": 0
            },
            {
                "id": "intro_3",
                "question": "What is the correct file extension for Python files?",
                "options": [".pt", ".pyth", ".py", ".p"],
                "correct_index": 2
            },
            {
                "id": "intro_4",
                "question": "Which character starts a comment in Python?",
                "options": ["//", "#", "/*", "--"],
                "correct_index": 1
            },
            {
                "id": "intro_5",
                "question": "What data type is 'Hello'?",
                "options": ["int", "char", "str", "float"],
                "correct_index": 2
            }
        ],
        "cheatsheet": """
# Intro to Python Cheatsheet
- **Print**: `print("Hello")`
- **Variables**: `x = 5` (No type declaration needed)
- **Strings**: Use single `'` or double `"` quotes
- **Comments**: Start with `#`
- **Extensions**: Python files end in `.py`
"""
    },

    # 2. Python Syntax Guide
    "Python Syntax Guide": {
        "questions": [
            {
                "id": "syntax_1",
                "question": "How does Python define code blocks?",
                "options": ["Curly braces {}", "Semi-colons ;", "Indentation", "Keywords begin/end"],
                "correct_index": 2
            },
            {
                "id": "syntax_2",
                "question": "Which is a valid variable name?",
                "options": ["2myvar", "my-var", "my_var", "my var"],
                "correct_index": 2
            },
            {
                "id": "syntax_3",
                "question": "How do you start an if statement?",
                "options": ["if (x > 5)", "if x > 5:", "if x > 5 then", "check x > 5"],
                "correct_index": 1
            },
            {
                "id": "syntax_4",
                "question": "True or False: Python is case-sensitive.",
                "options": ["True", "False", "Only for variables", "Only for functions"],
                "correct_index": 0
            },
            {
                "id": "syntax_5",
                "question": "What is the correct way to write a multi-line string?",
                "options": ["Using triple quotes \"\"\"", "Using brackets []", "Using slashes //", "Using #"],
                "correct_index": 0
            }
        ],
        "cheatsheet": """
# Python Syntax Cheatsheet
- **Indentation**: Use 4 spaces for code blocks (if, def, loops).
- **Case Sensitivity**: `Var` and `var` are different.
- **Naming**: Use `snake_case` for variables, `CamelCase` for classes.
- **Colon**: Statements ending in `:` expect an indented block.
- **Multi-line**: Use triple quotes `\"\"\"` for docstrings.
"""
    },

    # 3. Python Lists & Dicts
    "Python Lists & Dicts": {
        "questions": [
            {
                "id": "ld_1",
                "question": "Which brackets are used for Lists?",
                "options": ["()", "{}", "[]", "<>"],
                "correct_index": 2
            },
            {
                "id": "ld_2",
                "question": "Which brackets are used for Dictionaries?",
                "options": ["()", "{}", "[]", "<>"],
                "correct_index": 1
            },
            {
                "id": "ld_3",
                "question": "How do you access the value for key 'name' in dict d?",
                "options": ["d.name", "d['name']", "d(name)", "d->name"],
                "correct_index": 1
            },
            {
                "id": "ld_4",
                "question": "Lists are mutable. What does this mean?",
                "options": ["They cannot be changed", "They can be changed after creation", "They are sorted", "They are unique"],
                "correct_index": 1
            },
            {
                "id": "ld_5",
                "question": "What happens if you look up a non-existent key in a dict?",
                "options": ["Returns None", "Returns Null", "Raises KeyError", "Returns False"],
                "correct_index": 2
            },
            {
                "id": "ld_6",
                "question": "Which method adds an item to the end of a list?",
                "options": ["push()", "add()", "append()", "insert()"],
                "correct_index": 2
            },
            {
                "id": "ld_7",
                "question": "How do you remove the last item from a list?",
                "options": ["remove()", "delete()", "pop()", "back()"],
                "correct_index": 2
            }
        ],
        "cheatsheet": """
# Lists & Dicts Cheatsheet
- **Lists**: Ordered, mutable. `l = [1, 2]`
  - Access: `l[0]`
  - Add: `l.append(3)`
  - Remove: `l.pop()`
- **Dicts**: Key-Value pairs. `d = {'k': 'v'}`
  - Access: `d['k']`
  - Get safe: `d.get('k')`
  - Add/Update: `d['k'] = 'new'`
"""
    },

    # 4. Interactive Python Shell
    "Interactive Python Shell": {
        "questions": [
            {
                "id": "repl_1",
                "question": "What does REPL stand for?",
                "options": ["Read Eval Print Loop", "Run Execute Program Loop", "Read Edit Print Line", "Real Escape Print Line"],
                "correct_index": 0
            },
            {
                "id": "repl_2",
                "question": "What symbol indicates the Python shell prompt?",
                "options": [">>", ">>>", "$", "#"],
                "correct_index": 1
            },
            {
                "id": "repl_3",
                "question": "Which function shows available methods for an object?",
                "options": ["list()", "show()", "dir()", "methods()"],
                "correct_index": 2
            },
            {
                "id": "repl_4",
                "question": "Which function brings up documentation?",
                "options": ["doc()", "info()", "help()", "man()"],
                "correct_index": 2
            },
            {
                "id": "repl_5",
                "question": "How do you exit the Python shell?",
                "options": ["exit()", "quit()", "Ctrl+D", "All of the above"],
                "correct_index": 3
            }
        ],
        "cheatsheet": """
# Python Shell Cheatsheet
- **Prompt**: `>>>` means ready for input.
- **Inspect**: `type(x)` shows type, `dir(x)` shows attributes.
- **Docs**: `help(x)` or `help("topic")`.
- **Exit**: `exit()` or `Ctrl+Z` (Win) / `Ctrl+D` (Unix).
- **History**: Use Up/Down arrows to recall commands.
"""
    },

    # 5. Decorators Explained
    "Decorators Explained": {
        "questions": [
            {
                "id": "dec_1",
                "question": "A decorator is essentially a...",
                "options": ["Class", "String", "Function that takes a function", "Loop"],
                "correct_index": 2
            },
            {
                "id": "dec_2",
                "question": "What syntax applies a decorator?",
                "options": ["&name", "#name", "@name", "$name"],
                "correct_index": 2
            },
            {
                "id": "dec_3",
                "question": "A common use case for decorators is...",
                "options": ["Logging", "Authentication checking", "Timing functions", "All of the above"],
                "correct_index": 3
            },
            {
                "id": "dec_4",
                "question": "Does a decorator modify the original function?",
                "options": ["No, it wraps it", "Yes, it deletes it", "No, it copies it", "Yes, it renames it"],
                "correct_index": 0
            },
            {
                "id": "dec_5",
                "question": "What does functools.wraps do?",
                "options": ["Wraps text", "Preserves metadata of the original function", "Speeds up code", "Deletes the function"],
                "correct_index": 1
            }
        ],
        "cheatsheet": """
# Decorators Cheatsheet
- **Concept**: A function that wraps another function to extend behavior.
- **Syntax**: Place `@decorator_name` above definition.
- **Structure**:
  ```python
  def my_decorator(func):
      def wrapper():
          # do something before
          func()
          # do something after
      return wrapper
  ```
- **Best Practice**: Use `@functools.wraps(func)` to preserve docstrings.
"""
    }
}

def update_topic_quizzes():
    with Session(engine) as session:
        assets = session.exec(select(Asset)).all()
        print(f"Checking {len(assets)} assets for specific quiz updates...\n")
        
        updated_count = 0
        
        for asset in assets:
            if asset.title in QUIZ_MAP:
                data = QUIZ_MAP[asset.title]
                asset.quiz_data = data["questions"]
                asset.cheatsheet = data["cheatsheet"]
                session.add(asset)
                updated_count += 1
                print(f"✅ Updated '{asset.title}' with {len(data['questions'])} specific questions.")
            else:
                print(f"ℹ️  Skipping '{asset.title}' (No specific map found)")
        
        session.commit()
        print(f"\n🎉 Successfully updated {updated_count} assets with topic-specific quizzes!")

if __name__ == "__main__":
    update_topic_quizzes()
