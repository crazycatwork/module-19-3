from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

# session data
RESPONSES_KEY = "responses"

app = Flask(__name__)

app.config['SECRET_KEY'] = "mysecretkey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def index():
    return render_template('start.html', survey=survey)

@app.route("/start", methods=["POST"])
def start():
    session[RESPONSES_KEY] = [];
    return redirect("/question/0")

@app.route('/question/<int:num>')
def ask(num):
    responses = session.get(RESPONSES_KEY)
    if (responses is None):
        return redirect("/")
    
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    
    if (len(responses) != num):
        flash(f"Invalid question number: {num}.")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[num]
    return render_template("question.html", question_num=num, question=question)


@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""
    # get the response choice
    choice = request.form['answer']

    # add this response to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/question/{len(responses)}")
    
@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("complete.html")
