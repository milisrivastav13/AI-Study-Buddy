import streamlit as st
import pandas as pd
import plotly.express as px

from explainer import explain_topic
from summarizer import summarize_notes
from quiz_generator import generate_quiz
from flashcards import generate_flashcards

st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="wide"
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.title("📚 AI Study Buddy")

    st.markdown("---")

    st.write("### Your Learning Buddy......")

    st.write(
        """
        AI-Powered Study Assistant

        **Features:**
        - Topic Explanation
        - Notes Summary
        - Quiz Generator
        - Flashcards
        - Analytics
        """
    )
    st.balloons()
    st.button("All rights reserved | Made by Mili Srivastava | Edunet IBMSkills Build")

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("📚 AI-Powered Study Buddy")

mode = st.selectbox(
    "Choose Feature",
    [
        "Explain Topic",
        "Summarize Notes",
        "Generate Quiz",
        "Generate Flashcards"
    ]
)

# ---------------------------------------------------
# EXPLAIN TOPIC
# ---------------------------------------------------

if mode == "Explain Topic":

    topic = st.text_input(
        "Enter Topic"
    )

    if st.button("Explain"):

        with st.spinner("Generating explanation..."):

            result = explain_topic(topic)

            st.subheader("Explanation")

            st.write(result)

# ---------------------------------------------------
# SUMMARIZE NOTES
# ---------------------------------------------------

elif mode == "Summarize Notes":

    notes = st.text_area(
        "Paste Notes",
        height=250
    )

    if st.button("Summarize"):

        with st.spinner("Summarizing..."):

            summary = summarize_notes(notes)

            st.subheader("Summary")

            st.success(summary)

            words = len(notes.split())

            analytics = pd.DataFrame({
                "Metric": [
                    "Word Count",
                    "Summary Length"
                ],
                "Value": [
                    words,
                    len(summary.split())
                ]
            })

            fig = px.bar(
                analytics,
                x="Metric",
                y="Value",
                title="Study Analytics"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

# ---------------------------------------------------
# QUIZ
# ---------------------------------------------------

elif mode == "Generate Quiz":

    notes = st.text_area(
        "Paste Notes",
        height=250
    )

    if "quiz" not in st.session_state:
        st.session_state.quiz = None

    if st.button("Generate Quiz"):

        with st.spinner("Generating quiz..."):
            st.session_state.quiz = generate_quiz(notes)

    if st.session_state.quiz:

        st.subheader("Quiz Questions")

        for i, q in enumerate(st.session_state.quiz):

            st.write("### " + q["question"])

            if st.checkbox(
                "Show Answer",
                key=f"answer_{i}"
            ):
                st.success(q["answer"])

# ---------------------------------------------------
# FLASHCARDS
# ---------------------------------------------------
elif mode == "Generate Flashcards":

    notes = st.text_area(
        "Paste Notes",
        height=250
    )

    if st.button("Generate Flashcards"):

        with st.spinner("Generating Flashcards..."):
            st.session_state.flashcards = generate_flashcards(notes)

    if "flashcards" in st.session_state:

        st.subheader("🃏 Flashcards")

        for i, card in enumerate(st.session_state.flashcards):

            with st.container(border=True):

                st.markdown(
                    f"""
### 🃏 Flashcard {i+1}

**Front Side**

📌 {card['front']}
"""
                )

                if st.button(
                    f"🔄 Flip Card {i+1}",
                    key=f"flip_{i}"
                ):

                    st.success(card["back"])
# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "AI Study Buddy | IBM SkillsBuild Internship Project"
)
