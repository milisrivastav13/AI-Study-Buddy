TOPIC_ALIASES = {

    "ai": "artificial intelligence",
    "ml": "machine learning",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "iot": "internet of things",

    "ann": "artificial neural network",
    "cnn": "convolutional neural network",
    "rnn": "recurrent neural network",
    "llm": "large language model",

    "ds": "data science",
    "dbms": "database management system",
    "os": "operating system",
    "cn": "computer networks",

    "se": "software engineering",
    "svm": "support vector machine",

    "rl": "reinforcement learning",

    "genai": "generative ai",
    "gpt": "chatgpt",

    "cs": "cyber security"
}


TOPICS = {

"artificial intelligence":
"Artificial Intelligence (AI) is the simulation of human intelligence in machines. AI systems can learn, reason, solve problems, and make decisions. Applications include chatbots, recommendation systems, virtual assistants, healthcare systems, and autonomous vehicles.",

"machine learning":
"Machine Learning is a branch of Artificial Intelligence that enables computers to learn patterns from data and make predictions without explicit programming. It is widely used in recommendation systems, fraud detection, spam filtering, and predictive analytics.",

"deep learning":
"Deep Learning is a subset of Machine Learning that uses neural networks with multiple layers to learn complex patterns from large datasets. It is commonly used in image recognition, speech processing, and natural language understanding.",

"natural language processing":
"Natural Language Processing (NLP) enables computers to understand, interpret, and generate human language. Applications include chatbots, language translation, sentiment analysis, text summarization, and voice assistants.",

"computer vision":
"Computer Vision is a field of AI that enables machines to understand and analyze images and videos. It is used in facial recognition, object detection, medical imaging, and autonomous vehicles.",

"data science":
"Data Science combines statistics, machine learning, and data analysis techniques to extract useful insights and knowledge from data.",

"data mining":
"Data Mining is the process of discovering hidden patterns and useful information from large datasets using statistical and machine learning techniques.",

"big data":
"Big Data refers to extremely large and complex datasets that cannot be processed using traditional methods. It is characterized by volume, velocity, and variety.",

"cloud computing":
"Cloud Computing provides on-demand computing resources such as storage, servers, and software over the internet. It enables scalability, flexibility, and cost efficiency.",

"edge computing":
"Edge Computing processes data closer to its source rather than relying on centralized cloud servers, reducing latency and improving performance.",

"internet of things":
"The Internet of Things (IoT) connects physical devices through the internet, allowing them to collect, exchange, and analyze data automatically.",

"blockchain":
"Blockchain is a decentralized digital ledger technology that securely records transactions across multiple computers. It is widely used in cryptocurrencies and secure data management.",

"cyber security":
"Cyber Security focuses on protecting systems, networks, and data from cyber threats, attacks, and unauthorized access.",

"ethical hacking":
"Ethical Hacking involves legally testing systems and networks to identify vulnerabilities and improve security.",

"cryptography":
"Cryptography is the practice of securing information through encryption techniques to protect confidentiality and integrity.",

"database management system":
"A Database Management System (DBMS) is software that allows users to create, manage, and retrieve data efficiently from databases.",

"sql":
"SQL (Structured Query Language) is a programming language used to manage and manipulate relational databases.",

"operating system":
"An Operating System is system software that manages computer hardware and software resources while providing services to applications.",

"computer networks":
"Computer Networks enable multiple devices to communicate and share resources through wired or wireless connections.",

"software engineering":
"Software Engineering is the systematic application of engineering principles to design, develop, test, and maintain software systems.",

"object oriented programming":
"Object-Oriented Programming (OOP) is a programming paradigm based on objects and classes, promoting reusability, modularity, and maintainability.",

"python":
"Python is a high-level programming language known for its simplicity and extensive use in web development, data science, AI, and automation.",

"java":
"Java is a platform-independent object-oriented programming language widely used in enterprise applications and Android development.",

"c++":
"C++ is a powerful programming language used in system programming, game development, and performance-critical applications.",

"generative ai":
"Generative AI is a branch of Artificial Intelligence that creates new content such as text, images, audio, and videos using trained models.",

"large language model":
"Large Language Models (LLMs) are AI models trained on massive text datasets to understand and generate human-like language.",

"chatgpt":
"ChatGPT is a conversational AI model developed by OpenAI that can answer questions, generate content, summarize text, and assist users in various tasks.",

"neural network":
"A Neural Network is a computational model inspired by the human brain. It consists of interconnected nodes that process information and learn patterns from data.",

"convolutional neural network":
"A Convolutional Neural Network (CNN) is a deep learning architecture primarily used for image recognition and computer vision tasks.",

"recurrent neural network":
"A Recurrent Neural Network (RNN) is a neural network designed for sequential data processing such as text, speech, and time-series data.",

"reinforcement learning":
"Reinforcement Learning is a machine learning approach where an agent learns by interacting with an environment and receiving rewards or penalties.",

"supervised learning":
"Supervised Learning is a machine learning technique where models are trained using labeled datasets to make predictions.",

"unsupervised learning":
"Unsupervised Learning is a machine learning technique that identifies patterns and structures in unlabeled data.",

"decision tree":
"A Decision Tree is a machine learning algorithm that uses a tree-like structure for classification and prediction tasks.",

"random forest":
"Random Forest is an ensemble machine learning algorithm that combines multiple decision trees to improve prediction accuracy.",

"support vector machine":
"Support Vector Machine (SVM) is a supervised learning algorithm used for classification and regression problems.",

"artificial neural network":
"Artificial Neural Networks (ANNs) are computing systems inspired by biological neural networks and are widely used in machine learning applications."
}


def explain_topic(topic):

    topic = topic.lower().strip()

    if topic in TOPIC_ALIASES:
        topic = TOPIC_ALIASES[topic]

    if topic in TOPICS:
        return TOPICS[topic]

    return f"""
{topic.title()} is an important concept in computer science and technology.
It has applications in modern systems and contributes to solving real-world problems.
Further study can help understand its concepts, benefits, and practical uses.
"""
