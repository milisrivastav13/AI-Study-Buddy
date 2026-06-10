def summarize_notes(text):

    sentences = text.split(".")

    sentences = [s.strip() for s in sentences if s.strip()]

    if len(sentences) <= 3:
        return ". ".join(sentences)

    summary = ". ".join(sentences[:3])

    return summary + "."
