test_emails = [
    {
        "name": "Multiple tasks with deadline",
        "email": """Subject: Report due Friday

Hi Karen,

Please review the project results, correct any errors,
and submit the final report by Friday, October 9.

Also, share the GitHub link with the coordinator.

Regards,
Professor"""
    },
    {
        "name": "Reply requested, no deadline",
        "email": """Subject: Meeting confirmation

Hi Karen,

Could you please confirm whether you can attend
the project meeting next week?

Thanks,
Alex"""
    },
    {
        "name": "Informational email, no action",
        "email": """Subject: Application update

Hi Karen,

Thank you for applying. We have received your
application and will contact you if there are updates.

Regards,
Recruitment Team"""
    },
    {
        "name": "Urgent task",
        "email": """Subject: Urgent: Submit the form today

Hi Karen,

Please complete and submit the attached form today
before 5 PM. Reply to this email once it is done.

Regards,
Team Lead"""
    }
]

for index, test in enumerate(test_emails, start=1):
    print(f"\nTEST {index}: {test['name']}")
    print(test["email"])
    print("-" * 50)