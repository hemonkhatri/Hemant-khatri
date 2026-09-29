from django.contrib import admin

from .models import ContactMessage, Education, Experience, Profile, Project, Skill


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "headline", "email", "open_to_work")
    fieldsets = (
        ("Who you are", {"fields": ("full_name", "headline", "bio", "location", "open_to_work")}),
        ("How to reach you", {"fields": ("email", "phone")}),
        ("Files", {"fields": ("avatar", "resume")}),
        ("Links", {"fields": ("github_url", "linkedin_url", "x_url", "website_url")}),
    )

    def has_add_permission(self, request):
        # Only one profile row is ever needed.
        return not Profile.objects.exists()


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "proficiency", "order")
    list_editable = ("category", "proficiency", "order")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "is_featured", "is_published", "completed_on", "order")
    list_editable = ("is_featured", "is_published", "order")
    list_filter = ("is_featured", "is_published")
    search_fields = ("title", "summary", "tech_stack")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {"fields": ("title", "slug", "summary", "description", "image")}),
        ("Details", {"fields": ("tech_stack", "role", "completed_on", "live_url", "repo_url")}),
        ("Visibility", {"fields": ("is_featured", "is_published", "order")}),
    )


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "start_date", "end_date", "order")
    list_editable = ("order",)
    search_fields = ("role", "company")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("qualification", "school", "start_year", "end_year", "order")
    list_editable = ("order",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at")
    actions = ["mark_read", "mark_unread"]

    def has_add_permission(self, request):
        return False

    @admin.action(description="Mark selected messages as read")
    def mark_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description="Mark selected messages as unread")
    def mark_unread(self, request, queryset):
        queryset.update(is_read=False)
