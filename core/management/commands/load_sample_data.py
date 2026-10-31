import os
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.base import ContentFile
from accounts.models import UserProfile
from opportunities.models import Company, Opportunity
from applications.models import Application, ApplicationStatusHistory, ApplicationNote
from interviews.models import Interview, InterviewChecklistItem
from reminders.models import Reminder
from documents.models import Document
from planner.models import CareerTask, CareerGoal


class Command(BaseCommand):
    help = "Loads realistic sample demonstration data for CareerPilot or clears it."

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Safely remove demonstration data created for demo_user',
        )
        parser.add_argument(
            '--username',
            type=str,
            default='demo_user',
            help='Username to attach sample demonstration data to (default: demo_user)',
        )

    def handle(self, *args, **options):
        username = options['username']
        clear_only = options['clear']

        try:
            demo_user = User.objects.get(username=username)
        except User.DoesNotExist:
            if clear_only:
                self.stdout.write(self.style.WARNING(f"User '{username}' does not exist. Nothing to clear."))
                return
            demo_user = User.objects.create_user(
                username=username,
                email='demo.candidate@careerpilot.local',
                password='DemoPassword123!',
                first_name='Ragu',
                last_name='Ram'
            )
            self.stdout.write(self.style.SUCCESS(f"Created demo user '{username}' (Password: DemoPassword123!)"))

        if clear_only:
            self.stdout.write(f"Clearing demonstration records for user '{username}'...")
            Application.objects.filter(user=demo_user).delete()
            Opportunity.objects.filter(user=demo_user).delete()
            Company.objects.filter(user=demo_user).delete()
            Interview.objects.filter(user=demo_user).delete()
            Reminder.objects.filter(user=demo_user).delete()
            Document.objects.filter(user=demo_user).delete()
            CareerTask.objects.filter(user=demo_user).delete()
            CareerGoal.objects.filter(user=demo_user).delete()
            self.stdout.write(self.style.SUCCESS("Demonstration data cleared successfully."))
            return

        self.stdout.write("Populating comprehensive demonstration career workspace...")

        # 1. Update Profile
        profile, _ = UserProfile.objects.get_or_create(user=demo_user)
        profile.headline = "Final-Year B.Tech AI & Data Science | Full-Stack & Python Developer"
        profile.phone = "+91 98401 23456"
        profile.location = "Bengaluru / Chennai, India"
        profile.preferred_roles = "Software Engineer, AI Engineer, Backend Python Developer, Data Analyst"
        profile.preferred_locations = "Bengaluru, Hyderabad, Chennai, Remote"
        profile.preferred_employment_types = "Full-time"
        profile.preferred_work_modes = "Hybrid"
        profile.expected_salary = "8,00,000 - 14,00,000 INR"
        profile.preferred_industries = "FinTech, SaaS, AI/ML, Cloud Infrastructure"
        profile.skill_profile = "Python, Django, FastAPI, PostgreSQL, PyTorch, Scikit-learn, React, Docker, Git"
        profile.career_goals = "Secure a high-impact full-time Software Engineer role in a product engineering team. Target 3 offers before graduation."
        profile.follow_up_default_days = 7
        profile.save()

        today = timezone.now().date()

        # 2. Documents
        dummy_pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Title (CareerPilot Sample Resume) >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"
        
        doc_sde, _ = Document.objects.get_or_create(
            user=demo_user,
            title="Ragu_Ram_SDE_Core_Resume_2026.pdf",
            defaults={
                'document_type': 'Resume',
                'resume_category': 'Software Engineer',
                'description': 'Targeted for Backend Python, Django, System Design, and Algorithms roles.',
                'file_size': len(dummy_pdf_content),
            }
        )
        if not doc_sde.file:
            doc_sde.file.save("Ragu_Ram_SDE_Core_Resume_2026.pdf", ContentFile(dummy_pdf_content), save=True)

        doc_ai, _ = Document.objects.get_or_create(
            user=demo_user,
            title="Ragu_Ram_AI_DataScience_Resume_2026.pdf",
            defaults={
                'document_type': 'Resume',
                'resume_category': 'Data Analyst',
                'description': 'Tailored for Applied ML, NLP, Feature Engineering, and Analytics roles.',
                'file_size': len(dummy_pdf_content),
            }
        )
        if not doc_ai.file:
            doc_ai.file.save("Ragu_Ram_AI_DataScience_Resume_2026.pdf", ContentFile(dummy_pdf_content), save=True)

        doc_cert, _ = Document.objects.get_or_create(
            user=demo_user,
            title="AWS_Cloud_Practitioner_Certificate.pdf",
            defaults={
                'document_type': 'Certificate',
                'resume_category': 'None',
                'description': 'Official AWS Certified Cloud Practitioner verification credential.',
                'file_size': len(dummy_pdf_content),
            }
        )
        if not doc_cert.file:
            doc_cert.file.save("AWS_Cloud_Practitioner_Certificate.pdf", ContentFile(dummy_pdf_content), save=True)

        # 3. Companies & Opportunities
        companies_data = [
            ("Razorpay", "https://razorpay.com/careers", "Bengaluru, India", "Leading payments infrastructure and financial platform."),
            ("Zoho Corporation", "https://www.zoho.com/careers", "Chennai, India", "Global cloud SaaS suite enterprise applications."),
            ("Atlassian", "https://www.atlassian.com/company/careers", "Bengaluru, India (Remote)", "Team collaboration and productivity software leader."),
            ("Google India", "https://careers.google.com", "Bengaluru / Hyderabad", "Global tech leader in search, cloud, and AI solutions."),
            ("Microsoft IDC", "https://careers.microsoft.com", "Hyderabad, India", "India Development Center for enterprise cloud & productivity."),
            ("Swiggy", "https://careers.swiggy.com", "Bengaluru, India", "On-demand hyper-local consumer delivery and marketplace."),
            ("CRED", "https://cred.club/careers", "Bengaluru, India", "High-trust community fintech platform for creditworthy individuals."),
        ]

        companies = {}
        for cname, cweb, cloc, cdesc in companies_data:
            comp, _ = Company.objects.get_or_create(
                user=demo_user,
                name=cname,
                defaults={'website': cweb, 'location': cloc, 'description': cdesc}
            )
            companies[cname] = comp

        opportunities_data = [
            {
                'company': companies['Razorpay'],
                'title': 'Associate Software Engineer (Backend)',
                'category': 'Software Engineering',
                'employment_type': 'Full-time',
                'classification': 'Full-time',
                'work_mode': 'Hybrid',
                'location': 'Bengaluru',
                'salary_min': 1000000,
                'salary_max': 1400000,
                'required_skills': 'Python, Django, PostgreSQL, Redis, REST APIs, Microservices',
                'source': 'LinkedIn',
                'priority': 'High',
                'deadline': today + timedelta(days=2),
                'interest_status': 'Interested',
                'application_url': 'https://razorpay.com/careers/backend-ase'
            },
            {
                'company': companies['Zoho Corporation'],
                'title': 'Member Technical Staff — AI & Analytics',
                'category': 'AI & Machine Learning',
                'employment_type': 'Full-time',
                'classification': 'Full-time',
                'work_mode': 'On-site',
                'location': 'Chennai',
                'salary_min': 850000,
                'salary_max': 1200000,
                'required_skills': 'Python, PyTorch, Scikit-learn, SQL, Data Structures',
                'source': 'College placement cell',
                'priority': 'High',
                'deadline': today + timedelta(days=12),
                'interest_status': 'Interested',
                'application_url': 'https://careers.zohocorp.com/mts-ai'
            },
            {
                'company': companies['Atlassian'],
                'title': 'Graduate Software Engineer — Cloud Foundations',
                'category': 'Full Stack Development',
                'employment_type': 'Full-time',
                'classification': 'Full-time',
                'work_mode': 'Remote',
                'location': 'Bengaluru / Remote',
                'salary_min': 1400000,
                'salary_max': 1800000,
                'required_skills': 'Java/Python, React, TypeScript, Distributed Systems',
                'source': 'Referral',
                'priority': 'Urgent',
                'deadline': today - timedelta(days=15),
                'interest_status': 'Interested',
                'application_url': 'https://www.atlassian.com/careers/grad-cloud'
            },
            {
                'company': companies['Google India'],
                'title': 'Software Engineering Intern — Summer 2027',
                'category': 'Software Engineering',
                'employment_type': 'Internship',
                'classification': 'Internship',
                'work_mode': 'Hybrid',
                'location': 'Bengaluru',
                'salary_min': 90000,
                'salary_max': 110000,
                'required_skills': 'C++, Python, Algorithms, Problem Solving',
                'source': 'Company website',
                'priority': 'Urgent',
                'deadline': today + timedelta(days=1),
                'interest_status': 'Saved',
                'application_url': 'https://careers.google.com/jobs/results/intern-swe'
            },
            {
                'company': companies['Microsoft IDC'],
                'title': 'Data Scientist — Cloud Intelligence',
                'category': 'Data Analytics & BI',
                'employment_type': 'Full-time',
                'classification': 'Full-time',
                'work_mode': 'Hybrid',
                'location': 'Hyderabad',
                'salary_min': 1300000,
                'salary_max': 1700000,
                'required_skills': 'Python, SQL, Azure ML, Statistical Modeling, Power BI',
                'source': 'Indeed',
                'priority': 'Medium',
                'deadline': today + timedelta(days=20),
                'interest_status': 'Saved',
                'application_url': 'https://careers.microsoft.com/ds-cloud'
            },
            {
                'company': companies['Swiggy'],
                'title': 'Associate SDE — Logistics Platform',
                'category': 'Software Engineering',
                'employment_type': 'Full-time',
                'classification': 'Full-time',
                'work_mode': 'On-site',
                'location': 'Bengaluru',
                'salary_min': 950000,
                'salary_max': 1300000,
                'required_skills': 'Golang/Python, MySQL, Docker, Kafka, High Concurrency',
                'source': 'Naukri',
                'priority': 'High',
                'deadline': today - timedelta(days=25),
                'interest_status': 'Interested',
                'application_url': 'https://swiggy.hire.com/asde-logistics'
            },
            {
                'company': companies['CRED'],
                'title': 'Backend Developer Intern',
                'category': 'Full Stack Development',
                'employment_type': 'Internship',
                'classification': 'Internship',
                'work_mode': 'On-site',
                'location': 'Bengaluru',
                'salary_min': 80000,
                'salary_max': 100000,
                'required_skills': 'Python, Django, AWS, Event-driven architecture',
                'source': 'LinkedIn',
                'priority': 'Medium',
                'deadline': today + timedelta(days=5),
                'interest_status': 'Saved',
                'application_url': 'https://cred.club/careers/intern'
            }
        ]

        created_opps = {}
        for o_data in opportunities_data:
            opp, _ = Opportunity.objects.get_or_create(
                user=demo_user,
                company=o_data['company'],
                title=o_data['title'],
                defaults=o_data
            )
            created_opps[o_data['company'].name] = opp

        # 4. Applications across stages
        # Razorpay -> Technical Interview
        app_razorpay, _ = Application.objects.get_or_create(
            user=demo_user,
            opportunity=created_opps['Razorpay'],
            defaults={
                'status': 'Technical Interview',
                'application_date': today - timedelta(days=14),
                'application_method': 'Company Portal',
                'submitted_resume': doc_sde,
                'expected_salary': 1200000,
                'recruiter_name': 'Priya Sharma',
                'recruiter_email': 'priya.sharma@razorpay.com',
                'follow_up_date': today + timedelta(days=1),
                'notes': 'Passed online assessment on HackerRank (Score: 100%). Round 1 System Design & Problem Solving.'
            }
        )
        ApplicationStatusHistory.objects.get_or_create(
            application=app_razorpay,
            previous_status='Applied',
            new_status='Assessment',
            defaults={'notes': 'Invited to HackerRank online coding test.'}
        )
        ApplicationStatusHistory.objects.get_or_create(
            application=app_razorpay,
            previous_status='Assessment',
            new_status='Technical Interview',
            defaults={'notes': 'Cleared coding assessment. Shortlisted for Technical Round 1.'}
        )

        # Zoho -> Assessment
        app_zoho, _ = Application.objects.get_or_create(
            user=demo_user,
            opportunity=created_opps['Zoho Corporation'],
            defaults={
                'status': 'Assessment',
                'application_date': today - timedelta(days=8),
                'application_method': 'College Placement Cell',
                'submitted_resume': doc_ai,
                'expected_salary': 950000,
                'recruiter_name': 'Karthik Raja (Placement Officer)',
                'follow_up_date': today - timedelta(days=1),  # overdue follow-up demo
                'notes': 'Campus placement test scheduled for upcoming weekend.'
            }
        )

        # Atlassian -> Offer Received!
        app_atlassian, _ = Application.objects.get_or_create(
            user=demo_user,
            opportunity=created_opps['Atlassian'],
            defaults={
                'status': 'Offer Received',
                'application_date': today - timedelta(days=35),
                'application_method': 'Referral',
                'submitted_resume': doc_sde,
                'referral_name': 'Siddharth Rao (Senior SDE)',
                'expected_salary': 1500000,
                'offered_salary': 1650000,
                'notes': 'Completed all 3 rounds. Official written offer letter received with joining in July.'
            }
        )
        ApplicationStatusHistory.objects.get_or_create(
            application=app_atlassian,
            previous_status='HR Interview',
            new_status='Offer Received',
            defaults={'notes': 'Verbal offer confirmed by HR. Official letter uploaded.'}
        )

        # Swiggy -> Rejected
        app_swiggy, _ = Application.objects.get_or_create(
            user=demo_user,
            opportunity=created_opps['Swiggy'],
            defaults={
                'status': 'Rejected',
                'application_date': today - timedelta(days=28),
                'application_method': 'Naukri FastForward',
                'submitted_resume': doc_sde,
                'rejection_reason': 'Role filled internally; recruiter suggested reapplying in 6 months for Core Platform.',
                'notes': 'Good experience with dynamic programming round, need to practice concurrency.'
            }
        )

        # 5. Interviews
        # Razorpay upcoming interview (tomorrow)
        int_razorpay, _ = Interview.objects.get_or_create(
            user=demo_user,
            application=app_razorpay,
            round_number=1,
            defaults={
                'round_title': 'Round 1: Problem Solving & System Architecture',
                'interview_date': today + timedelta(days=1),
                'interview_time': timezone.now().time().replace(hour=14, minute=30, second=0),
                'mode': 'Online',
                'meeting_url': 'https://meet.google.com/rzp-tech-round1',
                'interviewer_names': 'Aravind Venkat',
                'interviewer_titles': 'Lead Architect — Merchant Core',
                'preparation_notes': 'Focus on idempotency, database indexing, caching strategies, and payment webhook guarantees.',
                'topics_to_prepare': 'PostgreSQL ACID, Distributed Locks, B-Trees, Python generators, REST architecture',
                'outcome': 'Scheduled',
            }
        )
        # Seed checklist
        for item in InterviewChecklistItem.DEFAULT_ITEMS:
            InterviewChecklistItem.objects.get_or_create(
                interview=int_razorpay,
                item_text=item,
                defaults={'is_completed': False}
            )

        # Atlassian past interview review
        int_atlassian, _ = Interview.objects.get_or_create(
            user=demo_user,
            application=app_atlassian,
            round_number=2,
            defaults={
                'round_title': 'Round 2: Systems & Coding Bar Raiser',
                'interview_date': today - timedelta(days=10),
                'mode': 'Online',
                'meeting_url': 'https://zoom.us/j/atlassian-round2',
                'interviewer_names': 'Elena Woods',
                'interviewer_titles': 'Principal Staff Engineer',
                'outcome': 'Passed',
                'feedback': 'Excellent problem structuring, articulate thought process, strong test-case considerations.',
                'questions_asked': '1. Design an in-memory rate limiter supporting rolling window counters.\n2. Explain trade-offs between Redis Lua script vs token bucket with atomic increments.',
                'topics_covered': 'Concurrency, Token Bucket, Sliding Window, Redis, Unit Testing',
                'personal_answers': 'Implemented sliding window log approach using sorted sets (ZADD/ZREMRANGEBYSCORE), discussed time complexity O(log N + M) and memory mitigation.',
                'areas_to_improve': 'Explore thread-safe local lock alternatives for zero-network latency caches.'
            }
        )

        # 6. Reminders
        reminders_data = [
            ("Send polite follow-up to Zoho Placement Coordinator", "Assessment deadline", today - timedelta(days=1), "High", False, app_zoho),
            ("Check Razorpay technical meeting link & audio test", "Interview reminder", today + timedelta(days=1), "Urgent", False, app_razorpay),
            ("Review Google Software Engineer Intern job description", "Job application deadline", today, "High", False, None),
            ("Submit signed offer acceptance for Atlassian", "Document submission", today + timedelta(days=5), "Medium", False, app_atlassian),
            ("Practice 2 Hard Graph Questions on LeetCode", "Custom reminder", today, "Medium", True, None),
        ]

        for title, rtype, ddate, prio, is_comp, rel_app in reminders_data:
            Reminder.objects.get_or_create(
                user=demo_user,
                title=title,
                defaults={
                    'reminder_type': rtype,
                    'due_date': ddate,
                    'priority': prio,
                    'is_completed': is_comp,
                    'application': rel_app,
                    'opportunity': rel_app.opportunity if rel_app else None,
                    'completed_at': timezone.now() if is_comp else None
                }
            )

        # 7. Career Tasks
        tasks_data = [
            ("Solve 3 Dynamic Programming problems on LeetCode", "Skill Development", "High", today, True),
            ("Revise Database Indexing & Query Execution Plans in PostgreSQL", "Interview Preparation", "Urgent", today, False),
            ("Tailor resume for Google Software Engineer Summer Internship", "Resume Improvement", "High", today, False),
            ("Reach out to 2 alumni at Microsoft IDC on LinkedIn", "Job Search", "Medium", today + timedelta(days=1), False),
            ("Review Razorpay system design architecture notes", "Interview Preparation", "Urgent", today, False),
            ("Completed mock technical interview with peer", "Interview Preparation", "Medium", today - timedelta(days=2), True),
        ]

        for t_title, t_cat, t_prio, t_due, t_comp in tasks_data:
            CareerTask.objects.get_or_create(
                user=demo_user,
                title=t_title,
                defaults={
                    'category': t_cat,
                    'priority': t_prio,
                    'due_date': t_due,
                    'is_completed': t_comp,
                    'completed_at': timezone.now() if t_comp else None
                }
            )

        # 8. Career Goals
        CareerGoal.objects.get_or_create(
            user=demo_user,
            title="Submit 5 Targeted SDE & AI Applications",
            defaults={
                'goal_type': 'Weekly',
                'category': 'Applications',
                'target_count': 5,
                'period_start_date': today - timedelta(days=4),
                'period_end_date': today + timedelta(days=3),
                'notes': 'Focus on high-growth tier-1 tech and product engineering companies.'
            }
        )
        CareerGoal.objects.get_or_create(
            user=demo_user,
            title="Complete 3 In-depth Technical Interview Sessions",
            defaults={
                'goal_type': 'Weekly',
                'category': 'Interview Prep',
                'target_count': 3,
                'period_start_date': today - timedelta(days=4),
                'period_end_date': today + timedelta(days=3),
                'notes': 'Includes real rounds and peer mock simulations.'
            }
        )
        CareerGoal.objects.get_or_create(
            user=demo_user,
            title="Solve 10 LeetCode Medium/Hard Coding Problems",
            defaults={
                'goal_type': 'Weekly',
                'category': 'Learning',
                'target_count': 10,
                'period_start_date': today - timedelta(days=4),
                'period_end_date': today + timedelta(days=3),
                'notes': 'Graphs, Trees, DP, and SQL optimization.'
            }
        )

        # Ensure admin superuser exists
        admin_user, admin_created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@careerpilot.local',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if admin_created or not admin_user.is_superuser:
            admin_user.set_password('AdminPassword123!')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()

        self.stdout.write(self.style.SUCCESS("Demo career workspace populated with realistic records!"))
        self.stdout.write(self.style.SUCCESS(f"Demo Credentials -> Username: {username} | Password: DemoPassword123!"))
        self.stdout.write(self.style.SUCCESS("Admin Credentials -> Username: admin | Password: AdminPassword123!"))
