from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application
from opportunities.models import Opportunity
from authentication.models import VolunteerProfile
from .forms import ApplicationForm
from django.core.exceptions import ObjectDoesNotExist

@login_required
def apply_opportunity(request, opportunity_id):
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)

    # Check if user has a volunteer profile
    try:
        volunteer_profile = request.user.volunteer_profile  # Use the related_name
    except ObjectDoesNotExist:
        messages.error(request, "You need to create a volunteer profile before applying.")
        return redirect('opportunities:opportunities')

    # If the user model has a 'role' field, check if it's 'volunteer'
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

    return render(request, "apply.html", {
        "form": form,
        "opportunity": opportunity
    })
