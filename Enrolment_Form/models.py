from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


def application_upload_path(instance, filename):
    school_id = instance.application.school_id if instance.application and instance.application.school_id else "unknown"
    application_id = instance.application_id if instance.application_id else "unknown"
    return f"uploads/school_{school_id}/application_{application_id}/{filename}"


class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class UserRole(models.Model):
    class RoleType(models.TextChoices):
        SCHOOL_ADMIN = "school_admin", "School Admin"
        SCHOOL_SYSTEMS_ADMIN = "school_systems_admin", "School Systems Admin"
        SLT = "slt", "SLT"
        CAREGIVER = "caregiver", "Caregiver"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="role_profile"
    )
    school = models.ForeignKey(
        "School",
        on_delete=models.CASCADE,
        related_name="user_roles",
        blank=True,
        null=True
    )
    role_type = models.CharField(
        max_length=30,
        choices=RoleType.choices
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["school__name", "user__username"]

    def __str__(self):
        return f"{self.user} - {self.get_role_type_display()}"


class BaseForm(models.Model):
    name = models.CharField(max_length=255, default="Base Enrolment Form")
    version = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    form_schema = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_active", "-version"]

    def __str__(self):
        return f"{self.name} (v{self.version})"


class CustomForm(models.Model):
    school = models.ForeignKey(
        "School",
        on_delete=models.CASCADE,
        related_name="custom_forms"
    )
    created_by = models.ForeignKey(
        "UserRole",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_custom_forms"
    )
    title = models.CharField(max_length=255)
    section_number = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    form_schema = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["school__name", "section_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["school", "section_number"],
                name="unique_customform_section_per_school"
            )
        ]

    def clean(self):
        if self.section_number is not None and self.section_number < 5:
            raise ValidationError("Custom form section number must be 5 or greater.")

    def save(self, *args, **kwargs):
        if not self.section_number:
            last_custom_form = self.__class__.objects.filter(
                school=self.school
            ).order_by("-section_number").first()

            if last_custom_form:
                self.section_number = last_custom_form.section_number + 1
            else:
                self.section_number = 5

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.school.name} - Section {self.section_number} - {self.title}"


class Application(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        IN_REVIEW = "in_review", "In Review"
        INCOMPLETE = "incomplete", "Incomplete"
        APPROVED = "approved", "Approved"
        DECLINED = "declined", "Declined"
        WAITLISTED = "waitlisted", "Waitlisted"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    school = models.ForeignKey(
        "School",
        on_delete=models.CASCADE,
        related_name="applications"
    )
    base_form = models.ForeignKey(
        "BaseForm",
        on_delete=models.PROTECT,
        related_name="applications"
    )
    custom_forms = models.ManyToManyField(
        "CustomForm",
        related_name="applications",
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )

    submitted_at = models.DateTimeField(blank=True, null=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Application #{self.pk} - {self.user} - {self.get_status_display()}"


class AppAnswer(models.Model):
    class SourceType(models.TextChoices):
        BASE = "base", "Base Form"
        CUSTOM = "custom", "Custom Form"

    application = models.ForeignKey(
        "Application",
        on_delete=models.CASCADE,
        related_name="answers"
    )
    source_type = models.CharField(
        max_length=10,
        choices=SourceType.choices
    )
    custom_form = models.ForeignKey(
        "CustomForm",
        on_delete=models.CASCADE,
        related_name="answers",
        blank=True,
        null=True
    )

    question_key = models.CharField(max_length=100)

    answer_text = models.TextField(blank=True, null=True)
    answer_file = models.FileField(
        upload_to=application_upload_path,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["application_id", "id"]
        indexes = [
            models.Index(fields=["application", "source_type"]),
            models.Index(fields=["question_key"]),
        ]

    def clean(self):
        if not self.answer_text and not self.answer_file:
            raise ValidationError("An answer must contain either text or a file.")

        if self.answer_text and self.answer_file:
            raise ValidationError("An answer cannot contain both text and a file.")

        if self.source_type == self.SourceType.BASE and self.custom_form is not None:
            raise ValidationError("Base form answers must not link to a custom form.")

        if self.source_type == self.SourceType.CUSTOM and self.custom_form is None:
            raise ValidationError("Custom form answers must link to a custom form.")

        if self.custom_form and self.application and self.custom_form.school_id != self.application.school_id:
            raise ValidationError("Custom form school must match the application school.")

    def __str__(self):
        return f"Application {self.application_id} - {self.question_key}"


class InterviewAvailability(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        ARCHIVED = "archived", "Archived"

    class Weekday(models.IntegerChoices):
        MONDAY = 0, "Monday"
        TUESDAY = 1, "Tuesday"
        WEDNESDAY = 2, "Wednesday"
        THURSDAY = 3, "Thursday"
        FRIDAY = 4, "Friday"
        SATURDAY = 5, "Saturday"
        SUNDAY = 6, "Sunday"

    staff = models.ForeignKey(
        "UserRole",
        on_delete=models.CASCADE,
        related_name="interview_availabilities"
    )
    school = models.ForeignKey(
        "School",
        on_delete=models.CASCADE,
        related_name="interview_availabilities"
    )

    title = models.CharField(max_length=100, blank=True, null=True)

    weekday = models.IntegerField(choices=Weekday.choices)
    window_start_time = models.TimeField()
    window_end_time = models.TimeField()

    slot_length_minutes = models.PositiveIntegerField()
    generate_weeks = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    effective_from = models.DateField(blank=True, null=True)
    effective_until = models.DateField(blank=True, null=True)
    generated_until_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["school_id", "staff_id", "weekday", "window_start_time"]
        indexes = [
            models.Index(fields=["school", "staff", "status"]),
            models.Index(fields=["weekday"]),
        ]

    def clean(self):
        if self.window_end_time <= self.window_start_time:
            raise ValidationError("Window end time must be after window start time.")

        if self.slot_length_minutes <= 0:
            raise ValidationError("Slot length must be greater than 0 minutes.")

        if self.generate_weeks <= 0:
            raise ValidationError("Generate weeks must be greater than 0.")

        if self.staff and self.school and self.staff.school_id != self.school_id:
            raise ValidationError("Staff school must match the selected school.")

    def __str__(self):
        return f"{self.title or 'Interview Availability'} - {self.get_weekday_display()}"


class InterviewSlot(models.Model):
    availability = models.ForeignKey(
        "InterviewAvailability",
        on_delete=models.SET_NULL,
        related_name="slots",
        blank=True,
        null=True
    )
    staff = models.ForeignKey(
        "UserRole",
        on_delete=models.CASCADE,
        related_name="interview_slots"
    )
    school = models.ForeignKey(
        "School",
        on_delete=models.CASCADE,
        related_name="interview_slots"
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    is_active = models.BooleanField(default=True)
    is_booked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["start_time"]
        indexes = [
            models.Index(fields=["school", "staff", "is_active", "is_booked"]),
            models.Index(fields=["start_time"]),
        ]

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

        if self.staff and self.school and self.staff.school_id != self.school_id:
            raise ValidationError("Staff school must match the selected school.")

        if self.availability and self.availability.school_id != self.school_id:
            raise ValidationError("Availability school must match the selected school.")

        if self.availability and self.availability.staff_id != self.staff_id:
            raise ValidationError("Availability staff must match the selected staff.")

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


class Interview(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Slots Sent"
        BOOKED = "booked", "Booked"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    application = models.OneToOneField(
        "Application",
        on_delete=models.CASCADE,
        related_name="interview"
    )
    slot = models.ForeignKey(
        "InterviewSlot",
        on_delete=models.SET_NULL,
        related_name="interviews",
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    booked_at = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["application_id"]
        indexes = [
            models.Index(fields=["status"]),
        ]

    def clean(self):
        if self.slot and self.application and self.slot.school_id != self.application.school_id:
            raise ValidationError("Interview slot school must match the application school.")

    def __str__(self):
        return f"Interview for Application {self.application_id}"