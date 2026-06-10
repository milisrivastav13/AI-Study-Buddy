def explain_topic(topic):

    topic = topic.lower()

    topics = {

        "artificial intelligence":
        """Artificial Intelligence (AI) is a branch of computer science that enables machines to perform tasks that normally require human intelligence such as learning, reasoning, problem solving, and decision making.""",
        "Artificial Intelligence":
        """Artificial Intelligence (AI) is a branch of computer science that enables machines to perform tasks that normally require human intelligence such as learning, reasoning, problem solving, and decision making.""",
        "AI":
        """Artificial Intelligence (AI) is a branch of computer science that enables machines to perform tasks that normally require human intelligence such as learning, reasoning, problem solving, and decision making.""",

        "machine learning":
        """Machine Learning is a subset of AI that allows computers to learn from data without being explicitly programmed. It is used in recommendation systems, spam filtering, and image recognition.""",

        "deep learning":
        """Deep Learning is a type of Machine Learning that uses neural networks with many layers. It is commonly used in speech recognition, image processing, and self-driving cars.""",

        "nlp":
        """Natural Language Processing (NLP) enables computers to understand, interpret, and generate human language. Examples include chatbots, translators, and voice assistants.""",

        "ai ethics":
        """AI Ethics focuses on ensuring that AI systems are fair, transparent, safe, and unbiased while protecting user privacy and human rights.""",

        "data science":
        """Data Science combines statistics, programming, and domain knowledge to extract insights from data and support decision-making.""",

        "cyber security":
        """Cyber Security protects computer systems, networks, and data from unauthorized access, attacks, and damage."""
    }

    return topics.get(
        topic,
        f"Explanation for '{topic}' is not available."
    )
