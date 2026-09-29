"""Everything your portfolio stores: who you are, what you built, who wrote to you."""
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Profile(models.Model):
    """You. Keep exactly one row — the site reads the first one it finds."""

    full_name = models.CharField(max_length=120)
    headline = models.CharField(
        max_length=160,
        help_text="One line under your name, e.g. 'Backend developer, Kathmandu'.",
    )
    bio = models.TextField(help_text="A few short paragraphs. Blank lines start new paragraphs.")
    location = models.CharField(max_length=120, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    avatar = models.ImageField(upload_to="profile/", blank=True)
    resume = models.FileField(upload_to="resume/", blank=True)

    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    x_url = models.URLField("X / Twitter URL", blank=True)
    website_url = models.URLField(blank=True)

    open_to_work = models.BooleanField(
        default=True, help_text="Shows an 'open to work' note in the sidebar."
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self):
        return self.full_name

    @property
    def first_name(self):
        return self.full_name.split(" ")[0]

    @property
    def social_links(self):
        """Pairs of (label, url) for whichever links are filled in."""
        candidates = [
            ("GitHub", self.github_url),
            ("LinkedIn", self.linkedin_url),
            ("X", self.x_url),
            ("Website", self.website_url),
        ]
        return [(label, url) for label, url in candidates if url]


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ("language", "Languages"),
        ("framework", "Frameworks"),
        ("database", "Databases"),
        ("tool", "Tools"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=60)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="other")
    proficiency = models.PositiveSmallIntegerField(
        default=70, help_text="0–100. Drawn as a bar on the home page."
    )
    order = models.PositiveSmallIntegerField(default=0, help_text="Lower numbers come first.")

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    summary = models.CharField(max_length=220, help_text="One sentence shown in the project list.")
    description = models.TextField(help_text="The full write-up. Blank lines start new paragraphs.")
    tech_stack = models.CharField(
        max_length=240, blank=True, help_text="Comma separated, e.g. Django, Postgres, HTMX"
    )
    image = models.ImageField(upload_to="projects/", blank=True)
    live_url = models.URLField(blank=True)
    repo_url = models.URLField(blank=True)
    role = models.CharField(max_length=120, blank=True, help_text="e.g. Solo build, Team of 4")
    completed_on = models.DateField(null=True, blank=True)
    is_featured = models.BooleanField(default=False, help_text="Featured projects show on the home page.")
    is_published = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-completed_on", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:150] or "project"
            slug = base
            counter = 2
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("portfolio:project_detail", kwargs={"slug": self.slug})

    @property
    def tech_list(self):
        return [item.strip() for item in self.tech_stack.split(",") if item.strip()]


class Experience(models.Model):
    role = models.CharField(max_length=140)
    company = models.CharField(max_length=140)
    company_url = models.URLField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Leave empty if this is current.")
    description = models.TextField(blank=True, help_text="One bullet per line.")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start_date"]
        verbose_name_plural = "Experience"

    def __str__(self):
        return f"{self.role} at {self.company}"

    @property
    def is_current(self):
        return self.end_date is None

    @property
    def period(self):
        start = self.start_date.strftime("%b %Y")
        end = self.end_date.strftime("%b %Y") if self.end_date else "Now"
        return f"{start} – {end}"

    @property
    def bullets(self):
        return [line.strip() for line in self.description.splitlines() if line.strip()]


class Education(models.Model):
    school = models.CharField(max_length=160)
    qualification = models.CharField(max_length=160, help_text="e.g. BSc Computer Science")
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField(null=True, blank=True)
    note = models.CharField(max_length=220, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start_year"]
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.qualification}, {self.school}"

    @property
    def period(self):
        return f"{self.start_year} – {self.end_year or 'Now'}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=160, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"{self.name} · {self.subject or 'No subject'}"
