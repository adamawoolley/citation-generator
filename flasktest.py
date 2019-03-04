from flask import Flask
from flask import render_template
from cite import *
# from flask import Markup
from flask import request as r

app = Flask(__name__)

@app.route("/")
def citation_selection():
	return render_template("home.html")

@app.route("/manual", methods=["POST"])
def manual():
	global cite_names
	global format
	format = r.form["format"]
	if not r.form["url"].startswith("http"):
		url = f"http://{r.form['url']}"
	else:
		url = r.form["url"]
	results, cite_names = cite(format, url)
	return render_template("manual.html", results=results)

@app.route("/citation", methods=["POST"])
def citation():
	results = []
	for name in cite_names:
		results.append(r.form[name])
	print(results)
	if format == "apa":
		if results[0] != "":
			results[0] != ". "
		if results[1] != "":
			results[1] = f"({results[1]}) "
		if results[2] != "":
			results[2] += ". "
		results[2] = f"<i>{results[2]}</i>"
		results[3] += ". "
	elif format == "chicago":
		if results[0] != "":
			results[0] += ". "
		if results[1] != "":
			results[1] = f'"{results[1]}." '
		if results[2] != "":
			results[2] != ". "
		results[3] += ". "
		if results[4] != "":
			results[4] = f"({results[4]})."

	return render_template("citation.html", citation="".join(results))

if __name__ == "__main__":
	app.run()
