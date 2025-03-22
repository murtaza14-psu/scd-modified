from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
import json
import csv
from.forms import *
from .models import Application, Attendance
from opportunities.models import Opportunity
from authentication.models import VolunteerProfile


@login_required
def apply_opportunity(request, opportunity_id):
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)

    try:
        volunteer_profile = request.user.volunteer_profile
    except ObjectDoesNotExist:
        messages.error(request, "You need to create a volunteer profile before applying.")
        return redirect('opportunities:opportunities')

    if hasattr(request.user, "role") and request.user.role != 'volunteer':
        messages.error(request, "Only volunteers can apply for opportunities.")
        return redirect('opportunities:opportunities')

    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.volunteer = volunteer_profile
            application.opportunity = opportunity
            application.save()
            messages.success(request, "Application submitted successfully!")
            return redirect('opportunities:opportunities')

    else:
        form = ApplicationForm()

    return render(request, "apply.html", {"form": form, "opportunity": opportunity})

@login_required
def manage_opportunity(request, opportunity_id):
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)
    applications = Application.objects.filter(opportunity=opportunity)
    
    # Convert attendances into a dictionary for direct access
    attendances = {attendance.volunteer.id: attendance for attendance in Attendance.objects.filter(opportunity=opportunity)}

    return render(request, 'manage.html', {
        'opportunity': opportunity,
        'applications': applications,
        'attendances': attendances,  # This is now a dictionary
    })



@login_required
def check_in(request, opportunity_id, volunteer_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            status = data.get("status", "checked_in")
            notes = data.get("notes", "")

            opportunity = get_object_or_404(Opportunity, id=opportunity_id)
            volunteer = get_object_or_404(VolunteerProfile, id=volunteer_id)

            attendance, created = Attendance.objects.get_or_create(
                volunteer=volunteer,
                opportunity=opportunity,
                defaults={"status": status, "notes": notes, "check_in_time": now()}
            )

            if not created:
                attendance.status = status
                attendance.notes = notes
                attendance.check_in_time = now()
                attendance.save()

            return JsonResponse({"success": True, "message": "Checked in successfully!"})
        except Exception as e:
            print("Error:", e)  # Log error to the console
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)


@login_required
def check_out(request, attendance_id):
    """Handles volunteer check-out."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            hours_contributed = float(data.get("hours_contributed", 0))
            notes = data.get("notes", "")

            attendance = get_object_or_404(Attendance, id=attendance_id)

            attendance.status = "completed"
            attendance.check_out_time = now()
            attendance.hours_contributed = hours_contributed
            attendance.notes = notes
            attendance.save()

            return JsonResponse({"success": True, "message": "Checked out successfully!"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)
    
    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)


@login_required
def export_attendance_excel(request, opportunity_id):
    """Exports attendance data to a CSV file."""
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)
    attendance_records = Attendance.objects.filter(opportunity=opportunity)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{opportunity.title}_attendance.csv"'

    writer = csv.writer(response)
    writer.writerow(["Volunteer", "Status", "Check-in Time", "Check-out Time", "Hours Contributed", "Notes"])

    for record in attendance_records:
        writer.writerow([
            record.volunteer.user.username,
            record.status,
            record.check_in_time.strftime('%Y-%m-%d %H:%M:%S') if record.check_in_time else "",
            record.check_out_time.strftime('%Y-%m-%d %H:%M:%S') if record.check_out_time else "",
            record.hours_contributed or "0",
            record.notes
        ])

    return response
