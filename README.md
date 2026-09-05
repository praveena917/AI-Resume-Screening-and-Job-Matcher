# 🤖 AI Resume Screening & Job Matcher

An AI-powered web application that analyzes a candidate's resume against a job description and generates an intelligent **resume-to-job match score**.

The application combines **skill-based matching, job capability analysis, and semantic similarity** to evaluate how well a candidate fits a particular role.

---

## 📌 Overview

Recruiters often need to manually compare resumes with job descriptions to identify relevant skills and candidate suitability.

This project automates that initial screening process by:

* Extracting information from PDF resumes
* Detecting technical skills from resumes
* Extracting required and preferred skills from job descriptions
* Comparing candidate skills with job requirements
* Identifying matched and missing skills
* Detecting job-related capabilities
* Calculating semantic similarity using an NLP model
* Generating an overall AI match score
* Providing a human-readable recommendation

The application is built using **Python, Streamlit, NLP, Sentence Transformers, and Scikit-learn**.

---

## ✨ Features

### 📄 Resume Parsing

Upload a resume in PDF format and automatically extract:

* Candidate name
* Email address
* Phone number
* Resume sections
* Technical skills
* Education
* Experience
* Projects
* Certifications
* Achievements

### 💼 Job Description Analysis

The application analyzes a job description to identify:

* Required skills
* Preferred skills
* Job capabilities
* Technical requirements

It supports common skills such as:

`Python` · `SQL` · `Power BI` · `Excel` · `Pandas` · `NumPy` · `Tableau` · `Git` · `GitHub` · `Machine Learning` and more.

### 🛠️ Skill Matching

The system compares the candidate's skills against the skills mentioned in the job description.

It identifies:

* ✅ Matched skills
* ❌ Missing skills
* Required skill matches
* Preferred skill matches

### 🧩 Capability Matching

Beyond individual technical skills, the system identifies capabilities required by the job, such as:

* Data Analysis
* Data Cleaning
* Data Quality
* Data Validation
* Data Integration
* Automation
* Dashboard Support
* Data Queries
* Anomaly Detection
* Predictive Analytics
* Documentation
* Problem Solving

These capabilities are then compared against the candidate's resume.

### 🧠 Semantic Matching

The project uses the **`all-MiniLM-L6-v2` Sentence Transformer model** to calculate semantic similarity between the resume and job description.

This helps identify meaningful similarity even when the exact same wording is not used.

### 🎯 AI Match Score

The final score combines multiple dimensions:

| Component           | Weight |
| ------------------- | -----: |
| Required Skills     |    45% |
| Preferred Skills    |    15% |
| Job Capabilities    |    20% |
| Semantic Similarity |    20% |

If a job description does not contain preferred skills or detectable capabilities, the corresponding weight is redistributed across the remaining scoring dimensions.

### 🤖 Recommendation

The application converts the final score into an easy-to-understand recommendation:

| Score     | Recommendation     |
| --------- | ------------------ |
| 80%+      | 🟢 Excellent Match |
| 70–79%    | 🟢 Good Match      |
| 55–69%    | 🟡 Partial Match   |
| Below 55% | 🔴 Poor Match      |

---

## 🏗️ Project Architecture

```text
AI Resume Screening & Job Matcher/
│
├── app.py
├── job_description.txt
├── requirements.txt
│
├── Resumes/
│   └── Praveena_Resume.pdf
│
├── src/
│   ├── capability_analyzer.py
│   ├── job_analyzer.py
│   ├── matcher.py
│   ├── recommendation.py
│   ├── resume_parser.py
│   ├── section_extractor.py
│   ├── semantic_matcher.py
│   └── skill_extractor.py
│
├── test_job.py
├── test_resume.py
└── test_semantic.py
```

---

## 🔄 How It Works

```text
                 ┌──────────────────┐
                 │   Resume PDF     │
                 └────────┬─────────┘
                          │
                          ▼
                ┌────────────────────┐
                │  Resume Text       │
                │    Extraction      │
                └─────────┬──────────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
      ┌───────────────┐       ┌────────────────┐
      │ Skill         │       │ Resume Section │
      │ Extraction    │       │ Extraction     │
      └───────┬───────┘       └────────────────┘
              │
              │
              ▼
      ┌─────────────────────┐
      │ Resume Skill Set    │
      └──────────┬──────────┘
                 │
                 │
                 │        ┌────────────────────┐
                 │        │ Job Description    │
                 │        └─────────┬──────────┘
                 │                  │
                 │                  ▼
                 │        ┌────────────────────┐
                 │        │ Job Skill &        │
                 │        │ Capability         │
                 │        │ Extraction         │
                 │        └─────────┬──────────┘
                 │                  │
                 └──────────┬───────┘
                            ▼
                 ┌─────────────────────┐
                 │ Skill & Capability  │
                 │ Matching            │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Semantic Similarity │
                 │ all-MiniLM-L6-v2    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Final AI Match      │
                 │ Score               │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Recommendation      │
                 │ Excellent / Good /  │
                 │ Partial / Poor      │
                 └─────────────────────┘
```

---

## 🧰 Tech Stack

### Programming Language

* **Python**

### Frontend / UI

* **Streamlit**

### PDF Processing

* **PyMuPDF**

### NLP / Machine Learning

* **Sentence Transformers**
* `all-MiniLM-L6-v2`

### Similarity Calculation

* **Scikit-learn**
* Cosine Similarity

### Data Processing

* Python Regular Expressions (`re`)
* Custom rule-based skill extraction

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/AI-Resume-Screening-Job-Matcher.git
cd AI-Resume-Screening-Job-Matcher
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

Start the Streamlit application using:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🖥️ Using the Application

1. Upload a **resume PDF**.
2. Paste the **job description** into the text area.
3. Click **Analyze Resume**.
4. The application processes the resume and job description.
5. Review:

   * Candidate information
   * Final AI match score
   * Score breakdown
   * Matched skills
   * Missing skills
   * Required skills
   * Preferred skills
   * Job capabilities
   * Resume skills
   * Job skills
   * Resume sections
   * AI recommendation

---

## 🧪 Testing

The project includes separate test files for different components.

### Test job skill extraction

```bash
python test_job.py
```

### Test resume analysis

```bash
python test_resume.py
```

### Test semantic similarity

```bash
python test_semantic.py
```

---

## 📊 Example Output

For a Data Analyst position, the application can produce an output similar to:

```text
AI Match Score: 82.45%

Recommendation:
🟢 EXCELLENT MATCH

Required Skills:
✓ Python
✓ SQL
✓ Pandas
✓ NumPy
✓ Power BI
✓ Excel
✓ Matplotlib
✓ Seaborn

Preferred Skills:
✓ Machine Learning
✗ Tableau
✓ Git
✓ GitHub

Skill Analysis:
Matched Skills → Python, SQL, Power BI, Pandas, NumPy...
Missing Skills → Tableau...

Semantic Similarity:
84.21%
```

*The actual score depends on the uploaded resume and job description.*

---

## 🧠 Scoring Methodology

The final score is calculated using four major dimensions.

### 1. Required Skill Match — 45%

Measures how many explicitly required skills from the job description are present in the resume.

```text
Required Skill Score =
Matched Required Skills / Total Required Skills × 100
```

### 2. Preferred Skill Match — 15%

Measures the candidate's coverage of preferred or desirable skills.

```text
Preferred Skill Score =
Matched Preferred Skills / Total Preferred Skills × 100
```

### 3. Capability Match — 20%

Measures how many job-related capabilities detected in the job description are represented in the resume.

```text
Capability Score =
Matched Capabilities / Total Job Capabilities × 100
```

### 4. Semantic Similarity — 20%

Uses sentence embeddings and cosine similarity to measure the semantic relationship between the resume and job description.

---

## 🔍 Key Modules

### `resume_parser.py`

Extracts basic candidate information:

* Name
* Email
* Phone number

### `section_extractor.py`

Identifies common resume sections using section aliases such as:

* Summary
* Experience
* Education
* Skills
* Projects
* Certifications
* Achievements

### `skill_extractor.py`

Contains the project's skill vocabulary and extracts recognized technical skills from text using normalized, word-boundary-aware matching.

### `job_analyzer.py`

Analyzes job descriptions and classifies skills as:

* Required
* Preferred

It supports both phrase-based classification and heading-based extraction.

### `capability_analyzer.py`

Detects job capabilities and compares them with capabilities represented in the resume.

### `semantic_matcher.py`

Uses:

```text
all-MiniLM-L6-v2
```

to generate sentence embeddings and calculates cosine similarity between the resume and job description.

### `matcher.py`

Combines the individual scores using the defined weighting system to calculate the final match score.

### `recommendation.py`

Converts the final numerical score into a recommendation:

```text
EXCELLENT MATCH
GOOD MATCH
PARTIAL MATCH
POOR MATCH
```

### `app.py`

Provides the Streamlit interface and integrates all analysis modules into a single application.

---

## 🚀 Future Improvements

Potential enhancements include:

* [ ] Support for DOCX resumes
* [ ] Support for multiple resumes at once
* [ ] Resume ranking for multiple candidates
* [ ] More comprehensive skill ontology
* [ ] Improved contextual skill extraction
* [ ] Experience-level matching
* [ ] Education requirement matching
* [ ] Job-role classification
* [ ] Candidate ranking dashboard
* [ ] Export analysis results to PDF/Excel
* [ ] Recruiter dashboard
* [ ] Database integration
* [ ] Cloud deployment
* [ ] More advanced transformer-based resume/job matching

---

## ⚠️ Limitations

This project is intended as an **assistive resume-screening tool**, not as a replacement for human recruitment decisions.

Current limitations include:

* Skill extraction depends on the predefined skill vocabulary.
* Capability detection uses keyword-based rules.
* Semantic similarity does not independently verify candidate claims.
* Resume formatting and unusual section names may affect extraction.
* The system does not determine whether a candidate genuinely possesses a claimed skill.
* Results should be reviewed by a human before making hiring decisions.

---

## 🔐 Privacy

Resumes may contain personal information such as names, email addresses, and phone numbers.

For a public GitHub repository, **avoid uploading real candidate resumes or other personally identifiable information** unless you have permission to publish them.

Consider replacing sample resumes with anonymized/demo data before making the repository public.

---

## 👩‍💻 Author

**Praveena K**


### Skills

`Python` `SQL` `Power BI` `Excel` `Pandas` `NumPy` `Data Analysis` `Data Visualization` `Machine Learning`

---
