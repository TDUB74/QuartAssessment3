import sqlite3
import tkinter as tk
from tkinter import messagebox
import random

class Question:
    def __init__(self, prompt, options, correct_answer):
        self.prompt = prompt
        self.options = options
        self.correct_answer = correct_answer

class QuizbowlGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Quizbowl")

        self.categories = ["Marketing", "Accounting", "Coding", "Database Management"]
        self.selected_category = tk.StringVar()
        self.selected_answer = tk.StringVar()

        self.create_category_selection_window()

    def create_category_selection_window(self):
        self.category_selection_frame = tk.Frame(self.master)
        self.category_selection_frame.pack()

        tk.Label(self.category_selection_frame, text="Select a category:").pack()

        for category in self.categories:
            tk.Radiobutton(self.category_selection_frame, text=category, variable=self.selected_category, value=category).pack()

        tk.Button(self.category_selection_frame, text="Start Quiz Now", command=self.start_quiz).pack()

    def start_quiz(self):
        selected_category = self.selected_category.get()
        self.category_selection_frame.destroy()
        self.create_quiz_window(selected_category)

    def create_quiz_window(self, category):
        self.quiz_frame = tk.Frame(self.master)
        self.quiz_frame.pack()

        tk.Label(self.quiz_frame, text=f"Category: {category}").pack()

        self.questions = self.get_questions_from_database(category)

        self.current_question_index = 0
        self.display_question()

    def get_questions_from_database(self, category):
        conn = sqlite3.connect('quiz.db')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
                            id INTEGER PRIMARY KEY,
                            category TEXT,
                            prompt TEXT,
                            option1 TEXT,
                            option2 TEXT,
                            option3 TEXT,
                            option4 TEXT,
                            correct_answer TEXT)''')

        # Generate new questions based on category
        questions = self.generate_questions(category)

        # Insert questions into the database
        for question in questions:
            cursor.execute("INSERT INTO questions (category, prompt, option1, option2, option3, option4, correct_answer) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (category, question.prompt, *question.options, question.correct_answer))

        conn.commit()

        # Retrieve questions from the database for the selected category
        cursor.execute("SELECT prompt, option1, option2, option3, option4, correct_answer FROM questions WHERE category=?", (category,))
        questions_from_db = []
        for row in cursor.fetchall():
            prompt, option1, option2, option3, option4, correct_answer = row
            options = [option1, option2, option3, option4]
            questions_from_db.append(Question(prompt, options, correct_answer))

        conn.close()

        return questions_from_db

    def generate_questions(self, category):
        if category == "Marketing":
            questions = [
                Question("What is the 4P's marketing mix consists of?", ["A. Product, Price, Promotion, Place", "B. Price, Promotion, People, Process", "C. Product, Process, People, Physical Evidence", "D. Price, Product, Physical Evidence, People"], "A"),
                Question("Which marketing strategy focuses on selling more of the current product to the existing customer base?", ["A. Market Penetration", "B. Market Development", "C. Product Development", "D. Diversification"], "A"),
                Question("What does ROI stand for in marketing?", ["A. Return On Investment", "B. Rate Of Interest", "C. Return Of Income", "D. Risk Of Investment"], "A"),
                Question("What is the difference between marketing and advertising?", ["A. Marketing involves creating and promoting a product or service, while advertising is only the promotion aspect", "B. Advertising involves creating and promoting a product or service, while marketing is only the promotion aspect", "C. There is no difference", "D. Advertising focuses on pricing strategies, while marketing focuses on distribution strategies"], "A"),
                Question("What is a SWOT analysis in marketing?", ["A. An analysis of a company's strengths, weaknesses, opportunities, and threats", "B. An analysis of a company's sales, wages, objectives, and taxes", "C. An analysis of a company's shareholders, workers, organization, and technology", "D. An analysis of a company's social media, website, online ads, and television commercials"], "A"),
                Question("What is a target market in marketing?", ["A. A specific group of customers that a company aims to reach with its products or services", "B. A market where products are bought and sold electronically", "C. A market that is targeted for growth by a company", "D. A market where a company sells its products at a discount"], "A"),
                Question("What is a marketing plan?", ["A. A comprehensive document that outlines a company's advertising and promotional efforts", "B. A plan that focuses solely on pricing strategies", "C. A plan that focuses solely on product development", "D. A plan that outlines a company's financial goals"], "A"),
                Question("What is market segmentation?", ["A. Dividing a market into distinct groups of buyers with different needs, characteristics, or behaviors", "B. Merging two or more markets to increase market share", "C. Marketing a product in multiple markets simultaneously", "D. Analyzing market trends and predictions"], "A"),
                Question("What is brand positioning?", ["A. The way a brand is perceived in relation to its competitors", "B. The physical location of a brand's headquarters", "C. The process of creating a new brand", "D. The price of a brand's products"], "A"),
                Question("What is a call to action (CTA) in marketing?", ["A. A prompt that encourages the audience to take a specific action", "B. A report on the effectiveness of a marketing campaign", "C. A meeting between marketing executives", "D. A legal document outlining marketing strategies"], "A")
            ]
        elif category == "Accounting":
            questions = [
                Question("Which financial statement presents a company's revenues and expenses?", ["A. Income statement", "B. Balance sheet", "C. Cash flow statement", "D. Statement of retained earnings"], "A"),
                Question("What accounting principle requires that expenses are recorded when they are incurred, regardless of when cash is paid?", ["A. Matching principle", "B. Revenue recognition principle", "C. Conservatism principle", "D. Accrual principle"], "D"),
                Question("Which accounting equation is expressed as Assets = Liabilities + Equity?", ["A. Balance sheet equation", "B. Income statement equation", "C. Cash flow equation", "D. Retained earnings equation"], "A"),
                Question("What is the purpose of depreciation in accounting?", ["A. To reduce the value of assets on the balance sheet", "B. To increase the value of assets on the balance sheet", "C. To record the sale of assets", "D. To record the increase in value of assets over time"], "A"),
                Question("What is GAAP in accounting?", ["A. Generally Accepted Accounting Principles", "B. General Accounting Assessment Process", "C. Global Accounting and Audit Protocol", "D. General Accounting Accreditation Program"], "A"),
                Question("What is the difference between accrual and cash accounting?", ["A. Accrual accounting records transactions when they occur, regardless of when cash is exchanged, while cash accounting only records transactions when cash is exchanged", "B. Cash accounting records transactions when they occur, regardless of when cash is exchanged, while accrual accounting only records transactions when cash is exchanged", "C. There is no difference", "D. Cash accounting is used by large corporations, while accrual accounting is used by small businesses"], "A"),
                Question("What is a balance sheet in accounting?", ["A. A financial statement that shows a company's revenues and expenses over a period of time", "B. A financial statement that shows a company's assets, liabilities, and equity at a specific point in time", "C. A financial statement that shows a company's cash inflows and outflows", "D. A financial statement that shows a company's retained earnings"], "B"),
                Question("What is the accounting equation?", ["A. Assets = Liabilities + Equity", "B. Assets = Liabilities - Equity", "C. Assets = Liabilities * Equity", "D. Assets = Liabilities / Equity"], "A"),
                Question("What is the purpose of a trial balance?", ["A. To ensure that debits equal credits in the accounting records", "B. To calculate the net income of a company", "C. To prepare financial statements", "D. To record adjusting entries"], "A"),
                Question("What is the difference between a debit and a credit in accounting?", ["A. Debits increase asset and expense accounts, while credits increase liability and equity accounts", "B. Debits increase liability and equity accounts, while credits increase asset and expense accounts", "C. Debits decrease asset and expense accounts, while credits decrease liability and equity accounts", "D. Debits decrease liability and equity accounts, while credits decrease asset and expense accounts"], "A")
            ]
        elif category == "Coding":
            questions = [
                Question("What does HTML stand for?", ["A. Hyper Text Markup Language", "B. High Tech Modern Language", "C. Home Tool Markup Language", "D. Hyperlinks and Text Markup Language"], "A"),
                Question("Which of the following is a programming language?", ["A. Python", "B. MySQL", "C. HTML", "D. CSS"], "A"),
                Question("What is the purpose of the 'if' statement in programming?", ["A. To loop through a list", "B. To define a function", "C. To make a decision based on a condition", "D. To print output to the screen"], "C"),
                Question("What does IDE stand for in programming?", ["A. Integrated Development Environment", "B. Internet Development Environment", "C. Interactive Development Environment", "D. Intelligent Design Environment"], "A"),
                Question("What is a variable in programming?", ["A. A value that cannot be changed", "B. A container for storing data values", "C. A loop that repeats a specific block of code", "D. A function that returns a value"], "B"),
                Question("What does HTTP stand for?", ["A. Hyper Text Transfer Protocol", "B. Home Tool Transfer Protocol", "C. High Tech Transfer Protocol", "D. Hyperlinks and Text Transfer Protocol"], "A"),
                Question("What is the purpose of comments in programming?", ["A. To make the code run faster", "B. To explain the code to other programmers", "C. To create visual effects in the code", "D. To mark the end of a line of code"], "B"),
                Question("What is object-oriented programming?", ["A. A programming paradigm based on objects and classes", "B. A programming language that uses only objects", "C. A programming technique that focuses on data types", "D. A programming concept that excludes functions"], "A"),
                Question("What is the difference between a list and a tuple in Python?", ["A. Lists are mutable, while tuples are immutable", "B. Tuples are mutable, while lists are immutable", "C. Lists and tuples are the same thing", "D. Lists and tuples cannot contain different data types"], "A"),
                Question("What is a function in programming?", ["A. A block of code that performs a specific task", "B. A variable that stores a value", "C. A condition that controls the flow of execution", "D. A statement that ends a loop"], "A")
            ]
        elif category == "Database Management":
            questions = [
                Question("What is a primary key in a database?", ["A. A unique identifier for each row in a table", "B. A key that allows access to a database", "C. A key used for encrypting data", "D. A key used to link tables in a database"], "A"),
                Question("What is SQL used for?", ["A. To create and manage databases", "B. To create and manage user interfaces", "C. To design web pages", "D. To write server-side scripts"], "A"),
                Question("Which of the following is not a type of database?", ["A. Relational database", "B. NoSQL database", "C. Object-oriented database", "D. Python database"], "D"),
                Question("What is the purpose of a foreign key in a database?", ["A. To ensure data integrity by enforcing referential integrity constraints", "B. To encrypt sensitive data", "C. To store primary keys from another table", "D. To create indexes for faster data retrieval"], "A"),
                Question("What is normalization in database design?", ["A. The process of organizing data to minimize redundancy", "B. The process of encrypting sensitive data", "C. The process of optimizing queries for faster performance", "D. The process of creating relationships between tables"], "A"),
                Question("What is the difference between a database and a database management system (DBMS)?", ["A. A database is a collection of related data, while a DBMS is software used to manage databases", "B. A database is software used to manage data, while a DBMS is a collection of related data", "C. There is no difference", "D. A database is used to store data, while a DBMS is used to analyze data"], "A"),
                Question("What is the purpose of indexes in a database?", ["A. To speed up data retrieval", "B. To encrypt data", "C. To enforce data integrity", "D. To store primary keys"], "A"),
                Question("What is a join in SQL?", ["A. A query that combines rows from two or more tables", "B. A query that retrieves data from a single table", "C. A query that updates data in a table", "D. A query that deletes data from a table"], "A"),
                Question("What is the difference between a clustered and non-clustered index?", ["A. A clustered index defines the physical order of data in a table, while a non-clustered index does not", "B. A clustered index is created by default on the primary key, while a non-clustered index is not", "C. There is no difference", "D. A clustered index is faster than a non-clustered index"], "A"),
                Question("What is ACID in database management?", ["A. A set of properties that guarantee database transactions are processed reliably", "B. A programming language for querying databases", "C. A data modeling technique", "D. A database management system"], "A")
            ]
        else:
            questions = []  # Handle unknown category

        return questions

    def display_question(self):
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]

            self.question_frame = tk.Frame(self.quiz_frame)
            self.question_frame.pack(pady=10)

            tk.Label(self.question_frame, text=question.prompt).pack()

            for option in question.options:
                tk.Radiobutton(self.question_frame, text=option, variable=self.selected_answer, value=option).pack()

            tk.Button(self.question_frame, text="Next", command=self.check_answer).pack(pady=5)
        else:
            messagebox.showinfo("Quiz Completed", "You have completed the quiz!")
    def check_answer(self):
        selected_answer = self.selected_answer.get()
        correct_answer_index = ord(self.questions[self.current_question_index].correct_answer) - ord('A')
        correct_answer = self.questions[self.current_question_index].options[correct_answer_index]

        if selected_answer == correct_answer:
            messagebox.showinfo("Correct", "Your answer is correct!")
        else:
            messagebox.showerror("Incorrect", f"Your answer is incorrect. Correct answer is {correct_answer}")

        self.current_question_index += 1
        self.question_frame.destroy()
        self.display_question()

    

root = tk.Tk()
app = QuizbowlGUI(root)
root.mainloop()

                





