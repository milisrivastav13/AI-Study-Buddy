# 📚 AI-Powered Study Buddy

An AI-powered learning companion built with **Python, Streamlit, and the Groq API** to help students understand concepts, summarize notes, practise questions, revise important topics, and organize their studies in one place.

AI Study Buddy combines AI-generated learning assistance with interactive revision tools, account registration and login, and text analytics in a responsive dark-themed interface.

🔗 **GitHub Repository:** https://github.com/milisrivastav13/AI-Study-Buddy

## ✨ Features

### 🔐 1. User Registration and Login
- Create an account using a username, email address, and password.
- Log in using a registered username or email address.
- Validate usernames, email addresses, and password requirements.
- Store account details in a local SQLite database.
- Hash passwords using PBKDF2-HMAC-SHA256 with individual random salts.
- Log out and clear the current session's learning state.

### 📊 2. Student Dashboard
- View a central dashboard for accessing study tools.
- Navigate between learning features using the sidebar.
- Use a clean, responsive dark-themed interface.
- Access tools for explanations, revision, AI assistance, and analytics.

### 📘 3. Explain Topic
- Enter an academic or technical topic.
- Receive student-friendly explanations generated through the Groq API.
- Request definitions, important points, and examples.
- Download generated responses as text files.

### 📝 4. Summarize Notes
- Paste study material into the application.
- Choose a concise, balanced, or detailed summary style.
- Generate AI-assisted summaries while preserving important facts and definitions.
- Compare the original and summarized word counts.
- Use a local rule-based summary fallback when needed.

### 🧠 5. Generate Quiz
- Generate quick revision questions from pasted study material.
- Choose between 1 and 10 questions.
- Enter your own answers.
- Reveal answers interactively to support self-assessment.
- Use a lightweight local question-generation method.

### 🎯 6. AI Quiz Generator
- Generate multiple-choice questions from study notes.
- Select the number of questions.
- Choose Easy, Medium, or Hard difficulty.
- Request four answer options, correct answers, and explanations.
- Use AI prompts designed to keep questions relevant to the supplied notes.

### 🃏 7. Generate Flashcards
- Convert study material into interactive flashcards.
- Choose how many cards to generate.
- Reveal the reverse side using the Flip Card button.
- Support active recall and quick revision through a local sentence-based method.

### 💬 8. Ask AI
- Ask academic questions in a chat-style interface.
- Receive AI-generated explanations and study assistance.
- Maintain conversation history during the current application session.
- Clear the chat when starting a new topic.
- Download individual generated responses.

### ✨ 9. Notes Simplifier
- Rewrite complex notes in simpler language.
- Choose from beginner-friendly explanations, bullet points, step-by-step explanations, and analogies.
- Preserve technical terms while making their meanings easier to understand.

### 📅 10. Study Plan Generator
- Create a study schedule for a subject or examination.
- Specify your learning goal and preparation period.
- Choose your current knowledge level.
- Set daily study hours.
- Generate a structured plan containing topics, practice, breaks, and revision.

### 💻 11. Code Explainer
- Submit code written in Python, C, C++, Java, JavaScript, SQL, or another language.
- Request beginner-friendly, line-by-line explanations.
- Ask for likely bugs and possible fixes.
- Understand execution flow and likely output.
- Request algorithm explanations and time-complexity analysis.

### 📈 12. Study Analytics
- Analyse pasted study material.
- Calculate word, sentence, character, and paragraph counts.
- Display text statistics using Streamlit metrics.
- Visualize the results with an interactive Plotly bar chart.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web interface and interactive components |
| Groq API | AI-generated explanations and study assistance |
| Groq Python SDK | Communication with the Groq API |
| SQLite | Local account database |
| hashlib | Password hashing |
| secrets | Cryptographically secure salt generation |
| hmac | Constant-time password-hash comparison |
| Pandas | Organizing analytics data |
| Plotly Express | Interactive charts and data visualization |
| Regular Expressions | Input validation and text processing |
| Git and GitHub | Version control and source-code hosting |
| Streamlit Community Cloud | Potential hosting and deployment platform |

## 🏗️ Project Architecture

The application follows a Python-based Streamlit architecture.

1. **User Interface:** Streamlit displays the dashboard, forms, navigation, study tools, and analytics.
2. **Authentication:** Registration and login functions validate credentials and interact with SQLite.
3. **AI Service Layer:** The Groq client sends prompts to the configured language model and returns generated responses.
4. **Local Processing:** Python functions generate basic summaries, quick quizzes, and flashcards without requiring an AI request.
5. **Analytics Layer:** Pandas prepares text statistics, and Plotly Express displays the results.
6. **Session Management:** Streamlit session state stores the current user's login state, chat history, quiz questions, and flashcards during the session.

## 📂 Project Structure

The main application code shared for this version is organized as follows:

```text
AI-Study-Buddy/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── .gitignore             # Files excluded from Git
└── .streamlit/
    └── secrets.toml       # Local secrets; do not commit
```


## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or a compatible version supported by your dependencies.
- Git.
- An internet connection for Groq-powered features.
- A Groq API key for AI-powered features.

### Step 1: Clone the repository

```bash
git clone https://github.com/milisrivastav13/AI-Study-Buddy.git
cd AI-Study-Buddy
```

### Step 2: Create a virtual environment (recommended)

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If the Groq SDK is missing from your dependency file, install it using:

```bash
pip install groq
```

Make sure `groq` is included in `requirements.txt` so the application can install it automatically in a fresh environment.

### Step 4: Configure the Groq API key

Create a file named `.streamlit/secrets.toml` in the project directory:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
GROQ_MODEL = "openai/gpt-oss-120b"
```

Replace the placeholder with your own valid API key. Never publish your real API key on GitHub.

Alternatively, configure `GROQ_API_KEY` and, optionally, `GROQ_MODEL` as environment variables.

The application uses `openai/gpt-oss-120b` as its default model when `GROQ_MODEL` is not configured. The model must be available to your Groq account.

### Step 5: Run the application

```bash
python -m streamlit run app.py
```

Streamlit will display a local URL, usually:

```text
http://localhost:8501
```

Open that address in your browser, register an account, and log in to explore the application.

## ☁️ Deployment

The application can be prepared for deployment on Streamlit Community Cloud.

1. Push the application source code to GitHub.
2. Open Streamlit Community Cloud and connect your GitHub account.
3. Select the `AI-Study-Buddy` repository and the `app.py` entry point.
4. Add `GROQ_API_KEY` and, if needed, `GROQ_MODEL` in the app's Secrets settings.
5. Deploy the application and test the AI features.

**Important deployment considerations:**

- SQLite data stored on an ephemeral hosting filesystem may not persist reliably across restarts or redeployments.
- Use a managed database with persistent storage for a production multi-user application.
- Keep API credentials in deployment secrets, never in source code.
- Confirm that the configured model is available before deployment.
- Test account creation, login, logout, AI requests, and interactive tools after deployment.

## 🔒 Security and Privacy

- Passwords are hashed instead of being stored as plain text.
- Random salts are generated for password hashing.
- Parameterized SQL statements are used for database queries.
- Password-hash comparison uses `hmac.compare_digest`.
- API credentials are read from Streamlit secrets or environment variables.
- Account storage currently uses a local SQLite database.
- Chat history and generated learning content are held in Streamlit session state rather than saved as a permanent learning record.

Do not use this educational implementation as a production authentication system without further security review, persistent storage, and appropriate deployment safeguards.

## 🎓 Use Cases

- Preparing for university examinations.
- Understanding computer science and technical concepts.
- Summarizing lengthy study notes.
- Creating revision questions and multiple-choice quizzes.
- Practising active recall using flashcards.
- Simplifying difficult textbook material.
- Planning daily study schedules.
- Understanding code and debugging concepts.
- Analysing the structure and length of study notes.

## ⚠️ Limitations

- AI responses depend on the configured model, API availability, rate limits, and network connectivity.
- AI-generated content may contain errors and should be verified against reliable study material.
- The quick quiz and flashcard generators use sentence-based rules rather than advanced semantic extraction.
- Session-based chat and learning content are not automatically stored as permanent user history.
- Local SQLite storage is not a substitute for a managed, persistent production database.
- The application does not claim that submitted code has been executed when explaining it.

## 🚀 Future Enhancements

- Upload and process PDF or DOCX study material.
- Save notes, quizzes, and flashcards to a persistent database.
- Track quiz scores and learning progress over time.
- Add personalized recommendations based on learning activity.
- Support multiple languages.
- Add export options for summaries, quizzes, and study plans.
- Introduce automated tests and improved error handling.
- Improve authentication, account recovery, and database management.

## 👩‍💻 Developer

**Mili Srivastava**  
B.Tech — Computer Science and Engineering (AI & Machine Learning)  
Buddha Institute of Technology, Gorakhpur  

**Training Programme:** IBM SkillsBuild × Edunet Foundation Internship

## 📜 Disclaimer

AI Study Buddy is an educational project developed for learning and internship purposes. It is not an official IBM or Edunet Foundation product. Third-party software, APIs, and libraries remain subject to their respective licenses and terms.

## 📄 License

No specific open-source license is stated here. Unless a license file is added to the repository, reuse and redistribution are subject to the applicable copyright rules.

---

**Made with ❤️ using Python, Streamlit, and Groq API.**
