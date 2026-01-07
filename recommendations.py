
SKILL_RECOMMENDATIONS = {
    "python":
    ["Take an advanced Python course", "Add Python projects to your resume"],
    "javascript":
    ["Practice JavaScript projects", "Include frontend frameworks experience"],
    "machine learning": [
        "Take a Machine Learning/AI course",
        "Add ML projects or Kaggle competitions"
    ],
    "cybersecurity": [
        "Complete a cybersecurity certification (CEH, CompTIA Security+)",
        "Include security-related projects or labs"
    ],
    "docker":
    ["Learn Docker and containerization", "Add Docker deployment projects"],
    "aws":
    ["Take AWS Cloud Practitioner course", "Include AWS cloud projects"],
    "linux": [
        "Improve Linux command line skills",
        "Add Linux-based project experience"
    ]
}


DEFAULT_RECOMMENDATIONS = [
    "Highlight relevant projects",
    "Add certifications or courses related to missing skills",
    "Include soft skills and teamwork experience"
]


def recommend_courses(missing_skills):
  """
    Returns a dynamic list of recommended courses or actions
    based on missing skills from the resume.
    """
  recommendations = []

 
  for skill in missing_skills:
    if skill.lower() in SKILL_RECOMMENDATIONS:
      recommendations.extend(SKILL_RECOMMENDATIONS[skill.lower()])
    else:
      recommendations.extend(DEFAULT_RECOMMENDATIONS)

  
  recommendations = list(dict.fromkeys(recommendations))

  
  return recommendations[:5]
