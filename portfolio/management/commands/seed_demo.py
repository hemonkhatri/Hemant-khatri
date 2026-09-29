"""Fill the database with sample content: `python manage.py seed_demo`."""
import datetime

from django.core.management.base import BaseCommand

from portfolio.models import Education, Experience, Profile, Project, Skill


class Command(BaseCommand):
    help = "Create sample profile, skills, projects and experience for local testing."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing portfolio content before seeding.",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            for model in (Skill, Project, Experience, Education, Profile):
                model.objects.all().delete()
            self.stdout.write("Cleared existing content.")

        profile, created = Profile.objects.get_or_create(
            defaults={
                "full_name": "Aarav Shrestha",
                "headline": "Django developer building web tools in Kathmandu",
                "bio": (
                    "I build the parts of a product people don't see: data models, "
                    "APIs, background jobs, and the admin screens a team actually "
                    "uses every day.\n\n"
                    "Most of my work is Django and Postgres. I like problems where "
                    "the hard part is getting the data right, and I care about "
                    "software that keeps working after the person who wrote it "
                    "has moved on."
                ),
                "location": "Kathmandu, Nepal",
                "email": "hello@example.com",
                "phone": "+977 98XXXXXXXX",
                "github_url": "https://github.com/",
                "linkedin_url": "https://linkedin.com/in/",
                "open_to_work": True,
            },
            id=1,
        )
        self.stdout.write("Profile created." if created else "Profile already existed.")

        skills = [
            ("Python", "language", 92, 1),
            ("JavaScript", "language", 74, 2),
            ("SQL", "language", 80, 3),
            ("Django", "framework", 90, 4),
            ("Django REST Framework", "framework", 82, 5),
            ("Tailwind CSS", "framework", 68, 6),
            ("PostgreSQL", "database", 84, 7),
            ("Redis", "database", 62, 8),
            ("Docker", "tool", 72, 9),
            ("Git", "tool", 88, 10),
            ("Linux", "tool", 76, 11),
        ]
        for name, category, level, order in skills:
            Skill.objects.get_or_create(
                name=name,
                defaults={"category": category, "proficiency": level, "order": order},
            )

        projects = [
            {
                "title": "Sajilo Khaja",
                "summary": "Order management for a cloud kitchen running six menus at once.",
                "description": (
                    "A kitchen was tracking orders across three notebooks and a "
                    "WhatsApp group. This replaced all of it.\n\n"
                    "Orders arrive from a public menu page, get routed to the right "
                    "prep station by item type, and close out on a tablet in the "
                    "kitchen. Nightly reports go to the owner by email.\n\n"
                    "The hard part was stock: ingredients are shared across menus, "
                    "so a sold-out item has to disappear from four pages at once. "
                    "That runs as a signal on order save, guarded by a database "
                    "transaction so two simultaneous orders can't oversell."
                ),
                "tech_stack": "Django, PostgreSQL, Celery, Redis, HTMX",
                "role": "Solo build",
                "is_featured": True,
                "completed_on": datetime.date(2025, 11, 4),
                "order": 1,
            },
            {
                "title": "Trekking permit checker",
                "summary": "An API that tells trekking agencies which permits a route needs.",
                "description": (
                    "Agencies were reading permit rules off PDFs that change every "
                    "season. This turns the rules into data.\n\n"
                    "You post a route and a nationality, and you get back the list "
                    "of permits, their costs, and where to get them. Rules are "
                    "stored as versioned records, so a quote from last March still "
                    "explains itself.\n\n"
                    "Built with Django REST Framework, documented with drf-spectacular, "
                    "and used by four agencies at last count."
                ),
                "tech_stack": "Django REST Framework, PostgreSQL, Docker",
                "role": "Backend, with a designer",
                "is_featured": True,
                "completed_on": datetime.date(2025, 6, 18),
                "order": 2,
            },
            {
                "title": "Ledger reconciler",
                "summary": "Matches bank statements against invoices and flags what doesn't line up.",
                "description": (
                    "A small accounting team spent two days a month matching "
                    "statement lines to invoices by eye.\n\n"
                    "This imports a CSV statement, matches lines by amount, date "
                    "window, and reference string, and leaves only genuine "
                    "mismatches for a person to look at. Typical run leaves under "
                    "a dozen rows out of nine hundred.\n\n"
                    "Matching logic lives in plain Python functions with no Django "
                    "imports, which made it straightforward to test."
                ),
                "tech_stack": "Django, pandas, SQLite",
                "role": "Solo build",
                "is_featured": True,
                "completed_on": datetime.date(2024, 12, 2),
                "order": 3,
            },
            {
                "title": "Class schedule board",
                "summary": "A read-only timetable screen for a college corridor.",
                "description": (
                    "One page, refreshed every minute, showing which room every "
                    "class is in right now and what comes next.\n\n"
                    "Teachers update the timetable in the Django admin; the display "
                    "needs no interaction and recovers on its own if the network "
                    "drops."
                ),
                "tech_stack": "Django, SQLite",
                "role": "Solo build",
                "completed_on": datetime.date(2024, 8, 21),
                "order": 4,
            },
        ]
        for data in projects:
            Project.objects.get_or_create(title=data["title"], defaults=data)

        experience = [
            {
                "role": "Backend developer",
                "company": "Himalaya Labs",
                "location": "Kathmandu",
                "start_date": datetime.date(2024, 3, 1),
                "end_date": None,
                "description": (
                    "Own the billing service: subscriptions, invoices, and retries.\n"
                    "Cut the nightly report job from 40 minutes to under 3 by moving "
                    "aggregation into the database.\n"
                    "Review most backend pull requests and mentor two juniors."
                ),
                "order": 1,
            },
            {
                "role": "Junior developer",
                "company": "Naxal Software",
                "location": "Kathmandu",
                "start_date": datetime.date(2022, 7, 1),
                "end_date": datetime.date(2024, 2, 1),
                "description": (
                    "Built internal Django apps for HR and inventory.\n"
                    "Wrote the test suite that got the main project from 0 to 70 "
                    "percent coverage.\n"
                    "Handled deployments on a single Ubuntu box with gunicorn and nginx."
                ),
                "order": 2,
            },
        ]
        for data in experience:
            Experience.objects.get_or_create(
                role=data["role"], company=data["company"], defaults=data
            )

        Education.objects.get_or_create(
            school="Tribhuvan University",
            defaults={
                "qualification": "BSc Computer Science and Information Technology",
                "start_year": 2018,
                "end_year": 2022,
                "note": "Final year project: a Nepali text summariser.",
            },
        )

        self.stdout.write(self.style.SUCCESS("Demo content ready. Run the server and open /."))
