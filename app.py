from flask import Flask, render_template, request, send_file, session
from ai.ai_generator import generate_resume
from database.db_config import save_student
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for session


# -------------------------
# PDF Download Route
# -------------------------
@app.route('/download')
def download():

    if "resume_data" not in session:
        return "No resume data available."

    data = session["resume_data"]

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Name Header
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(300, 770, data.get("name", "Resume"))

    y = 740

    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(300, y, f"{data.get('email', '')} | {data.get('phone', '')}")
    y -= 30

    pdf.line(40, y, 550, y)
    y -= 20

    resume_text = data.get("resume", "")
    lines = resume_text.split("\n")

    pdf.setFont("Helvetica", 12)

    for line in lines:
        if y < 60:
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y = 750

        pdf.drawString(50, y, line.strip())
        y -= 18

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Professional_Resume.pdf",
        mimetype="application/pdf"
    )


# -------------------------
# Main Route
# -------------------------
@app.route('/', methods=['GET', 'POST'])
def index():

    resume = ""

    if request.method == 'POST':

        name = request.form['name']
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        skills = request.form['skills']
        education = request.form['education']
        projects = request.form['projects']

        # Generate Resume using AI
        resume = generate_resume(name, skills, education, projects)

        # Save to database
        save_student(name, email, phone, skills, education, projects, resume)

        # Store in session (instead of global variable)
        session["resume_data"] = {
            "name": name,
            "email": email,
            "phone": phone,
            "resume": resume
        }

    return render_template('index.html', resume=resume)


# -------------------------
# Run App
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)