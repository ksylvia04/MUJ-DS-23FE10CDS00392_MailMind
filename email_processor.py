import json
import re
from pathlib import Path

from google import genai
from config import GEMINI_API_KEY, MODEL_NAME


VALID_CATEGORIES = {
    "Work",
    "Personal",
    "Promotional",
    "Finance",
    "Support",
    "Other",
}

VALID_LEVELS = {"High", "Medium", "Low"}
VALID_SENTIMENTS = {"Positive", "Neutral", "Negative"}


def get_client():
    if not GEMINI_API_KEY:
        raise ValueError("Gemini API key not found in .env")
    return genai.Client(api_key=GEMINI_API_KEY)


def load_prompts():
    prompt_file = Path(__file__).parent / "prompts.txt"
    return prompt_file.read_text(encoding="utf-8")


def extract_json(response_text):
    """Parse JSON returned by Gemini, including fenced JSON responses."""
    text = response_text.strip()

    # Remove optional Markdown code fences
    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(r"\s*```$", "", text)

    return json.loads(text)


def normalize_deadline(deadline):
    """Keep deadlines predictable for the Streamlit UI."""
    if deadline is None:
        return None

    deadline = str(deadline).strip()

    if not deadline:
        return None

    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", deadline):
        return deadline

    return deadline


def process_email(email_text):
    """
    Classify, analyze, and extract action items from an email
    using a single Gemini API request.
    """
    if not email_text or not email_text.strip():
        raise ValueError("Please enter an email before analyzing.")

    client = get_client()
    prompts = load_prompts()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=f"""
{prompts}

Analyze the email below and return ONLY a valid JSON object.
Do not include Markdown or text outside the JSON.

Use this exact structure:

{{
    "category": "Work",
    "urgency": "Medium",
    "classification_reason": "Brief explanation",
    "summary": "Concise email summary",
    "sender_intent": "What the sender wants",
    "sentiment": "Neutral",
    "priority": "Medium",
    "action_items": [
        {{
            "task": "Specific action to take",
            "deadline": "YYYY-MM-DD or null"
        }}
    ]
}}

Rules:

- Category must be exactly one of:
  Work, Personal, Promotional, Finance, Support, Other.

- Urgency and priority must each be:
  High, Medium, or Low.

- Sentiment must be:
  Positive, Neutral, or Negative.

- Extract only actions that the recipient is actually
  expected to take.

- Include a task for replying or confirming only when
  the email explicitly requests it.

- Do not invent tasks, deadlines, commitments, or dates.

- Use null for a deadline when none is explicitly stated.

- Convert a clearly stated date into YYYY-MM-DD only when
  the year and date can be determined confidently.

- If the email says "today", "tomorrow", or another
  relative date and the exact calendar date cannot be
  determined confidently, use null rather than guessing.

- If there are no action items, return an empty list.

- Keep summaries, explanations, and tasks concise.

Email:
{email_text}
"""
    )

    try:
        result = extract_json(response.text)
    except (json.JSONDecodeError, TypeError, AttributeError) as e:
        raise ValueError(
            "Gemini returned an unexpected response. Please try again."
        ) from e

    if not isinstance(result, dict):
        raise ValueError(
            "Gemini returned an invalid response structure."
        )

    # -----------------------------
    # Validate classification
    # -----------------------------

    category = result.get("category", "Other")
    if category not in VALID_CATEGORIES:
        category = "Other"

    urgency = result.get("urgency", "Medium")
    if urgency not in VALID_LEVELS:
        urgency = "Medium"

    priority = result.get("priority", "Medium")
    if priority not in VALID_LEVELS:
        priority = "Medium"

    sentiment = result.get("sentiment", "Neutral")
    if sentiment not in VALID_SENTIMENTS:
        sentiment = "Neutral"

    reason = str(
        result.get(
            "classification_reason",
            "No reason provided."
        )
    ).strip()

    # -----------------------------
    # Normalize action items
    # -----------------------------

    action_items = result.get("action_items", [])

    if not isinstance(action_items, list):
        action_items = []

    normalized_items = []

    for item in action_items:
        if not isinstance(item, dict):
            continue

        task = item.get("task")

        if not task:
            continue

        normalized_items.append({
            "task": str(task).strip(),
            "deadline": normalize_deadline(
                item.get("deadline")
            )
        })

    # -----------------------------
    # Build application structure
    # -----------------------------

    classification = {
        "category": category,
        "urgency": urgency,
        "reason": reason,
    }

    summary = str(
        result.get("summary", "Not available")
    ).strip()

    sender_intent = str(
        result.get("sender_intent", "Not available")
    ).strip()

    analysis = f"""
**Summary:** {summary}

**Sender's Intent:** {sender_intent}

**Sentiment:** {sentiment}

**Priority:** {priority}
""".strip()

    return {
        "classification": classification,
        "analysis": analysis,
        "action_items": normalized_items,
    }


def classify_email(email_text):
    """
    Compatibility function for standalone classification.

    Note:
    This performs a complete Gemini analysis and therefore
    consumes one API request.
    """
    return process_email(email_text)["classification"]


def analyze_email(email_text):
    """
    Compatibility function for standalone analysis.

    Note:
    This performs a complete Gemini analysis and therefore
    consumes one API request.
    """
    return process_email(email_text)["analysis"]


def generate_reply(email_text, tone="Professional"):
    """Generate a context-aware email reply."""
    if not email_text or not email_text.strip():
        raise ValueError("Please enter an email before generating a reply.")

    client = get_client()
    prompts = load_prompts()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=f"""
{prompts}

Write a suitable email reply to the following email.

Tone: {tone}

Instructions:

- Keep the reply concise, relevant, and natural.
- Consider the sender's intent and the email's context.
- Do not invent commitments, facts, dates, or promises.
- If essential information is missing, use a placeholder
  rather than making assumptions.
- Return only the reply draft.

Email:
{email_text}
"""
    )

    return response.text.strip()