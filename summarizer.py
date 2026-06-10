from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk

try:
    nltk.data.find("tokenizers/punkt")
except:
    nltk.download("punkt")
def summarize_notes(text):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()

    summary = summarizer(parser.document, 3)

    return " ".join([str(sentence) for sentence in summary])
