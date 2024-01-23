from flask import Flask, Response, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app=Flask(__name__)
app.config['SECRET_KEY'] = "secretkey"
app.debug = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# RESPONSES = []

@app.route("/")
def survey_instructions():
    return render_template("survey_instructions.html", survey=satisfaction_survey)

@app.route("/start")
def survey_start():
    # RESPONSES = []
    session["responses"] = []
    return redirect("questions/0")

@app.route("/questions/<int:n>")
def ask_question(n):
    if (session["responses"] == None):
        return redirect("/")
    
    if (len(session["responses"]) == len(satisfaction_survey.questions)):
        return redirect("/complete")
    
    if (len(session["responses"]) != n):
        flash(f"Invalid question: {n}")
        return redirect(f"/questions/{len(session['responses'])}")

    return render_template("question.html", question=satisfaction_survey.questions[n])

@app.route("/complete")
def end_survey():
    return render_template("complete.html", survey=satisfaction_survey)

@app.route("/answer", methods=["POST"])
def parse_answer():
    temp_session = session["responses"]
    temp_session.append(request.form["answer"])
    session["responses"] = temp_session
    n = len(session["responses"])
    # n = request.form["n"]
    if (len(session["responses"]) == len(satisfaction_survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{n}")


# @app.route("/testing")
# def testing():
#     RESPONSES.append(request.args["test"])
#     return render_template("testing.html", responses=RESPONSES)