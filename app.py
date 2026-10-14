
import os
import re
import sqlite3
import hashlib
import hmac
import secrets
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

try:
    from groq import Groq
except ImportError:
    Groq = None


# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR / "users.db"
DEFAULT_MODEL = "openai/gpt-oss-120b"


# =========================================================
# DATABASE AND AUTHENTICATION
# =========================================================
def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE COLLATE NOCASE,
            email TEXT NOT NULL UNIQUE COLLATE NOCASE,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT ''
        )
    """)

    columns = {
        row[1]
        for row in conn.execute("PRAGMA table_info(users)").fetchall()
    }

    if "created_at" not in columns:
        conn.execute(
            "ALTER TABLE users ADD COLUMN created_at TEXT NOT NULL DEFAULT ''"
        )

    conn.commit()
    return conn


def hash_password(password, salt_hex=None):
    salt = bytes.fromhex(salt_hex) if salt_hex else secrets.token_bytes(16)

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        310_000,
    )

    return digest.hex(), salt.hex()


def register_user(username, email, password):
    username = username.strip()
    email = email.strip().lower()

    if not re.fullmatch(r"[A-Za-z0-9_.-]{3,24}", username):
        return False, (
            "Username must be 3–24 characters and may contain "
            "letters, numbers, dots, underscores and hyphens."
        )

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return False, "Please enter a valid email address."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
        return False, "Password must contain at least one letter and one number."

    password_hash, salt = hash_password(password)

    try:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO users
                (username, email, password_hash, salt, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    username,
                    email,
                    password_hash,
                    salt,
                    datetime.now().isoformat(timespec="seconds"),
                ),
            )

        return True, "Registration successful! You can now log in."

    except sqlite3.IntegrityError:
        return False, "This username or email is already registered."


def authenticate_user(identity, password):
    identity = identity.strip()

    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, username, email, password_hash, salt
            FROM users
            WHERE username = ? COLLATE NOCASE
               OR email = ? COLLATE NOCASE
            """,
            (identity, identity),
        ).fetchone()

    if not row:
        return None

    user_id, username, email, saved_hash, salt = row
    candidate_hash, _ = hash_password(password, salt)

    if hmac.compare_digest(candidate_hash, saved_hash):
        return {
            "id": user_id,
            "username": username,
            "email": email,
        }

    return None


# =========================================================
# DARK THEME ONLY
# =========================================================
def apply_theme(theme="Dark"):
    st.markdown(
        """
        <style>
        :root {
            color-scheme: dark;
        }

        html, body, [class*="css"] {
            font-family: Inter, "Segoe UI", Arial, sans-serif;
        }

        .stApp,
        [data-testid="stAppViewContainer"] {
            background: #0B1220;
            color: #F3F6FC;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stMainBlockContainer"] {
            width: 100%;
            max-width: 1180px;
            padding: 1.5rem clamp(0.8rem, 4vw, 3rem) 2.5rem;
        }

        [data-testid="stSidebar"] {
            background: #111C2F;
            border-right: 1px solid #33445F;
        }

        [data-testid="stSidebar"] * {
            color: #F3F6FC;
        }

        h1, h2, h3, h4, h5, h6,
        p, li, label, legend,
        [data-testid="stMarkdownContainer"] {
            color: #F3F6FC;
        }

        [data-testid="stCaptionContainer"] {
            color: #B8C5D9;
        }

        h1 {
            font-size: clamp(1.55rem, 3vw, 2.35rem);
            line-height: 1.25;
        }

        h2 {
            font-size: clamp(1.3rem, 2.5vw, 1.8rem);
        }

        .hero {
            background: linear-gradient(135deg, #111C2F, #162338);
            border: 1px solid #33445F;
            border-radius: 20px;
            padding: clamp(1.1rem, 3vw, 2rem);
            margin-bottom: 1.25rem;
            overflow-wrap: anywhere;
        }

        .hero h1 {
            color: #F3F6FC !important;
            margin-top: 0;
        }

        .hero p {
            color: #B8C5D9 !important;
            line-height: 1.6;
        }

        [data-testid="stForm"] {
            background: #111C2F;
            border: 1px solid #33445F;
            border-radius: 16px;
            padding: clamp(12px, 3vw, 24px);
        }

        [data-testid="stTextInput"] label,
        [data-testid="stTextArea"] label,
        [data-testid="stSelectbox"] label,
        [data-testid="stRadio"] label,
        [data-testid="stCheckbox"] label,
        [data-testid="stSlider"] label {
            color: #F3F6FC !important;
            font-weight: 600;
        }

        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input,
        .stDateInput input,
        [data-baseweb="select"] > div {
            background: #18263B !important;
            color: #F3F6FC !important;
            border: 1px solid #33445F !important;
            border-radius: 10px !important;
            min-height: 2.7rem;
        }

        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: #B8C5D9 !important;
        }

        [data-baseweb="select"] *,
        [data-baseweb="popover"] *,
        [role="listbox"] *,
        [role="option"] {
            color: #F3F6FC !important;
        }

        [data-baseweb="popover"],
        [data-baseweb="menu"] {
            background: #111C2F !important;
        }

        div.stButton > button,
        div.stFormSubmitButton > button,
        [data-testid="stDownloadButton"] button {
            background: #FF4B4B;
            color: #FFFFFF !important;
            border: 1px solid #FF4B4B;
            border-radius: 10px;
            min-height: 2.7rem;
            font-weight: 650;
        }

        div.stButton > button:hover,
        div.stFormSubmitButton > button:hover,
        [data-testid="stDownloadButton"] button:hover {
            background: #E43F3F;
            color: #FFFFFF !important;
            border-color: #E43F3F;
        }

        div.stButton > button p,
        div.stFormSubmitButton > button p {
            color: #FFFFFF !important;
        }

        [data-testid="stMetric"] {
            background: #162338;
            border: 1px solid #33445F;
            border-radius: 14px;
            padding: 1rem;
        }

        [data-testid="stMetricLabel"],
        [data-testid="stMetricValue"] {
            color: #F3F6FC !important;
        }

        [data-testid="stExpander"] {
            background: #111C2F;
            border: 1px solid #33445F;
            border-radius: 12px;
        }

        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary p {
            color: #F3F6FC !important;
        }

        [data-testid="stAlert"] {
            border-radius: 12px;
        }

        [data-testid="stTabs"] button[role="tab"] {
            color: #B8C5D9 !important;
        }

        [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
            color: #A9B5FF !important;
        }

        hr {
            border-color: #33445F;
        }

        a {
            color: #A9B5FF;
        }

        @media (max-width: 768px) {
            [data-testid="stMainBlockContainer"] {
                padding: 1rem 0.8rem 2rem;
            }

            .hero {
                padding: 1rem;
                border-radius: 15px;
            }

            .hero h1 {
                font-size: 1.55rem;
            }

            div.stButton > button,
            div.stFormSubmitButton > button {
                width: 100%;
            }
        }

        @media (max-width: 480px) {
            [data-testid="stMainBlockContainer"] {
                padding-left: 0.6rem;
                padding-right: 0.6rem;
            }

            .hero h1 {
                font-size: 1.35rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# GROQ AI HELPERS
# =========================================================
def read_secret(name, default=None):
    try:
        value = st.secrets.get(name, default)
        if value:
            return value
    except Exception:
        pass

    return os.getenv(name, default)


def get_groq_client():
    api_key = read_secret("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "Groq API key not found. Add GROQ_API_KEY to "
            ".streamlit/secrets.toml or environment variables."
        )

    if Groq is None:
        raise RuntimeError("Groq package missing. Run: pip install groq")

    return Groq(api_key=api_key)


def ask_groq(system_prompt, user_prompt, max_tokens=1600, temperature=0.4):
    client = get_groq_client()
    model = read_secret("GROQ_MODEL", DEFAULT_MODEL)

    request_args = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_completion_tokens": max_tokens,
    }

    if not model.startswith("openai/gpt-oss"):
        request_args["temperature"] = temperature

    response = client.chat.completions.create(**request_args)
    answer = response.choices[0].message.content

    if not answer:
        raise RuntimeError("The AI returned an empty response. Please try again.")

    return answer.strip()


def show_ai_result(system_prompt, user_prompt, max_tokens=1600, temperature=0.4):
    try:
        with st.spinner("Groq AI is working..."):
            result = ask_groq(
                system_prompt,
                user_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
            )

        st.markdown(result)

        st.download_button(
            "⬇️ Download response",
            data=result,
            file_name="ai_study_buddy_response.txt",
            mime="text/plain",
        )

        return result

    except Exception as exc:
        st.error(f"AI request failed: {exc}")
        st.caption(
            "Check your API key, selected model, internet connection "
            "and Groq usage limits."
        )
        return None


# =========================================================
# LOCAL FALLBACK HELPERS
# =========================================================
def quick_summary(text, sentence_limit=3):
    sentences = [
        part.strip()
        for part in re.split(r"(?<=[.!?])\s+", text.strip())
        if part.strip()
    ]

    if not sentences:
        return "No text was provided."

    if len(sentences) <= sentence_limit:
        return " ".join(sentences)

    return " ".join(sentences[:sentence_limit])


def local_quiz(text, count=5):
    sentences = [
        part.strip()
        for part in re.split(r"(?<=[.!?])\s+", text.strip())
        if len(part.split()) >= 5
    ]

    questions = []

    for sentence in sentences[:count]:
        words = sentence.split()
        start = " ".join(words[:5])

        questions.append({
            "question": f"Complete or explain this statement: {start} ...",
            "answer": sentence,
        })

    return questions


def local_flashcards(text, count=10):
    sentences = [
        part.strip()
        for part in re.split(r"(?<=[.!?])\s+", text.strip())
        if len(part.split()) >= 4
    ]

    cards = []

    for sentence in sentences[:count]:
        words = sentence.split()

        cards.append({
            "front": " ".join(words[:3]),
            "back": " ".join(words[3:]) or sentence,
        })

    return cards


# =========================================================
# AUTHENTICATION PAGE
# =========================================================
def authentication_page():
    st.markdown(
        """
        <div class="hero">
            <h1>📚 AI Study Buddy</h1>
            <p>Your personal learning companion — understand, practise and revise smarter.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    register_tab, login_tab = st.tabs(["✨ Register", "🔐 Login"])

    with register_tab:
        st.subheader("Create your account")

        with st.form("register_form"):
            username = st.text_input(
                "Username",
                placeholder="e.g. mili_studies",
            )

            email = st.text_input(
                "Email address",
                placeholder="you@example.com",
            )

            password = st.text_input(
                "Password",
                type="password",
                help="At least 8 characters, including a letter and a number.",
            )

            confirm_password = st.text_input(
                "Confirm password",
                type="password",
            )

            register_clicked = st.form_submit_button(
                "Create account",
                use_container_width=True,
            )

        if register_clicked:
            if password != confirm_password:
                st.error("Passwords do not match.")
            else:
                ok, message = register_user(username, email, password)
                if ok:
                    st.success(message)
                else:
                    st.error(message)

    with login_tab:
        st.subheader("Welcome back")

        with st.form("login_form"):
            identity = st.text_input("Username or email")
            login_password = st.text_input("Password", type="password")

            login_clicked = st.form_submit_button(
                "Login",
                use_container_width=True,
            )

        if login_clicked:
            user = authenticate_user(identity, login_password)

            if user:
                st.session_state.user = user
                st.session_state.chat_history = []
                st.rerun()
            else:
                st.error("Login failed. Check your credentials or register first.")

    st.caption(
        "Accounts are stored in a local SQLite database. "
        "For multi-user cloud deployment, use a persistent managed database."
    )


# =========================================================
# SESSION STATE
# =========================================================
if "user" not in st.session_state:
    st.session_state.user = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []

if "flashcards" not in st.session_state:
    st.session_state.flashcards = []

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

st.session_state.theme = "Dark"


# =========================================================
# LOGIN GATE
# =========================================================
apply_theme("Dark")

if not st.session_state.user:
    with st.sidebar:
        st.markdown("### 🌙 Dark Mode")
        st.caption("Dark theme is enabled.")

        st.markdown("---")
        st.markdown("### 👩‍💻 Developer")
        st.markdown("**Mili Srivastava**")
        st.caption("B.Tech CSE (AI & Machine Learning)")
        st.caption("Buddha Institute of Technology, Gorakhpur")

        st.markdown("---")
        st.markdown("### 🏢 Training Organization")
        st.markdown("IBM SkillsBuild × Edunet Foundation")

        st.markdown("---")
        st.caption("Educational project developed during industrial training.")
        st.caption("© 2026 Mili Srivastava")

    authentication_page()
    st.stop()


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================
with st.sidebar:
    st.title("📚 AI Study Buddy")
    st.markdown("---")

    st.write(f"Welcome, **{st.session_state.user['username']}**!")

    st.markdown("### 🌙 Dark Mode")
    st.caption("Dark theme is enabled.")

    st.markdown("---")

    mode = st.radio(
        "YOUR WORKSPACE",
        [
            "Dashboard",
            "Explain Topic",
            "Summarize Notes",
            "Generate Quiz",
            "Generate Flashcards",
            "Ask AI",
            "AI Quiz Generator",
            "Notes Simplifier",
            "Study Plan Generator",
            "Code Explainer",
            "Study Analytics",
        ],
    )

    st.markdown("---")

    st.markdown("### 👩‍💻 Developer")
    st.markdown("**Mili Srivastava**")
    st.caption("B.Tech CSE (AI & ML)")
    st.caption("Buddha Institute of Technology, Gorakhpur")

    st.markdown("---")

    st.markdown("### 🏢 Organization")
    st.markdown("**IBM SkillsBuild × Edunet Foundation**")
    st.caption("Industrial Training Project")

    st.markdown("---")

    st.markdown("### © Rights & Disclaimer")
    st.caption(
        "AI Study Buddy is an educational project developed as part "
        "of industrial training."
    )
    st.caption(
        "Third-party libraries and components remain subject to "
        "their respective licenses. This is not an official IBM product."
    )
    st.caption("© 2026 Mili Srivastava")

    st.markdown("---")

    st.caption("Made with ❤️ using Python and Streamlit")

    if st.button("🚪 Log Out", use_container_width=True):
        st.session_state.user = None
        st.session_state.chat_history = []
        st.session_state.quiz_questions = []
        st.session_state.flashcards = []
        st.rerun()


# =========================================================
# APP HEADER
# =========================================================
st.markdown(
    """
    <div class="hero">
        <h1>📚 AI-Powered Study Buddy</h1>
        <p>
            Understand concepts, revise notes, practise questions
            and plan your learning in one place.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DASHBOARD
# =========================================================
if mode == "Dashboard":
    st.subheader(f"Welcome to your study space 👋")
    st.write("Choose a feature from the sidebar to get started.")

    c1, c2, c3 = st.columns(3)

    c1.metric("AI Study Tools", "10")
    c2.metric("Learning Style", "Personalized")
    c3.metric("Account Status", "Active")

    st.subheader("What would you like to do today?")

    dashboard_cards = [
        ("📘 Explain Topic", "Understand difficult concepts in simple language."),
        ("📝 Summarize Notes", "Turn long notes into revision material."),
        ("🧠 Generate Quiz", "Practise questions based on your notes."),
        ("🃏 Flashcards", "Revise definitions and important ideas."),
        ("💬 Ask AI", "Ask academic questions and get explanations."),
        ("📅 Study Plan", "Build a practical study schedule."),
    ]

    for start in range(0, len(dashboard_cards), 2):
        col1, col2 = st.columns(2)

        for col, item in zip(
            [col1, col2],
            dashboard_cards[start:start + 2],
        ):
            with col:
                with st.container(border=True):
                    st.markdown(f"### {item[0]}")
                    st.write(item[1])


# =========================================================
# EXPLAIN TOPIC
# =========================================================
elif mode == "Explain Topic":
    st.subheader("📘 Explain Topic")

    topic = st.text_input(
        "Enter a topic",
        placeholder="e.g. Deep Learning, IoT, Machine Learning",
    )

    if st.button("Explain Topic", type="primary"):
        if not topic.strip():
            st.warning("Please enter a topic first.")
        else:
            show_ai_result(
                "You are a computer science tutor. Explain concepts in "
                "clear student-friendly language. Include a definition, "
                "key points, and an example. Do not invent facts.",
                f"Explain this topic for an undergraduate student: {topic.strip()}",
                max_tokens=1800,
            )


# =========================================================
# SUMMARIZE NOTES
# =========================================================
elif mode == "Summarize Notes":
    st.subheader("📝 Summarize Notes")

    notes = st.text_area(
        "Paste your study notes",
        height=250,
        key="summary_notes",
    )

    style = st.selectbox(
        "Summary style",
        ["Concise", "Balanced", "Detailed"],
    )

    if st.button("Summarize Notes", type="primary"):
        if len(notes.strip()) < 20:
            st.warning("Please enter more text to summarize.")
        else:
            try:
                summary = show_ai_result(
                    "You are an academic note summarizer. Preserve important "
                    "facts and definitions. Do not add unsupported details. "
                    "Use headings and bullet points where useful.",
                    f"Create a {style.lower()} summary of these notes:\n\n{notes}",
                    max_tokens=2000,
                )

                if summary:
                    col1, col2 = st.columns(2)
                    col1.metric("Original words", len(notes.split()))
                    col2.metric("Summary words", len(summary.split()))

            except Exception:
                st.warning("AI summarization is unavailable.")
                st.markdown(quick_summary(notes))


# =========================================================
# GENERATE QUIZ — WITH WORKING REVEAL BUTTONS
# =========================================================
elif mode == "Generate Quiz":
    st.subheader("🧠 Quick Revision Quiz")

    quiz_text = st.text_area(
        "Paste your study material",
        height=230,
        placeholder="Paste your chapter or notes here...",
        key="quick_quiz_text",
    )

    question_count = st.slider(
        "Number of questions",
        min_value=1,
        max_value=10,
        value=5,
        key="quick_quiz_count",
    )

    if st.button("Create Quiz", type="primary"):
        if not quiz_text.strip():
            st.warning("Please enter your study material.")
        else:
            questions = local_quiz(quiz_text, question_count)

            if not questions:
                st.warning(
                    "Please enter a few complete sentences with enough detail."
                )
            else:
                st.session_state.quiz_questions = questions

                for i in range(len(questions)):
                    st.session_state[f"show_quiz_answer_{i}"] = False

    if st.session_state.quiz_questions:
        st.markdown("### Your Quiz")

        for index, item in enumerate(
            st.session_state.quiz_questions
        ):
            with st.container(border=True):
                st.markdown(
                    f"**Question {index + 1}:** {item['question']}"
                )

                st.text_input(
                    "Your answer (optional)",
                    key=f"quiz_user_answer_{index}",
                )

                if st.button(
                    "👁️ Reveal Answer",
                    key=f"reveal_quiz_answer_{index}",
                    use_container_width=True,
                ):
                    st.session_state[f"show_quiz_answer_{index}"] = True

                if st.session_state.get(
                    f"show_quiz_answer_{index}", False
                ):
                    st.success("Answer")
                    st.write(item["answer"])


# =========================================================
# GENERATE FLASHCARDS
# =========================================================
elif mode == "Generate Flashcards":
    st.subheader("🃏 Generate Flashcards")

    notes = st.text_area(
        "Paste your study notes",
        height=240,
        key="flashcard_notes",
    )

    count = st.slider("Number of flashcards", 1, 10, 5)

    if st.button("Generate Flashcards", type="primary"):
        if not notes.strip():
            st.warning("Please paste your notes first.")
        else:
            st.session_state.flashcards = local_flashcards(notes, count)

            for i in range(len(st.session_state.flashcards)):
                st.session_state[f"flip_card_{i}"] = False

    if st.session_state.flashcards:
        st.markdown("### Your Flashcards")

        for i, card in enumerate(st.session_state.flashcards):
            with st.container(border=True):
                st.markdown(f"**Flashcard {i + 1}**")
                st.markdown(f"### {card['front']}")

                if st.button(
                    "🔄 Flip Card",
                    key=f"flip_button_{i}",
                    use_container_width=True,
                ):
                    key = f"flip_card_{i}"
                    st.session_state[key] = not st.session_state.get(key, False)

                if st.session_state.get(f"flip_card_{i}", False):
                    st.info(card["back"])


# =========================================================
# ASK AI
# =========================================================
elif mode == "Ask AI":
    st.subheader("💬 Ask AI")
    st.write("Ask a question about a topic or concept.")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask your study question...")

    if prompt:
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt,
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            answer = show_ai_result(
                "You are AI Study Buddy, a helpful and honest study "
                "assistant. Explain clearly and use examples where useful.",
                prompt,
                max_tokens=1800,
            )

        if answer:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer,
            })

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()


# =========================================================
# AI QUIZ GENERATOR
# =========================================================
elif mode == "AI Quiz Generator":
    st.subheader("🎯 AI Quiz Generator")

    notes = st.text_area(
        "Paste your study material",
        height=240,
        key="ai_quiz_notes",
    )

    col1, col2 = st.columns(2)

    with col1:
        number_of_questions = st.slider(
            "Number of questions", 3, 10, 5
        )

    with col2:
        difficulty = st.selectbox(
            "Difficulty",
            ["Easy", "Medium", "Hard"],
        )

    if st.button("Generate AI Quiz", type="primary"):
        if len(notes.strip()) < 50:
            st.warning("Please paste more study material.")
        else:
            show_ai_result(
                "Create reliable multiple-choice questions strictly "
                "from the supplied notes. Provide four options A-D, "
                "the correct answer, and a short explanation. "
                "Do not test facts absent from the notes.",
                f"Create {number_of_questions} {difficulty.lower()}-level "
                f"MCQs from these notes. Include four options, answer, "
                f"and explanation for each question.\n\nNOTES:\n{notes}",
                max_tokens=3000,
                temperature=0.3,
            )


# =========================================================
# NOTES SIMPLIFIER
# =========================================================
elif mode == "Notes Simplifier":
    st.subheader("✨ Notes Simplifier")

    notes = st.text_area(
        "Paste difficult notes or textbook content",
        height=250,
    )

    style = st.selectbox(
        "Explanation style",
        [
            "Simple English for beginners",
            "Bullet points for quick revision",
            "Step-by-step explanation",
            "Explain using an analogy",
        ],
    )

    if st.button("Simplify Notes", type="primary"):
        if len(notes.strip()) < 20:
            st.warning("Please enter some notes first.")
        else:
            show_ai_result(
                "You are a learning coach. Rewrite study material "
                "in clear language without changing its meaning. "
                "Keep technical terms and define them.",
                f"Rewrite these notes using this style: {style}.\n\n{notes}",
                max_tokens=2000,
            )


# =========================================================
# STUDY PLAN GENERATOR
# =========================================================
elif mode == "Study Plan Generator":
    st.subheader("📅 Personalized AI Study Plan")

    with st.form("study_plan_form"):
        subject = st.text_input(
            "Subject or exam",
            placeholder="e.g. Deep Learning",
        )

        goal = st.text_input(
            "Your goal",
            placeholder="e.g. Understand concepts",
        )

        col1, col2 = st.columns(2)

        with col1:
            days = st.slider("Preparation period (days)", 1, 30, 7)
            hours = st.slider("Study hours per day", 0.5, 10.0, 2.0, 0.5)

        with col2:
            level = st.selectbox(
                "Current level",
                ["Beginner", "Some knowledge", "Revision"],
            )

        create_plan = st.form_submit_button(
            "Create Study Plan",
            type="primary",
        )

    if create_plan:
        if not subject.strip() or not goal.strip():
            st.warning("Please enter the subject and your goal.")
        else:
            show_ai_result(
                "You are a practical study-planning assistant. "
                "Create a day-by-day plan including learning, practice, "
                "breaks, and revision. Fit it to the available time.",
                f"Create a {days}-day study plan.\n"
                f"Subject: {subject}\nGoal: {goal}\n"
                f"Daily study time: {hours} hours\n"
                f"Current level: {level}\n"
                "Include daily topics, practice tasks, breaks and revision.",
                max_tokens=2600,
            )


# =========================================================
# CODE EXPLAINER
# =========================================================
elif mode == "Code Explainer":
    st.subheader("💻 Code Explainer")

    language = st.selectbox(
        "Programming language",
        ["Python", "C", "C++", "Java", "JavaScript", "SQL", "Other"],
    )

    focus = st.selectbox(
        "Explanation focus",
        [
            "Beginner-friendly line-by-line explanation",
            "Find likely bugs and explain fixes",
            "Explain algorithm and time complexity",
            "Explain output and execution flow",
        ],
    )

    code = st.text_area(
        "Paste your code",
        height=280,
        placeholder="Paste code here...",
    )

    if st.button("Explain Code", type="primary"):
        if not code.strip():
            st.warning("Please paste some code first.")
        else:
            show_ai_result(
                "You are a careful programming tutor. Explain code for "
                "a student. Do not claim that you executed the code. "
                "Point out likely bugs when visible.",
                f"Language: {language}\nFocus: {focus}\n"
                f"Explain the purpose, step-by-step flow, likely output "
                f"if determinable, and possible improvements.\n\nCODE:\n{code}",
                max_tokens=2600,
                temperature=0.2,
            )


# =========================================================
# STUDY ANALYTICS
# =========================================================
elif mode == "Study Analytics":
    st.subheader("📊 Study Analytics")

    text_to_analyse = st.text_area(
        "Paste notes to analyse",
        height=220,
        key="analytics_text",
    )

    if st.button("Analyse Text", type="primary"):
        if not text_to_analyse.strip():
            st.warning("Please paste some text first.")
        else:
            word_count = len(text_to_analyse.split())

            sentence_count = len([
                part
                for part in re.split(r"[.!?]+", text_to_analyse)
                if part.strip()
            ])

            character_count = len(text_to_analyse)

            paragraph_count = len([
                part
                for part in re.split(r"\n\s*\n", text_to_analyse.strip())
                if part.strip()
            ])

            c1, c2, c3, c4 = st.columns(4)

            c1.metric("Words", word_count)
            c2.metric("Sentences", sentence_count)
            c3.metric("Characters", character_count)
            c4.metric("Paragraphs", paragraph_count)

            analytics = pd.DataFrame({
                "Metric": [
                    "Words",
                    "Sentences",
                    "Characters",
                    "Paragraphs",
                ],
                "Value": [
                    word_count,
                    sentence_count,
                    character_count,
                    paragraph_count,
                ],
            })

            fig = px.bar(
                analytics,
                x="Metric",
                y="Value",
                text="Value",
                title="Study Text Overview",
                template="plotly_dark",
            )

            fig.update_layout(
                paper_bgcolor="#0B1220",
                plot_bgcolor="#0B1220",
                font_color="#F3F6FC",
            )

            st.plotly_chart(fig, use_container_width=True)


# =========================================================
# FOOTER
# =========================================================
st.markdown("---")

st.caption(
    "AI Study Buddy | Python | Streamlit | Groq API | "
    "Pandas | Plotly | SQLite"
)
