#  AI Resume Screening & Candidate Ranking System

An AI-powered resume screening application that helps recruiters analyze, compare, score, and rank multiple candidates against a given job description.

The project uses **specialized AI agents, structured outputs, deterministic scoring logic, and LangGraph workflow orchestration** to automate the initial stages of the recruitment process.

## 🚀 Live Demo

**[Try the Live Application](https://resumeanalyzer-aniket.streamlit.app/)**

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
         ▼                     ▼
┌─────────────────────┐
│ Resume Parser Agent │
└──────────┬──────────┘
           │
           ▼
      ┌────────────────────────────┐
      │     Candidate + JD Data    │
      └──────────────┬─────────────┘
                     │
                     ▼
           ┌───────────────────┐
           │  Matching Agent   │
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
Experience Gap:             1 year

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

The overall workflow follows:

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

# 📥 Excel Report

The final screening results can be exported for further analysis.

The report can contain information such as:

* Candidate name
* Overall score
* Recommendation
* Matching information
* Candidate evaluation results

This allows recruiters to retain the screening results outside the application.

---

# 👥 Batch Processing

The application supports processing multiple resumes against the same job description.

Example:

```text
                    Job Description
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
       Resume 1         Resume 2         Resume 3
          │                │                │
          ▼                ▼                ▼
       Screening        Screening        Screening
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                    Candidate Ranking
```

Candidates are ranked based on their calculated scores.

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
* python-dotenv

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

> File names may vary slightly depending on the final implementation, but the project follows a separation between UI, agents, models, workflow orchestration, services, and utilities.

---

# ⚙️ How the Application Works

## Step 1 — Upload Resumes

The recruiter uploads one or more PDF resumes.

## Step 2 — Enter Job Description

The recruiter provides the job description through the Streamlit interface.

## Step 3 — Extract Resume Text

The PDF processing utility extracts text from each uploaded resume.

## Step 4 — Parse Candidate Information

The Resume Parser Agent converts the unstructured resume information into structured candidate data.

## Step 5 — Parse Job Requirements

The JD Parser Agent converts the job description into structured requirements.

## Step 6 — Match Candidate

The Matching Agent compares the candidate profile with the job requirements.

## Step 7 — Calculate Score

The Scoring Agent calculates the candidate's score based on the matching results.

## Step 8 — Generate HR Review

The Reviewer Agent generates a human-readable assessment.

## Step 9 — Rank Candidates

When multiple resumes are uploaded, candidates are ranked according to their scores.

## Step 10 — Export Results

The final screening results can be exported as an Excel report.

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

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
```

Never commit the `.env` file to GitHub.

## 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

# ☁️ Deployment

The application is deployed using **Streamlit Community Cloud**.

### Live Application

🚀 **https://resumeanalyzer-aniket.streamlit.app/**

The deployment uses Streamlit Secrets for the OpenAI API key rather than storing credentials in the repository.

---

# 🔐 Security Considerations

This project handles potentially sensitive candidate information, so API keys and candidate documents should be handled carefully.

### API Keys

API keys are stored through environment variables locally and deployment secrets in the cloud.

### `.env`

The `.env` file is excluded from version control.

### Candidate Data

Uploaded resumes are processed by the application and should not be treated as permanent storage.

### Hiring Decisions

The application is intended to assist recruiters with initial screening. It should not independently make final employment decisions.

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

# 🎓 Learning Outcomes

This project was built to gain practical experience with modern AI application development and Agentic AI.

Key areas explored:

* Large Language Model integration
* Prompt engineering
* Structured LLM outputs
* Pydantic data models
* Multi-agent architecture
* LangGraph
* Workflow orchestration
* State management
* Deterministic business logic
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

# 🎯 Project Goal

The goal of this project was to understand how **LLMs, specialized agents, structured data, deterministic logic, and workflow orchestration can be combined to solve a practical business problem.**

Rather than building a simple chatbot, the project focuses on building an end-to-end AI application with:

* Multiple specialized agents
* Structured data models
* Workflow orchestration
* Deterministic business logic
* Batch processing
* A user-facing interface
* Cloud deployment

---

# 👨‍💻 Author

## Aniket Nalawade

Computer Engineering Graduate

Interested in:

* Software Development
* Artificial Intelligence
* Agentic AI
* Data Science
* Full-Stack Development

---

# ⭐ Live Demo

🚀 **[Launch the AI Resume Screening Agent](https://resumeanalyzer-aniket.streamlit.app/)**

Feel free to explore the repository and try the live application.
