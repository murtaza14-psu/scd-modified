from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from .models import *
from authentication.models import *
from .forms import AttendanceForm, AttendanceCheckoutForm, ApplicationForm
import pandas as pd
from io import BytesIO
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from django.template.loader import get_template

@login_required
def export_attendance_excel(request, opportunity_id):
    if request.user.role != 'ngo':
        messages.error(request, "Access denied")
        return redirect("authentication:home")

    opportunity = get_object_or_404(Opportunity, id=opportunity_id)

    # Check if the logged-in NGO owns this opportunity
    if opportunity.ngo.id != request.user.ngo_profile.id:
        messages.error(request, "Access denied")
        return redirect("authentication:home")

    # Get all accepted applications for the opportunity
    applications = Application.objects.filter(
        opportunity_id=opportunity_id, status="accepted"
    )

    # Get attendance records
    attendances = {a.volunteer_id: a for a in Attendance.objects.filter(opportunity_id=opportunity_id)}

    # Prepare data for Excel
    data = []
    for app in applications:
        volunteer = app.volunteer
        attendance = attendances.get(volunteer.id)

        row = {
            "Volunteer Name": volunteer.user.name,
            "Email": volunteer.user.email,
            "Status": "Not Checked In",
            "Check-in Time": attendance.check_in_time.strftime('%Y-%m-%d %H:%M') if attendance and attendance.check_in_time else '',
            "Check-out Time": attendance.check_out_time.strftime('%Y-%m-%d %H:%M') if attendance and attendance.check_out_time else '',
            "Hours Contributed": attendance.hours_contributed if attendance and attendance.hours_contributed else '',
            "Notes": attendance.notes if attendance and attendance.notes else ''
        }

        if attendance:
            row["Status"] = attendance.status.replace("_", " ").title()

        data.append(row)

    # Create a Pandas DataFrame
    df = pd.DataFrame(data)

    # Create an Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Attendance", index=False)

        # Auto-adjust column width
        worksheet = writer.sheets["Attendance"]
        for idx, col in enumerate(df.columns):
            col_letter = get_column_letter(idx + 1)
            max_length = max(df[col].astype(str).str.len().max(), len(col)) + 2
            worksheet.column_dimensions[col_letter].width = max_length

    output.seek(0)

    # Generate filename
    filename = f"attendance_{opportunity.title.replace(' ', '_')}_{now().strftime('%Y%m%d')}.xlsx"

    # Return the file as an HTTP response
    response = HttpResponse(
        output.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response

@login_required
def apply_opportunity(request, opportunity_id):
    if request.user.role != 'volunteer':  # Ensures only volunteers can apply
        messages.error(request, "Only volunteers can apply to opportunities.")
        return redirect("authentication:home")

    opportunity = get_object_or_404(Opportunity, id=opportunity_id)
    volunteer_profile = request.user.volunteer_profile  # Assuming user has a `volunteer_profile`

    # Check if the user has already applied
    existing_application = Application.objects.filter(volunteer=volunteer_profile, opportunity=opportunity).first()

    if existing_application:
        if existing_application.status == "pending":
            messages.info(request, "You have already applied for this opportunity. Your application is under review.")
            return redirect("opportunities:opportunities")  # Adjust as needed
        elif existing_application.status == "accepted":
            messages.success(request, "Congratulations! You have been accepted for this opportunity.")
            return redirect("opportunities:opportunities")  # Adjust as needed
        elif existing_application.status == "rejected":
            messages.warning(request, "Your application was rejected. You can apply again.")

    form = ApplicationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        application = Application(
            volunteer=volunteer_profile,
            opportunity=opportunity,
            message=form.cleaned_data['message']
        )
        application.save()
        messages.success(request, "Application submitted successfully!")
        return redirect("opportunities:opportunities")  # Adjust URL name as needed

    return render(request, "apply.html", {"form": form, "opportunity": opportunity})


@login_required
def manage_opportunity(request, opportunity_id):
    if request.user.role != 'ngo':
        messages.error(request, 'Only NGOs can manage attendance')
        return redirect('authentication:home')
    
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)
    
    if opportunity.ngo.id != request.user.ngo_profile.id:
        messages.error(request, 'You can only manage attendance for your own opportunities')
        return redirect('authentication:home')
    
    applications = Application.objects.filter(opportunity_id=opportunity_id, status='accepted')
    attendances = {a.volunteer.id: a for a in Attendance.objects.filter(opportunity_id=opportunity_id)}
    
    attendances = {att.volunteer.id: att for att in Attendance.objects.filter(opportunity=opportunity)}

    return render(request, 'manage.html', {
        'opportunity': opportunity,
        'applications': applications,
        'attendances': attendances,
        'form': AttendanceForm()
    })

from django.views.decorators.csrf import csrf_protect
@login_required
@csrf_protect  # Instead of @csrf_exempt, we use CSRF protection
def check_in(request, opportunity_id, volunteer_id):
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    if request.user.role != 'ngo':
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    opportunity = get_object_or_404(Opportunity, id=opportunity_id)

    if opportunity.ngo.id != request.user.ngo_profile.id:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    volunteer = get_object_or_404(VolunteerProfile, id=volunteer_id)

    # Check if volunteer is already checked in
    if Attendance.objects.filter(opportunity=opportunity, volunteer=volunteer).exists():
        return JsonResponse({'error': 'Volunteer already checked in'}, status=400)

    # Create a new attendance record
    attendance = Attendance.objects.create(
        volunteer=volunteer,
        opportunity=opportunity,
        check_in_time=now(),
        status="checked_in",
    )

    return JsonResponse({'status': 'success', 'attendance_id': attendance.id})
@login_required
@csrf_exempt
def check_out(request, attendance_id):
    if request.user.role != 'ngo':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    attendance = get_object_or_404(Attendance, id=attendance_id)
    opportunity = get_object_or_404(Opportunity, id=attendance.opportunity_id)
    
    if opportunity.ngo.id != request.user.ngo_profile.id:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    form = AttendanceCheckoutForm(request.POST)
    if form.is_valid():
        try:
            hours = float(form.cleaned_data['hours_contributed'])
            if hours < 0:
                return JsonResponse({'error': 'Hours must be positive'}, status=400)
            
            attendance.check_out_time = now()
            attendance.hours_contributed = hours
            attendance.status = 'completed'
            attendance.notes = form.cleaned_data['notes']
            attendance.save()
            
            return JsonResponse({'status': 'success'})
        except ValueError:
            return JsonResponse({'error': 'Invalid hours format'}, status=400)
    
    return JsonResponse({'error': 'Invalid form data'}, status=400)


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from applications.models import Application

@csrf_exempt  # Only if CSRF token issues occur (better to handle it properly)
def update_application_status(request, application_id):
    if request.method == "POST":
        application = get_object_or_404(Application, id=application_id)

        new_status = request.POST.get("status")
        if new_status in ["accepted", "rejected"]:
            application.status = new_status
            application.save()
            return JsonResponse({"status": "success", "new_status": new_status})
        else:
            return JsonResponse({"status": "error", "error": "Invalid status."})

    return JsonResponse({"status": "error", "error": "Invalid request method."})
