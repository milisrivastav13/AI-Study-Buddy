def generate_flashcards(text):

    sentences = text.split(".")
    flashcards = []

    for sentence in sentences:

        sentence = sentence.strip()

        if len(sentence) > 30:

            words = sentence.split()

            # Front = topic/term
            front = words[0]

            if len(words) > 1:
                front += " " + words[1]

            # Back = remaining explanation
            back = " ".join(words[2:])

            flashcards.append({
                "front": front,
                "back": back
            })

    return flashcards