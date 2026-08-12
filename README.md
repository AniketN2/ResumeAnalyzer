#  AI Resume Screening & Candidate Ranking System

An AI-powered resume screening application that helps recruiters analyze, compare, score, and rank multiple candidates against a given job description.

The system uses **specialized AI agents, structured outputs, deterministic scoring logic, and LangGraph-based workflow orchestration** to automate the initial stages of the recruitment process.

🔗 **Live Demo:** `YOUR_STREAMLIT_APP_URL`

🔗 **GitHub:** `YOUR_GITHUB_REPOSITORY_URL`

---

## 📌 Overview

Recruiters often have to manually review large numbers of resumes for a single job opening. This process can be time-consuming and inconsistent, especially when candidates have different resume formats and descriptions of their skills and experience.

This project aims to automate the initial screening process.

The application allows a recruiter to:

* Upload multiple resumes in PDF format
* Provide a job description
* Extract structured candidate information using AI
* Extract and understand job requirements
* Compare candidates against the job requirements
* Calculate a candidate score
* Generate an AI-powered HR review
* Rank multiple candidates
* Export the screening results to Excel

The system is designed as an **AI-assisted screening tool**, not as an autonomous hiring decision-maker. The final hiring decision should always remain with a human recruiter.

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │    Job Description  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   JD Parser Agent   │
                    └──────────┬──────────┘
                               │
                               │
┌──────────────────┐           │
│   Resume PDFs    │           │
└────────┬─────────┘           │
         │                     │
         ▼                     │
┌─────────────────────┐        │
│ Resume Parser Agent │        │
└──────────┬──────────┘        │
           │                   │
           ▼                   ▼
      ┌────────────────────────────┐
      │     Candidate + JD Data    │
      └──────────────┬─────────────┘
                     │
                     ▼
           ┌───────────────────┐
           │ Matching Agent    │
           └─────────┬─────────┘
                     │
                     ▼
           ┌───────────────────┐
           │   Scoring Agent   │
           └─────────┬─────────┘
                     │
                     ▼
           ┌───────────────────┐
           │  Reviewer Agent   │
           └─────────┬─────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │ Candidate Evaluation │
          └──────────┬───────────┘
                     │
                     ▼
              Ranked Results
                     │
                     ▼
                Excel Report
```

The workflow is orchestrated using **LangGraph**, allowing the different processing stages to operate as connected nodes while sharing application state.

---

# ✨ Key Features

## 📄 Resume Parsing

The system accepts PDF resumes and extracts relevant candidate information using an LLM.

Information includes:

* Name
* Email
* Phone number
* Skills
* Education
* Work experience
* Projects

The extracted information is returned using structured Pydantic models instead of relying on free-form LLM responses.

---

## 💼 Job Description Analysis

The recruiter can paste a job description into the application.

The JD Parser Agent identifies relevant requirements such as:

* Required skills
* Preferred skills
* Experience requirements
* Education requirements
* Other relevant qualifications

This structured information is then used during candidate matching.

---

## 🔍 Candidate-Job Matching

The Matching Agent compares the candidate's profile against the job description.

The system evaluates:

* Matching skills
* Missing skills
* Additional skills
* Required experience
* Candidate experience
* Experience gap
* Overall skill match percentage

Example:

```text
Skill Match:              82%
Required Experience:       3 years
Candidate Experience:      2 years

Matched Skills:
- Python
- SQL
- React
- Git

Missing Skills:
- Docker
- Kubernetes
```

---

## 📊 Deterministic Candidate Scoring

The project intentionally does not rely entirely on an LLM to determine the final candidate score.

The scoring stage uses deterministic application logic based on the matching results.

This makes the scoring:

* More predictable
* Reproducible
* Easier to debug
* Easier to explain to recruiters

The application produces an overall score along with a recommendation.

---

## 🧠 AI-Powered HR Review

After matching and scoring, the Reviewer Agent generates an HR-oriented assessment.

The review includes:

* Candidate summary
* Strengths
* Weaknesses
* Interview questions
* Final recommendation

The reviewer receives the structured candidate information and evaluation results rather than having to interpret the original PDF again.

---

# 🤖 Multi-Agent Architecture

Instead of using one large prompt for the entire application, the system separates responsibilities across specialized agents.

### Resume Parser Agent

Responsible for understanding and structuring information from resumes.

### Job Description Parser Agent

Responsible for converting an unstructured job description into structured requirements.

### Matching Agent

Responsible for comparing candidate information with job requirements.

### Scoring Agent

Responsible for calculating the candidate's score using deterministic logic.

### Reviewer Agent

Responsible for generating an HR-oriented evaluation based on the structured results.

This separation makes each component easier to test, debug, and improve independently.

---

# 🔄 LangGraph Workflow

LangGraph is used to orchestrate the multi-step AI workflow.

Conceptually, the workflow looks like:

```text
START
  │
  ▼
Resume Parsing
  │
  ▼
Job/Candidate Matching
  │
  ▼
Candidate Scoring
  │
  ▼
HR Review
  │
  ▼
END
```

The workflow uses shared state to pass information between different nodes.

For example:

```text
Candidate
    ↓
Match Result
    ↓
Score
    ↓
Review
```

This allows the individual agents to remain focused on their own responsibilities while LangGraph manages the overall workflow.

---

# 📁 Batch Processing

The application supports processing multiple resumes against the same job description.

Example:

```text
Job Description
      │
      ├── Resume 1
      ├── Resume 2
      ├── Resume 3
      ├── Resume 4
      └── Resume 5
```

Each candidate is processed through the screening workflow.

The results are then sorted by overall score to create a candidate ranking.

Example:

```text
Rank    Candidate       Score
--------------------------------
1       Candidate A      92
2       Candidate B      87
3       Candidate C      81
4       Candidate D      74
5       Candidate E      63
```

---

# 📥 Excel Report

The final screening results can be exported for further analysis.

The report can contain information such as:

* Candidate name
* Overall score
* Recommendation
* Matching information

This allows recruiters to retain the screening results outside the application.

---

# 🛠️ Tech Stack

### Programming Language

* Python

### AI / LLM

* OpenAI API

### Agentic AI

* LangGraph
* Specialized AI agents
* State-based workflow orchestration

### Data Validation

* Pydantic

### PDF Processing

* PyPDF

### Frontend

* Streamlit

### Data Export

* OpenPyXL

### Environment Management

* Python virtual environment
* `.env` for local API key management

### Deployment

* Streamlit Community Cloud

---

# 📂 Project Structure

```text
ResumeScreeningAgent/
│
├── agents/
│   ├── resume_parser.py
│   ├── jd_parser.py
│   ├── matching_agent.py
│   ├── scoring_agent.py
│   └── reviewer_agent.py
│
├── graph/
│   ├── state.py
│   ├── nodes.py
│   └── graph.py
│
├── models/
│   ├── candidate.py
│   ├── job_description.py
│   ├── match_result.py
│   ├── score.py
│   └── review.py
│
├── services/
│   └── pipeline.py
│
├── utils/
│   ├── pdf_reader.py
│   └── excel_export.py
│
├── uploads/
│
├── output/
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

> File names may vary slightly depending on the implementation, but the project follows a separation between UI, agents, models, workflow orchestration, services, and utilities.

---

# ⚙️ How the Application Works

## Step 1 — Upload Resumes

The recruiter uploads one or more PDF resumes.

## Step 2 — Enter Job Description

The recruiter pastes the job description into the application.

## Step 3 — Resume Processing

Each resume is converted into text and passed to the Resume Parser Agent.

## Step 4 — Structured Candidate Information

The LLM extracts the candidate's relevant information into a structured Pydantic model.

## Step 5 — Candidate Matching

The Matching Agent compares the candidate against the structured job requirements.

## Step 6 — Candidate Scoring

The scoring system calculates the candidate's overall score.

## Step 7 — HR Review

The Reviewer Agent generates a human-readable assessment.

## Step 8 — Ranking

Candidates are sorted according to their scores.

## Step 9 — Export

The recruiter can download the results as an Excel report.

---

# 🚀 Installation & Local Setup

## 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL

cd ResumeScreeningAgent
```

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
```

Never commit `.env` to GitHub.

The `.gitignore` file should contain:

```text
.env
.venv/
__pycache__/
*.pyc
uploads/
output/
```

---

## 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

# ☁️ Deployment

The application is deployed using Streamlit Community Cloud.

For deployment:

1. Push the project to GitHub.
2. Connect the repository to Streamlit Community Cloud.
3. Select `app.py` as the main application file.
4. Add the `OPENAI_API_KEY` through Streamlit Secrets.
5. Deploy the application.

The API key should never be committed to the GitHub repository.

---

# 🔐 Security Considerations

This project handles potentially sensitive candidate information, so API keys and candidate documents should be handled carefully.

### API Keys

API keys are stored through environment variables or deployment secrets.

### `.env`

The `.env` file is excluded from version control.

### Candidate Data

Uploaded resumes are processed by the application and should not be treated as permanent storage.

### Hiring Decisions

The application is intended to assist recruiters with initial screening. It should not be used as the sole basis for employment decisions.

---

# ⚠️ Limitations

This project is a portfolio/learning implementation and has several limitations.

### Resume Quality

The accuracy of extraction depends on the quality and formatting of the uploaded PDF.

### LLM Accuracy

LLMs can occasionally produce incorrect or incomplete interpretations.

### Scoring

The scoring system uses predefined application logic and may not represent every organization's hiring criteria.

### API Dependency

The application depends on the availability of the configured LLM API.

### Scalability

The current implementation is suitable for small-to-medium batch screening workloads rather than large enterprise-scale recruitment systems.

### Human Oversight

The generated recommendations should always be reviewed by a human recruiter.

---

# 🔮 Future Improvements

Possible future improvements include:

* Persistent database storage
* Authentication and user management
* Advanced ATS keyword analysis
* Resume version tracking
* Recruiter dashboards
* Custom scoring criteria for different job roles
* Background job processing for large batches
* Cloud object storage for uploaded documents
* Improved observability and logging
* Evaluation datasets for measuring extraction accuracy
* Human feedback loops for improving screening quality

---

# 🧪 Example Use Case

### Input

**Job Description**

```text
Looking for a Software Developer with 2+ years
of experience.

Required:
- Python
- SQL
- REST APIs
- Git

Preferred:
- Docker
- AWS
- React
```

**Candidate Resume**

```text
2.5 years of experience

Skills:
Python
SQL
React
Git
Docker
```

### Output

```text
Candidate Score: 89/100

Matched Skills:
Python
SQL
REST APIs
Git
React
Docker

Missing Skills:
AWS

Recommendation:
Strong candidate for interview
```

The system can perform the same evaluation across multiple uploaded resumes and rank the candidates.

---

# 🎯 Learning Outcomes

This project was built to gain practical experience with:

* LLM application development
* Prompt engineering
* Structured LLM outputs
* Pydantic
* Multi-agent architecture
* LangGraph
* Workflow orchestration
* State management
* Deterministic AI-assisted decision systems
* PDF processing
* Batch processing
* Streamlit application development
* API integration
* Cloud deployment

---

# 💡 Why This Project?

The goal was not simply to create another chatbot.

The project was designed to explore how an LLM can be combined with traditional software engineering:

```text
LLM
 +
Structured Data
 +
Deterministic Logic
 +
Specialized Agents
 +
Workflow Orchestration
 +
User Interface
 =
Practical AI Application
```

The project demonstrates how generative AI can be incorporated into a real-world workflow while keeping important business logic predictable and explainable.

---

# 👨‍💻 Author

**Aniket Nalawade**

Computer Engineering Graduate

Interested in:

* Software Development
* Artificial Intelligence
* Agentic AI
* Data Science
* Full-Stack Development

---

## ⭐ If you found this project interesting

Feel free to explore the repository, try the live demo, or use the architecture as a starting point for building your own AI-powered applications.
