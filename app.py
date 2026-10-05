
import hashlib
import streamlit as st
from email_processor import process_email, generate_reply

# Page configuration
st.set_page_config(
    page_title="MailMind",
    page_icon="📩",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
    .main {
        background-color: #f5f7fb;
    }
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }
    h1 {
        color: #243b64;
    }
</style>
""", unsafe_allow_html=True)


def display_classification(classification):
    """Display category, urgency, and reason separately."""
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Category**")
        st.info(classification.get("category", "Other"))

    with col2:
        st.markdown("**Urgency**")
        urgency = classification.get("urgency", "Medium")

        if urgency.lower() == "high":
            st.error(f"🚨 {urgency}")
        elif urgency.lower() == "medium":
            st.warning(f"⚠️ {urgency}")
        elif urgency.lower() == "low":
            st.success(f"🟢 {urgency}")
        else:
            st.info(urgency)

    reason = classification.get("reason")
    if reason:
        st.markdown("**Reason**")
        st.write(reason)


def display_action_items(action_items, email_text):
    """Display extracted tasks as an interactive checklist."""
    st.subheader("✅ Action Items")

    if not action_items:
        st.success("No action items found. Nothing to do!")
        return

    email_id = hashlib.md5(
        email_text.encode("utf-8")
    ).hexdigest()[:12]

    completed = 0

    for index, item in enumerate(action_items):
        task = item.get("task", "Untitled task")
        deadline = item.get("deadline")

        checkbox_key = f"task_{email_id}_{index}"

        label = task
        if deadline and str(deadline).lower() != "null":
            label += f"  📅 {deadline}"

        if st.checkbox(label, key=checkbox_key):
            completed += 1

    total = len(action_items)
    st.progress(completed / total)
    st.caption(f"{completed} of {total} tasks completed")

    if completed == total:
        st.success("All tasks completed! 🎉")


def show_demo():
    """Load sample results without making an API request."""
    demo_email = """Subject: Project Report Submission – Deadline Friday

Hi Karen,

Please complete the project report for the MailMind assignment
and submit the final document by Friday, October 9.

Before submitting, make sure you:
- Review the project results and correct any errors.
- Add screenshots of the application.
- Share the GitHub repository link with the faculty coordinator.

Please confirm once the report has been submitted.

Regards,
Project Coordinator"""

    st.session_state["email"] = demo_email
    st.session_state["classification"] = {
        "category": "Work",
        "urgency": "High",
        "reason": "The sender requests several tasks and a report submission by a specified deadline."
    }
    st.session_state["analysis"] = (
        "**Summary:** Complete and submit the MailMind project report by Friday, October 9.\n\n"
        "**Sender's Intent:** Request completion and submission of the project report, "
        "including a confirmation.\n\n"
        "**Sentiment:** Neutral\n\n"
        "**Priority:** High"
    )
    st.session_state["action_items"] = [
        {
            "task": "Review project results and correct any errors",
            "deadline": "2026-10-09"
        },
        {
            "task": "Add screenshots of the application",
            "deadline": "2026-10-09"
        },
        {
            "task": "Share the GitHub repository link with the faculty coordinator",
            "deadline": "2026-10-09"
        },
        {
            "task": "Submit the final project report",
            "deadline": "2026-10-09"
        },
        {
            "task": "Confirm once the report has been submitted",
            "deadline": None
        }
    ]

    st.session_state.pop("reply", None)
    st.session_state.pop("copy_message", None)


# Header
st.title("📩 MailMind")
st.caption("Your AI-powered email intelligence assistant")
st.divider()

# Email input
st.subheader("📨 Analyze an Email")

email_text = st.text_area(
    "Paste your email here",
    height=250,
    placeholder="Paste the email content, including the subject if available..."
)

# Demo mode
if st.button("🧪 Load Demo Results"):
    show_demo()

# Analyze button
if st.button("🔍 Analyze Email", type="primary"):
    if not email_text.strip():
        st.warning("Please paste an email first.")
    else:
        with st.spinner("Analyzing, classifying, and extracting tasks..."):
            try:
                result = process_email(email_text)

                st.session_state["classification"] = result["classification"]
                st.session_state["analysis"] = result["analysis"]
                st.session_state["action_items"] = result["action_items"]
                st.session_state["email"] = email_text

                st.session_state.pop("reply", None)
                st.session_state.pop("copy_message", None)
                st.session_state.pop("api_error", None)

            except Exception as e:
                error_text = str(e)
                st.session_state["api_error"] = error_text

                if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                    st.error(
                        "Gemini API quota exceeded. Your previous results "
                        "are preserved. Please try again when your quota resets."
                    )
                elif "503" in error_text or "UNAVAILABLE" in error_text:
                    st.error(
                        "Gemini is temporarily unavailable. "
                        "Please try again later."
                    )
                else:
                    st.error(f"Analysis failed: {error_text}")


# Display results
if all(
    key in st.session_state
    for key in ["classification", "analysis", "action_items", "email"]
):
    st.divider()

    st.subheader("📂 Email Classification")
    display_classification(st.session_state["classification"])

    st.divider()

    st.subheader("📊 Email Insights")
    st.markdown(st.session_state["analysis"])

    st.divider()

    display_action_items(
        st.session_state["action_items"],
        st.session_state["email"]
    )

    st.divider()

    # Smart Reply Generator
    st.subheader("✍️ Smart Reply Generator")
    st.caption("Generate a context-aware reply based on the email's content.")

    tone = st.selectbox(
        "Choose your reply tone",
        ["Professional", "Friendly", "Formal", "Concise"]
    )

    if st.button("Generate Reply"):
        with st.spinner("Generating your reply..."):
            try:
                reply = generate_reply(
                    st.session_state["email"],
                    tone
                )
                st.session_state["reply"] = reply
                st.session_state.pop("copy_message", None)

            except Exception as e:
                error_text = str(e)

                if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                    st.error(
                        "Gemini API quota exceeded. "
                        "Reply generation is unavailable until your quota resets."
                    )
                elif "503" in error_text or "UNAVAILABLE" in error_text:
                    st.error(
                        "Gemini is temporarily unavailable. "
                        "Please try again later."
                    )
                else:
                    st.error(f"Reply generation failed: {error_text}")

    if "reply" in st.session_state:
        st.text_area(
            "Generated Reply",
            value=st.session_state["reply"],
            height=180
        )

        st.button(
            "📋 Copy reply",
            on_click=lambda: st.session_state.update(
                {"copy_message": "Select and copy the reply above using Ctrl+C."}
            )
        )

        if st.session_state.get("copy_message"):
            st.info(st.session_state["copy_message"])


# Footer
st.divider()
st.caption("MailMind | AI-powered email analysis and response generation")