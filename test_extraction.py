
from test_emails import test_emails

expected_results = [
    {
        "name": "Multiple tasks with deadline",
        "expected_tasks": 4,
        "expected_deadline": "2026-10-09"
    },
    {
        "name": "Reply requested, no deadline",
        "expected_tasks": 1,
        "expected_deadline": None
    },
    {
        "name": "Informational email, no action",
        "expected_tasks": 0,
        "expected_deadline": None
    },
    {
        "name": "Urgent task",
        "expected_tasks": 2,
        "expected_deadline": "2026-10-05"
    }
]

print("MAILMIND EXTRACTION TEST CASES")
print("=" * 45)

for email, expected in zip(test_emails, expected_results):
    print(f"\nTest: {expected['name']}")
    print(f"Expected task count: {expected['expected_tasks']}")
    print(f"Expected deadline: {expected['expected_deadline']}")
    print("Email loaded:", bool(email["email"].strip()))

print("\nAll test cases are prepared.")