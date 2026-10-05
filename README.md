# MailMind

MailMind is an AI-powered email intelligence application that helps users understand, prioritize, and respond to emails more efficiently.

The application uses the Google Gemini API and Large Language Models (LLMs) to analyze email content and provide structured insights such as category, urgency, summary, sender intent, sentiment, priority, and actionable tasks. It also generates context-aware email replies based on the user's preferred tone.

## Project Overview

Managing emails manually can make it difficult to identify which messages require immediate attention and what actions need to be taken.

MailMind addresses this by applying Natural Language Processing (NLP) and LLM-based analysis to convert unstructured email content into structured, actionable information.

Given an email, MailMind can:

- Classify the email into a relevant category
- Determine its urgency and priority
- Summarize the message
- Identify the sender's intent
- Detect sentiment
- Extract actionable tasks
- Identify explicitly stated deadlines
- Track completion of extracted tasks
- Generate a context-aware reply

The application is built as a lightweight Streamlit web application with Gemini providing the LLM capabilities for natural language understanding and generation.

## Features

### 1. Email Classification

Emails are automatically classified into one of the following categories:

- Work
- Personal
- Promotional
- Finance
- Support
- Other

The application also assigns an urgency level:

- High
- Medium
- Low

A short explanation is provided for the classification.

### 2. Email Analysis

MailMind extracts useful information from the email, including:

- Concise summary
- Sender's intent
- Sentiment
- Priority

### 3. Action Item Extraction

MailMind identifies actions that the recipient is actually expected to perform.

Each action item can include:

- Task description
- Explicit deadline

The application avoids inventing tasks or deadlines that are not supported by the email.

### 4. Task Progress Tracking

Extracted action items are displayed as an interactive checklist.

Users can mark completed tasks and view their progress.

For example:

```text
2 of 5 tasks completed
████████░░░░░░░░
```

### 5. Smart Reply

MailMind can generate a context-aware email reply.

The user can select a preferred tone, such as:

- Professional
- Friendly
- Concise

The generated response is designed to remain relevant to the original email without inventing commitments or facts.

### 6. Demo Mode

A built-in demo mode allows the application to display sample analysis results without making a Gemini API request.

This is useful for:

- Demonstrations
- UI testing
- Presentations
- Testing when API quota is unavailable

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and NLP processing |
| Natural Language Processing (NLP) | Email understanding, classification, sentiment and intent analysis |
| Large Language Model (LLM) | Gemini-powered email analysis and response generation |
| Google Gemini API | LLM inference for email analysis and Smart Reply |
| Streamlit | Interactive web interface |
| `google-genai` | Gemini API integration |
| `python-dotenv` | Secure environment variable management |
| JSON | Structured LLM output and data processing |
| Regular Expressions | Response parsing and validation |
| Git & GitHub | Version control and project submission |

## How It Works

MailMind follows this workflow:

```text
User enters email
        ↓
Streamlit interface
        ↓
Email processing module
        ↓
Gemini API / LLM
        ↓
Structured JSON response
        ↓
Validation & normalization
        ↓
Classification + Analysis + Action Items
        ↓
Interactive Streamlit dashboard
```

For Smart Reply:

```text
Original Email
      ↓
Selected Tone
      ↓
Gemini API
      ↓
Generated Reply
      ↓
User reviews and copies the draft
```

## How to Run

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd MailMind
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_api_key_here
```

Do not commit the `.env` file to GitHub.

### 5. Start the Application

From the main MailMind project directory:

```bash
streamlit run app.py
```

The application will open through the local Streamlit URL provided in the terminal.

## Gemini API Setup

MailMind uses Google's Gemini API as the LLM backend for email analysis and reply generation.

### API Key Configuration

Add your Gemini API key to the `.env` file:

```text
GEMINI_API_KEY=your_api_key_here
```

The application loads the API key through environment variables rather than storing it directly in the source code.

The API key should never be committed to GitHub.

## Project Structure

```text
MailMind/
│
├── app.py
│       Main Streamlit application and user interface
│
├── email_processor.py
│       Gemini API integration, email analysis,
│       JSON processing, validation, and reply generation
│
├── config.py
│       Application configuration and environment variables
│
├── prompts.txt
│       Prompt instructions used by the LLM-powered
│       email analysis workflow
│
├── requirements.txt
│       Python dependencies
│
├── test_emails.py
│       Sample email test cases
│
├── test_extraction.py
│       Action-item extraction test plan
│
├── test_checklist.py
│       Local validation tests
│
├── .env
│       Local Gemini API key
│       NOT committed to GitHub
│
├── .gitignore
│       Files excluded from version control
│
└── README.md
        Project documentation
```

## Sample Workflow

### Example Input

```text
Hi Karen,

Please review the project report and correct the formatting issues
before submitting the final version.

Please upload the final report by October 9 and share the submission
link with the team.

Thanks.
```

### MailMind Output

```text
Category: Work
Urgency: High

Summary:
The sender asks the recipient to review and correct a project report,
submit the final version, and share the submission link.

Sender's Intent:
The sender wants the recipient to complete and submit the report.

Sentiment:
Neutral

Priority:
High
```

### Extracted Action Items

```text
☐ Review and correct the project report
☐ Submit the final report
☐ Share the submission link with the team
```

Explicit deadlines are associated with the relevant action items when they are present in the email.

### Smart Reply

The user can select a tone and generate a reply based on the original email.

Example:

```text
Hi,

Thanks for the update. I'll review and correct the report, submit the
final version, and share the submission link by the requested deadline.

Best,
Karen
```

## Validation and Error Handling

MailMind validates the LLM response before displaying it.

The application checks:

- Valid JSON structure
- Valid email category
- Valid urgency level
- Valid priority level
- Valid sentiment value
- Valid action-item structure
- Deadline formatting

The application also handles common Gemini API availability and quota errors gracefully.

## API Usage

Email analysis is designed to use a single Gemini request for:

```text
Classification
+
Analysis
+
Action Item Extraction
```

Smart Reply uses a separate Gemini request.

Demo Mode does not make API requests.

## Security

Sensitive configuration is stored locally in `.env`.

The repository excludes:

```text
.env
venv/
__pycache__/
*.pyc
```

The Gemini API key should never be committed to source control.

## Future Improvements

Potential future enhancements include:

- Gmail API integration
- Outlook integration
- Persistent task storage
- Email history and search
- Calendar integration for deadlines
- Automatic reminder notifications
- Batch email processing
- User authentication
- Improved deadline normalization
- Email analytics dashboard

## Author

**Karen Sylvia Vasmalla**

B.Tech Computer Science & Engineering — Data Science  
Manipal University Jaipur