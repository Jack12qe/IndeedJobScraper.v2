from flask import Flask, render_template, request, redirect, send_file
from scraper import get_jobs
from exporter import save_to_csv

app = Flask("IndeedJobScraper")
db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/report")
def report():
    word = request.args.get("word")
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = get_jobs(word)
            db[word] = jobs
    else:
        return redirect("/")
    return render_template(
        "report.html", resultsNumber=len(jobs), searchingBy=word, jobs=jobs
    )


@app.route("/export")
def export():
    try:
        word = request.args.get("word")
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_csv(jobs)
        return send_file("indeed_jobs.csv")
    except:
        redirect("/")


app.run(host="127.0.0.1")
