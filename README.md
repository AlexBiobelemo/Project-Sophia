# Sophia: The AI-Powered Developer's Command Center

Sophia is a personal, web-based knowledge base for developers, reimagined. It's an intelligent assistant designed to augment a developer's workflow by not only storing code snippets but also using the power of generative AI to generate, explain, and organize them on the fly.

---

## ✨ Key Features

This application was built with a focus on a rich user experience, a robust feature set, and professional development practices.

### Core Functionality
* **Secure User Authentication:** Full registration, login, and session management.
* **Complete Snippet CRUD:** Create, Read, Update, and Delete code snippets.
* **Collections & Folders:** Full CRUD functionality for grouping related snippets into organized collections.
* **Syntax Highlighting:** Beautiful and readable code rendering for dozens of languages via Prism.js.

### AI Co-Pilot (Powered by Google Gemini)
* **AI Snippet Generation:** Generate code from a natural language prompt.
* **AI Code Explanation:** Get a detailed, line-by-line explanation for any saved snippet.
* **AI Tag Suggestion:** Automatically analyze code to suggest relevant organizational tags.
* **AI-Powered Semantic Search:** An advanced search that understands the *meaning* of your query, not just keywords, powered by vector embeddings.

### Professional Polish & UX
* **Modern UI:** A clean, responsive interface built with Bootstrap 5.
* **Markdown Support:** Use rich text formatting (bold, lists, links) in snippet descriptions, rendered safely.
* **Modern Notifications:** Non-intrusive "toast" notifications for user actions.
* **Client-Side Enhancements:** Includes a one-click "Copy to Clipboard" for code, a "Save Explanation as Note" feature, and client-side code formatting with Prettier for web languages.
* **Scalability:** Snippet lists are paginated to ensure fast load times and a smooth experience with large amounts of data.
* **Robust Security:** The application is protected against common vulnerabilities like CSRF, SQL Injection, and XSS (via HTML sanitization). Object ownership is enforced on all relevant routes.
* **Automated Testing:** The project includes a foundational test suite using **PyTest** to ensure reliability and prevent regressions.

---

## 🛠️ Tech Stack

* **Backend:** Python with **Flask**
* **Database:** **SQLite** with **Flask-SQLAlchemy** and **Flask-Migrate**
* **Frontend:** **Bootstrap 5**, **Jinja2**
* **JavaScript Libraries:**
    * **Prism.js** for syntax highlighting
    * **Marked.js** for Markdown rendering
    * **DOMPurify** for XSS sanitization
    * **Prettier** for client-side code formatting
* **Forms & Auth:** **Flask-WTF** for secure forms (CSRF protection), **Flask-Login** for session management.
* **AI Integration:** **Google Gemini API** for generative features and embeddings.
* **Testing & Numerics:** **PyTest** for automated testing, **NumPy** for vector similarity calculations.

---

## 🚀 Setup and Installation

To run this project locally, follow these steps:

**1. Prerequisites**
* Python 3.7+
* Git

**2. Clone the Repository**
```bash
git clone https://github.com/AlexBiobelemo/Project-Sophia
cd CodeSnippetsManager # or your project folder name

3. Create and Activate Virtual Environment
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate

4. Install Dependencies
 * Ensure your requirements.txt is up to date with pip freeze > requirements.txt.
 * Install all packages:
<!-- end list -->
pip install -r requirements.txt

5. Set Up Environment Variables
 * Create a file named .env in the root directory.
 * Add your secret keys to this file. You must generate your own SECRET_KEY and get a GEMINI_API_KEY from Google AI Studio.
<!-- end list -->
# .env file

SECRET_KEY='a-very-long-and-random-secret-key'
GEMINI_API_KEY='your-google-gemini-api-key-here'

6. Initialize the Database
 * Run the database migration commands to create the app.db file and all tables.
<!-- end list -->
flask db init
flask db migrate -m "Initial database schema"
flask db upgrade

7. Run the Application
flask run

The application will be available at http://127.0.0.1:5000.
8. Running Tests
 * To run the automated test suite, execute the following command from the root directory:
<!-- end list -->
pytest


