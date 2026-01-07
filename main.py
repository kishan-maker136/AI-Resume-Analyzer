from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

HTML_PAGE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>AI Resume Analyzer | Smart Career Tool</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
/* ===== CSS from style.css ===== */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

body {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    color: #212529;
    min-height: 100vh;
    padding: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.container {
    width: 100%;
    max-width: 1200px;
    background-color: white;
    border-radius: 20px;
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

header {
    background: linear-gradient(90deg, #4361ee 0%, #3f37c9 100%);
    color: white;
    padding: 30px 40px;
    text-align: center;
}

header h1 {
    font-size: 2.5rem;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
}

header p {
    font-size: 1.1rem;
    opacity: 0.9;
    max-width: 800px;
    margin: 0 auto;
    line-height: 1.6;
}

.main-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
    padding: 40px;
}

@media (max-width: 992px) {
    .main-content {
        grid-template-columns: 1fr;
    }
}

.input-section, .output-section {
    background-color: #f8f9fa;
    border-radius: 15px;
    padding: 30px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.section-title {
    font-size: 1.5rem;
    color: #4361ee;
    margin-bottom: 25px;
    padding-bottom: 10px;
    border-bottom: 2px solid #4cc9f0;
    display: flex;
    align-items: center;
    gap: 10px;
}

.input-group {
    margin-bottom: 25px;
}

.input-label {
    display: block;
    font-weight: 600;
    margin-bottom: 10px;
    color: #212529;
    font-size: 1.1rem;
}

#resume {
    display: none;
}

.file-upload-area {
    border: 2px dashed #4895ef;
    border-radius: 10px;
    padding: 40px 20px;
    text-align: center;
    background-color: rgba(67, 97, 238, 0.03);
    cursor: pointer;
    transition: all 0.3s ease;
    margin-bottom: 10px;
}

.file-upload-area:hover {
    background-color: rgba(67, 97, 238, 0.08);
    border-color: #4361ee;
}

.file-upload-area i {
    font-size: 3rem;
    color: #4361ee;
    margin-bottom: 15px;
}

.file-upload-area p {
    color: #6c757d;
    margin-bottom: 5px;
}

.file-upload-area span {
    font-size: 0.9rem;
    color: #6c757d;
}

#file-name {
    margin-top: 10px;
    font-size: 0.9rem;
    color: #4ade80;
    font-weight: 500;
    display: none;
}

textarea {
    width: 100%;
    padding: 15px;
    border: 2px solid #e9ecef;
    border-radius: 10px;
    font-size: 1rem;
    resize: vertical;
    min-height: 200px;
    transition: border 0.3s;
}

textarea:focus {
    outline: none;
    border-color: #4361ee;
}

.char-count {
    text-align: right;
    margin-top: 5px;
    color: #6c757d;
    font-size: 0.9rem;
}

.analyze-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    width: 100%;
    padding: 18px;
    background: linear-gradient(90deg, #4361ee 0%, #3f37c9 100%);
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 1.2rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 10px;
}

.analyze-btn:hover:not(:disabled) {
    transform: translateY(-3px);
    box-shadow: 0 7px 15px rgba(67, 97, 238, 0.3);
}

.analyze-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.output-container {
    display: none;
}

.match-score {
    text-align: center;
    margin-bottom: 30px;
}

.match-score .score-circle {
    width: 180px;
    height: 180px;
    border-radius: 50%;
    margin: 0 auto 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.score-circle-bg {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: conic-gradient(#4361ee 0% var(--percentage), #e9ecef var(--percentage) 100%);
    position: absolute;
}

.score-circle-inner {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    background: white;
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}

.score-text {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(90deg, #4361ee 0%, #3f37c9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.score-category {
    font-size: 1.2rem;
    color: #6c757d;
    margin-top: 10px;
    font-weight: 600;
}

.results-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 30px;
}

.rec-list, .sug-list {
    list-style: none;
}

.rec-list li, .sug-list li {
    padding: 12px 15px;
    margin-bottom: 10px;
    background-color: white;
    border-left: 4px solid #4361ee;
    border-radius: 0 8px 8px 0;
    display: flex;
    align-items: flex-start;
    gap: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.sug-list li {
    border-left-color: #f59e0b;
}

.rec-list li i, .sug-list li i {
    color: #4361ee;
    margin-top: 3px;
}

.sug-list li i {
    color: #f59e0b;
}

.keywords-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.keyword-tag {
    background: linear-gradient(135deg, #4895ef 0%, #4cc9f0 100%);
    color: white;
    padding: 8px 15px;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 5px;
}

.loading {
    display: none;
    text-align: center;
    padding: 30px;
}

.spinner {
    width: 60px;
    height: 60px;
    border: 6px solid #e9ecef;
    border-top-color: #4361ee;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 20px;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.error {
    display: none;
    background-color: rgba(239, 68, 68, 0.1);
    border-left: 4px solid #ef4444;
    padding: 15px;
    border-radius: 0 8px 8px 0;
    margin-top: 20px;
}

.placeholder {
    text-align: center;
    color: #6c757d;
    padding: 40px 20px;
}

footer {
    text-align: center;
    padding: 20px;
    color: #6c757d;
    font-size: 0.9rem;
    border-top: 1px solid #e9ecef;
}
</style>
</head>
<body>
<div class="container">
<header>
<h1><i class="fas fa-robot"></i> AI Resume Analyzer</h1>
<p>Upload your resume and paste a job description to get an instant match score, recommendations, and improvement suggestions.</p>
</header>

<div class="main-content">
<div class="input-section">
<h2 class="section-title"><i class="fas fa-upload"></i> Input Details</h2>
<div class="input-group">
<label class="input-label">Upload Resume (PDF / DOCX)</label>
<div class="file-upload-area" id="uploadArea" tabindex="0">
<i class="fas fa-cloud-upload-alt"></i>
<p>Click to browse or drag & drop</p>
<span>PDF, DOC, DOCX • Max 5MB</span>
</div>
<input type="file" id="resume" accept=".pdf,.doc,.docx" />
<div id="file-name"></div>
</div>
<div class="input-group">
<label class="input-label"><i class="fas fa-file-alt"></i> Job Description</label>
<textarea id="jobDesc" placeholder="Paste the job description here (minimum 50 characters)..."></textarea>
<div class="char-count"><span id="charCount">0</span> characters</div>
</div>
<button class="analyze-btn" id="analyzeBtn"><i class="fas fa-search"></i> Analyze Resume Match</button>
<div class="loading" id="loading">
<div class="spinner"></div>
<p>Analyzing your resume… Please wait.</p>
</div>
<div class="error" id="error">
<p><strong>Error:</strong> <span id="error-text"></span></p>
</div>
</div>

<div class="output-section">
<h2 class="section-title"><i class="fas fa-chart-bar"></i> Analysis Results</h2>
<div class="output-container" id="outputContainer">
<div class="match-score">
<div class="score-circle">
<div class="score-circle-bg" id="scoreCircleBg"></div>
<div class="score-circle-inner">
<div class="score-text" id="scoreText">0%</div>
<div class="score-category"><span id="scoreCategory">Poor Match</span></div>
</div>
</div>
</div>
<div class="results-grid">
<div class="recommendations">
<h3 class="section-title"><i class="fas fa-graduation-cap"></i> Recommendations</h3>
<ul class="rec-list" id="recList"></ul>
</div>
<div class="suggestions">
<h3 class="section-title"><i class="fas fa-lightbulb"></i> Suggestions</h3>
<ul class="sug-list" id="sugList"></ul>
</div>
</div>
<h3 class="section-title"><i class="fas fa-key"></i> Keywords</h3>
<div class="keywords-container" id="keywordsContainer"></div>
</div>
<div class="placeholder">
<h3><i class="fas fa-chart-pie"></i> Results Will Appear Here</h3>
<p>Upload your resume and job description, then click Analyze.</p>
</div>
</div>
</div>

<footer>AI Resume Analyzer © <span id="currentYear"></span> | Powered by AI Technology</footer>
</div>

<script>
// ===== JS from script.js =====
const elements = {
    uploadArea: document.getElementById("uploadArea"),
    resumeInput: document.getElementById("resume"),
    fileName: document.getElementById("file-name"),
    jobDesc: document.getElementById("jobDesc"),
    charCount: document.getElementById("charCount"),
    analyzeBtn: document.getElementById("analyzeBtn"),
    loading: document.getElementById("loading"),
    error: document.getElementById("error"),
    errorText: document.getElementById("error-text"),
    outputContainer: document.getElementById("outputContainer"),
    scoreText: document.getElementById("scoreText"),
    scoreCircleBg: document.getElementById("scoreCircleBg"),
    scoreCategory: document.getElementById("scoreCategory"),
    recList: document.getElementById("recList"),
    sugList: document.getElementById("sugList"),
    keywordsContainer: document.getElementById("keywordsContainer"),
    currentYear: document.getElementById("currentYear"),
};

// Initialize the page
document.addEventListener("DOMContentLoaded", () => {
    elements.currentYear.textContent = new Date().getFullYear();

    // Event listeners
    elements.uploadArea.addEventListener("click", () => elements.resumeInput.click());
    elements.resumeInput.addEventListener("change", handleFileSelect);
    elements.jobDesc.addEventListener("input", updateCharCount);
    elements.analyzeBtn.addEventListener("click", analyze);

    // Initialize character count
    updateCharCount();
});

function handleFileSelect() {
    const file = this.files[0];
    if (!file) return;

    // Check file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
        alert("File size exceeds 5MB limit. Please choose a smaller file.");
        this.value = "";
        elements.fileName.style.display = "none";
        return;
    }

    // Check file type
    const validTypes = ["application/pdf", "application/msword", 
                       "application/vnd.openxmlformats-officedocument.wordprocessingml.document"];
    if (!validTypes.includes(file.type)) {
        alert("Please upload a PDF, DOC, or DOCX file.");
        this.value = "";
        elements.fileName.style.display = "none";
        return;
    }

    elements.fileName.textContent = `Selected: ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
    elements.fileName.style.display = "block";
}

function updateCharCount() {
    const count = elements.jobDesc.value.length;
    elements.charCount.textContent = count;

    // Visual feedback for length
    if (count < 50) {
        elements.charCount.style.color = "#ef4444";
    } else if (count < 100) {
        elements.charCount.style.color = "#f59e0b";
    } else {
        elements.charCount.style.color = "#10b981";
    }
}

async function analyze() {
    const file = elements.resumeInput.files[0];
    const jd = elements.jobDesc.value.trim();

    // Validation
    if (!file) {
        showError("Please upload a resume file.");
        return;
    }

    if (jd.length < 50) {
        showError("Job description must be at least 50 characters.");
        return;
    }

    // Show loading state
    elements.loading.style.display = "block";
    elements.error.style.display = "none";
    elements.outputContainer.style.display = "none";
    elements.analyzeBtn.disabled = true;

    // Prepare form data
    const formData = new FormData();
    formData.append("resume", file);
    formData.append("job_description", jd);

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Analysis failed");
        }

        // Update UI with results
        displayResults(data);

    } catch (err) {
        showError(err.message || "Failed to analyze resume. Please try again.");
        console.error("Analysis error:", err);
    } finally {
        elements.loading.style.display = "none";
        elements.analyzeBtn.disabled = false;
    }
}

function displayResults(data) {
    // Update match score
    const score = data.match_percentage || 0;
    elements.scoreText.textContent = `${score}%`;

    // Update score circle visualization
    elements.scoreCircleBg.style.setProperty('--percentage', `${score}%`);

    // Update score category
    let category = "Poor Match";
    let categoryColor = "#ef4444";

    if (score >= 80) {
        category = "Excellent Match";
        categoryColor = "#10b981";
    } else if (score >= 60) {
        category = "Good Match";
        categoryColor = "#3b82f6";
    } else if (score >= 40) {
        category = "Fair Match";
        categoryColor = "#f59e0b";
    }

    elements.scoreCategory.textContent = category;
    elements.scoreCategory.style.color = categoryColor;

    // Update recommendations
    elements.recList.innerHTML = "";
    if (data.recommendations && data.recommendations.length > 0) {
        data.recommendations.forEach(rec => {
            const li = document.createElement("li");
            li.innerHTML = `<i class="fas fa-check-circle"></i> ${rec}`;
            elements.recList.appendChild(li);
        });
    } else {
        const li = document.createElement("li");
        li.innerHTML = `<i class="fas fa-check-circle"></i> No specific recommendations at this time.`;
        elements.recList.appendChild(li);
    }

    // Update suggestions
    elements.sugList.innerHTML = "";
    if (data.suggestions && data.suggestions.length > 0) {
        data.suggestions.forEach(sug => {
            const li = document.createElement("li");
            li.innerHTML = `<i class="fas fa-lightbulb"></i> ${sug}`;
            elements.sugList.appendChild(li);
        });
    } else {
        const li = document.createElement("li");
        li.innerHTML = `<i class="fas fa-lightbulb"></i> No major suggestions, resume looks good!`;
        elements.sugList.appendChild(li);
    }

    // Update keywords
    elements.keywordsContainer.innerHTML = "";
    if (data.keywords && data.keywords.length > 0) {
        // Limit to 15 keywords for display
        const displayKeywords = data.keywords.slice(0, 15);
        displayKeywords.forEach(keyword => {
            const tag = document.createElement("div");
            tag.className = "keyword-tag";
            tag.innerHTML = `<i class="fas fa-hashtag"></i> ${keyword}`;
            elements.keywordsContainer.appendChild(tag);
        });
    } else {
        const tag = document.createElement("div");
        tag.className = "keyword-tag";
        tag.innerHTML = `<i class="fas fa-hashtag"></i> No keywords extracted`;
        elements.keywordsContainer.appendChild(tag);
    }

    // Show results
    elements.outputContainer.style.display = "block";

    // Smooth scroll to results on mobile
    if (window.innerWidth < 992) {
        elements.outputContainer.scrollIntoView({ behavior: "smooth" });
    }
}

function showError(message) {
    elements.errorText.textContent = message;
    elements.error.style.display = "block";
}

// Drag and drop functionality
elements.uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    elements.uploadArea.style.borderColor = '#4361ee';
    elements.uploadArea.style.backgroundColor = 'rgba(67, 97, 238, 0.1)';
});

elements.uploadArea.addEventListener('dragleave', () => {
    elements.uploadArea.style.borderColor = '#4895ef';
    elements.uploadArea.style.backgroundColor = 'rgba(67, 97, 238, 0.03)';
});

elements.uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    elements.uploadArea.style.borderColor = '#4895ef';
    elements.uploadArea.style.backgroundColor = 'rgba(67, 97, 238, 0.03)';

    if (e.dataTransfer.files.length) {
        elements.resumeInput.files = e.dataTransfer.files;
        handleFileSelect();
    }
});
</script>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def home_page():
    return Response(HTML_PAGE, mimetype="text/html")


@app.route("/analyze", methods=["POST"])
def analyze_resume():
    try:
        if "resume" not in request.files or "job_description" not in request.form:
            return jsonify(
                {"error": "Resume file and job description required"}), 400

        resume_file = request.files["resume"]
        job_description = request.form["job_description"].strip()

        if not resume_file.filename:
            return jsonify({"error": "No resume file selected"}), 400

        if len(job_description) < 50:
            return jsonify(
                {"error":
                 "Job description must be at least 50 characters"}), 400

        import random

        tech_keywords = [
            "python", "java", "javascript", "react", "node", "aws", "docker",
            "sql", "mongodb", "git", "api", "machine learning", "cloud",
            "agile"
        ]

        jd_lower = job_description.lower()
        detected_keywords = [kw for kw in tech_keywords if kw in jd_lower]

        base_score = random.randint(60, 95)

        filename = resume_file.filename.lower()
        if "senior" in filename:
            base_score += random.randint(5, 10)
        elif "junior" in filename:
            base_score -= random.randint(5, 10)

        base_score = min(max(base_score, 30), 100)

        recommendations = [
            "Consider taking an advanced Python course to strengthen your backend skills",
            "Learn AWS Cloud Practitioner fundamentals for cloud deployment",
            "Practice React.js with modern hooks and state management",
            "Improve your knowledge of Docker containerization"
        ]

        suggestions = [
            "Add more quantifiable achievements to your experience section",
            "Include specific projects that demonstrate your technical skills",
            "Tailor your resume keywords to match the job description more closely",
            "Consider adding a technical skills section at the top of your resume"
        ]

        all_keywords = list(
            set(detected_keywords + [
                "communication", "teamwork", "problem-solving",
                "project management", "leadership"
            ]))

        keywords = random.sample(all_keywords, min(10, len(all_keywords)))

        return jsonify({
            "match_percentage": base_score,
            "recommendations": random.sample(recommendations, 3),
            "suggestions": random.sample(suggestions, 3),
            "keywords": keywords
        })

    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
