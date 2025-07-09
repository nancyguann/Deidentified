"""
Making HTML website
"""
FILE = "website.html"
DATA = "anonymous.csv"
import pandas as pd
from flask import Flask, request, render_template_string

app = Flask(__name__)
df = pd.read_csv(DATA)

# HTML form page
HTML_FORM = """
<!DOCTYPE html>
<html>
  <head>
    <title>Patient Lookup</title>
  </head>
  <body style="text-align: center; font-family: Arial, sans-serif;">
    <h1>Patient Most Recent</h1>
    <h2>Enter a number:</h2>
    <form action="/process_number" method="post">
      <input type="number" name="user_number" required>
      <button type="submit">Submit</button>
    </form>
  </body>
</html>
"""
@app.route("/", methods=["GET"])
def form():
    return HTML_FORM

def get_patient_info(df, patient):
    patient = str(patient)
    filtered_df = df[df["Deidentified"].astype(str) == patient]

    if not filtered_df.empty:
        latest_row = filtered_df.iloc[-1]
        line = latest_row["Line of Treatment"]
        date = latest_row["Plan Start Date"]
        status = latest_row["Plan Status"]

        html_table = filtered_df.to_html(index=False)

        return (f"<h2>Patient {patient}'s most recent plan:</h2>"
                f"<p Line: {line}<br>Date: {date}<br> Status: {status}</p>"
                f"<h3>All Plans for Patient {patient}</h3>"
                f"{html_table}")
    else:
        return f"<h2>No data found for patient {patient}.</h2>"

@app.route("/process_number", methods=["POST"])
def process_number():
    number = request.form.get("user_number")
    if number:
        number = str(number)
        result = get_patient_info(df, number)
        return result
    return "<h2>Invalid input.</h2>"

if __name__ == "__main__":
    app.run(debug=True)
