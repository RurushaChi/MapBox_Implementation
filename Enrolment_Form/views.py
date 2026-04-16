from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import School, Staff, CustomForm, BaseForm, Application, AppAnswer
from .forms import CustomFormBuilderForm

def enrolment_form_view(request, school_id):
    school = get_object_or_404(School, id=school_id)

    base_form = BaseForm.objects.filter(is_active=True).first()

    if not base_form:
        return render(request, "error.html", {"message": "No active base form found."})

    custom_forms = CustomForm.objects.filter(
        school=school,
        is_active=True
    ).order_by("section_number")

    base_sections = base_form.form_schema["sections"]

    combined_sections = []

    for index, section in enumerate(base_sections, start=1):
        combined_sections.append({
            "section_number": index,
            "section_title": section["section_title"],
            "questions": section["questions"],
            "source_type": "base",
            "custom_form_id": None
        })

    for custom_form in custom_forms:
        combined_sections.append({
            "section_number": custom_form.section_number,
            "section_title": custom_form.title,
            "questions": custom_form.form_schema,
            "source_type": "custom",
            "custom_form_id": custom_form.id
        })

    if request.method == "POST":
        application = Application.objects.create(
            user=request.user,
            school=school,
            base_form=base_form,
            status="new"
        )

        application.custom_forms.set(custom_forms)

        for section in combined_sections:
            for question in section["questions"]:
                key = question["key"]

                if question["type"] == "file":
                    value = request.FILES.get(key)
                    if value:
                        AppAnswer.objects.create(
                            application=application,
                            source_type=section["source_type"],
                            custom_form_id=section["custom_form_id"],
                            question_key=key,
                            answer_file=value
                        )
                else:
                    value = request.POST.get(key)
                    if value:
                        AppAnswer.objects.create(
                            application=application,
                            source_type=section["source_type"],
                            custom_form_id=section["custom_form_id"],
                            question_key=key,
                            answer_text=value
                        )

        return render(request, "success.html", {"school": school})

    return render(request, "enrolment_form.html", {
        "sections": combined_sections,
        "school": school
    })
@login_required
def create_custom_form_view(request, school_id):
    school = get_object_or_404(School, id=school_id)
    staff = get_object_or_404(Staff, user=request.user, school=school)

    if request.method == "POST":
        form = CustomFormBuilderForm(request.POST)

        if form.is_valid():
            custom_form = form.save(commit=False)
            custom_form.school = school
            custom_form.created_by = staff

            question_labels = request.POST.getlist("question_label")
            question_keys = request.POST.getlist("question_key")
            question_types = request.POST.getlist("question_type")
            question_requireds = request.POST.getlist("question_required")
            question_choices = request.POST.getlist("question_choices")

            questions = []

            for i in range(len(question_labels)):
                label = question_labels[i].strip()
                key = question_keys[i].strip()
                q_type = question_types[i].strip()
                choices_raw = question_choices[i].strip()

                if not label or not key or not q_type:
                    continue

                question = {
                    "key": key,
                    "label": label,
                    "type": q_type,
                    "required": question_requireds[i] == "true",
                    "order": i + 1
                }

                if q_type == "select" and choices_raw:
                    question["choices"] = [
                        choice.strip()
                        for choice in choices_raw.split(",")
                        if choice.strip()
                    ]

                questions.append(question)

            custom_form.form_schema = questions
            custom_form.save()

            return redirect("custom_form_success")

    else:
        form = CustomFormBuilderForm()

    return render(
        request,
        "create_custom_form.html",
        {
            "form": form,
            "school": school
        }
    )


@login_required
def custom_form_success_view(request):
    return render(request, "custom_form_success.html")


