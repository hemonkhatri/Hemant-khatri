from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactForm
from .models import Education, Experience, Profile, Project, Skill


def _grouped_skills():
    """{'Languages': [Skill, ...], 'Frameworks': [...]} in the model's declared order."""
    grouped = {}
    for skill in Skill.objects.all():
        grouped.setdefault(skill.get_category_display(), []).append(skill)
    return grouped


def home(request):
    projects = Project.objects.filter(is_published=True)
    featured = projects.filter(is_featured=True)[:4] or projects[:4]
    context = {
        "featured_projects": featured,
        "project_count": projects.count(),
        "skills_by_category": _grouped_skills(),
        "experiences": Experience.objects.all(),
        "educations": Education.objects.all(),
    }
    return render(request, "portfolio/home.html", context)


def project_list(request):
    projects = Project.objects.filter(is_published=True)
    query = request.GET.get("q", "").strip()
    if query:
        projects = projects.filter(title__icontains=query) | projects.filter(
            tech_stack__icontains=query
        )
        projects = projects.distinct()
    return render(
        request, "portfolio/project_list.html", {"projects": projects, "query": query}
    )


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_published=True)
    others = Project.objects.filter(is_published=True).exclude(pk=project.pk)[:3]
    return render(
        request, "portfolio/project_detail.html", {"project": project, "others": others}
    )


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            if not form.is_spam:
                message = form.save()
                _notify_owner(message)
            messages.success(
                request, "Message sent. I'll reply to the address you gave."
            )
            return redirect("portfolio:contact")
        messages.error(request, "Check the highlighted fields and send again.")
    else:
        form = ContactForm()
    return render(request, "portfolio/contact.html", {"form": form})


def _notify_owner(message):
    """Email yourself when someone writes. Prints to the console while DEBUG=True."""
    profile = Profile.objects.first()
    if not profile:
        return
    send_mail(
        subject=f"Portfolio message from {message.name}",
        message=f"From: {message.name} <{message.email}>\n\n{message.message}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[profile.email],
        fail_silently=True,
    )
