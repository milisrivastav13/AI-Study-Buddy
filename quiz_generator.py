def generate_quiz(text):
 sentences = text.split(".")
 quiz = []


 question_starters = [
    "What is",
    "Explain",
    "Describe",
    "What do you know about",
    "Why is"
]

 q_no = 1

 for sentence in sentences:
     sentence = sentence.strip()

     if len(sentence) > 30:
        words = sentence.split()

        if len(words) >= 3:
            topic = " ".join(words[:3])

            quiz.append({
                "question": f"Q{q_no}: {question_starters[q_no % len(question_starters)]} {topic}?",
                "answer": sentence
            })

            q_no += 1

        if q_no > 5:
            break

 return quiz

