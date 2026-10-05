def check_tasks(tasks, expected_count):
    assert len(tasks) == expected_count, (
        f"Expected {expected_count} tasks, got {len(tasks)}"
    )

    for task in tasks:
        assert isinstance(task, dict)
        assert task.get("task"), "Task description is missing"
        assert "deadline" in task, "Deadline field is missing"


sample_results = [
    {
        "name": "Multiple tasks",
        "tasks": [
            {"task": "Review project results", "deadline": "2026-10-09"},
            {"task": "Correct errors", "deadline": "2026-10-09"},
            {"task": "Submit report", "deadline": "2026-10-09"},
            {"task": "Share GitHub link", "deadline": "2026-10-09"},
        ],
        "expected": 4
    },
    {
        "name": "Reply requested",
        "tasks": [
            {"task": "Confirm meeting attendance", "deadline": None}
        ],
        "expected": 1
    },
    {
        "name": "No action required",
        "tasks": [],
        "expected": 0
    },
    {
        "name": "Urgent task",
        "tasks": [
            {"task": "Complete the form", "deadline": "2026-10-05"},
            {"task": "Submit the form and reply", "deadline": "2026-10-05"}
        ],
        "expected": 2
    }
]

for result in sample_results:
    check_tasks(result["tasks"], result["expected"])
    print(f"PASS: {result['name']}")

print("\nAll local checklist tests passed!")