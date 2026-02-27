from openai import OpenAI

# Keep API integration
client = OpenAI(api_key="YOUR_OPENAI_KEY")

def generate_resume(name, skills, education, projects, template="professional"):

    prompt = f"""
Generate a professional ATS-friendly resume.

Name: {name}
Skills: {skills}
Education: {education}
Projects: {projects}

Structure:
CAREER OBJECTIVE
TECHNICAL SKILLS
PROJECT EXPERIENCE
EDUCATION
KEY STRENGTHS
DECLARATION
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=800
        )

        return response.choices[0].message.content.strip()

    except Exception:
        # Fallback AI-style generation (Offline NLG)
        return local_ai_generator(name, skills, education, projects)


def local_ai_generator(name, skills, education, projects):

    skills_list = [s.strip() for s in skills.split(",") if s.strip()]

    objective = f"""
Motivated Computer Science Engineering student with expertise in {', '.join(skills_list[:3])}. 
Seeking internship opportunities to apply technical skills and contribute to innovative projects.
"""

    resume = f"""
CAREER OBJECTIVE
{objective.strip()}

TECHNICAL SKILLS
"""

    for skill in skills_list:
        resume += f"- {skill}\n"

    resume += f"""

PROJECT EXPERIENCE
{projects}

EDUCATION
{education}

KEY STRENGTHS
- Problem-solving
- Analytical thinking
- Quick learner
- Team collaboration

DECLARATION
I hereby declare that the above information is true.

{name}
"""

    return resume.strip()