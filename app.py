from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


def get_top_issue(text):
    # Split text into sentences
    sentences = [s.strip() for s in text.replace("!", ".").replace("?", ".").split(".") if s.strip()]
    negative_words = ["bad", "poor", "confusing", "unclear", "difficult", "boring", "fast", "rushed", "stressful"]
    
    # Find the first sentence that contains a negative word
    for sentence in sentences:
        if any(word in sentence.lower() for word in negative_words):
            return sentence
    return "No clear issues detected."


@app.route("/summarise", methods=["POST"])
def summarise():
    text = request.form.get("feedback", "").strip()
    if not text:
        return render_template("index.html", error="Please paste some feedback first.")

    words = text.lower().split()
    themes = []
    if any(w in words for w in ["teacher", "teaching", "lecturer", "explained"]):
        themes.append("teaching")
    if any(w in words for w in ["pace", "fast", "slow", "rushed"]):
        themes.append("pace")
    if any(w in words for w in ["exam", "test", "grading", "assignment"]):
        themes.append("assessment")
    if any(w in words for w in ["slides", "materials", "notes", "moodle"]): # I added moodle here!
        themes.append("materials")
    if not themes:
        themes = ["general"]

    positive = ["good", "great", "helpful", "clear", "useful", "enjoyed", "engaging"] # I added engaging here!
    negative = ["bad", "poor", "confusing", "unclear", "difficult", "boring", "stressful"] # I added stressful here!
    pos = sum(1 for w in words if w in positive)
    neg = sum(1 for w in words if w in negative)
    if pos + neg == 0:
        sentiment = "neutral"
    elif pos > neg:
        sentiment = "positive"
    elif neg > pos:
        sentiment = "negative"
    else:
        sentiment = "mixed"

    return render_template(
        "result.html",
        themes=themes,
        sentiment=sentiment,
        word_count=len(words),
        original=text,
        top_issue=get_top_issue(text),
    )


if __name__ == "__main__":
    app.run(debug=True)