import re


SKILL_SYNONYMS = {
    "python": ["python", "py"],
    "javascript": ["javascript", "js"],
    "machine learning": ["machine learning", "ml"],
    "cybersecurity": ["cybersecurity", "security", "infosec"],
    "docker": ["docker", "containers"],
    "aws": ["aws", "amazon web services"],
    "linux": ["linux", "unix"]
}



def normalize_text(text):

  return re.sub(r"[^a-zA-Z0-9 ]", " ", text.lower())



def extract_skills(text):
  text = normalize_text(text)
  found = set()
  for skill, variations in SKILL_SYNONYMS.items():
    for v in variations:
      if v in text:
        found.add(skill)
  return found



def calculate_match(resume_text, job_description):
  resume_skills = extract_skills(resume_text)
  jd_skills = extract_skills(job_description)

  matched = resume_skills & jd_skills
  missing = jd_skills - resume_skills

  
  if not jd_skills:
    score = 0
  else:
    score = int((len(matched) / len(jd_skills)) * 100)

  return score, list(missing)
