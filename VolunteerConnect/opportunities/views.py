from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Opportunity
from .forms import OpportunityForm

# def opportunities(request):
#     opportunities = Opportunity.objects.all()
#     locations = sorted(set(opportunity.location for opportunity in opportunities))
#     return render(request, 'list.html', {
#         'opportunities': opportunities,
#         'locations': locations
#     })


def opportunities(request):
    opportunities = Opportunity.objects.filter(status='open', content_status='active')
    print("Opportunities in view:", opportunities)  # Debugging
    locations = sorted(set(opportunity.location for opportunity in opportunities))

    return render(request, 'list.html', {
        'opportunities': opportunities,
        'locations': locations
    })

# @login_required
# def createOpportunity(request):
#     print(request.user)  # Debugging: check logged-in user
#     print(hasattr(request.user, 'ngo_profile'))

#     if not hasattr(request.user, 'ngo_profile'):
#         messages.error(request, 'Only NGOs can create opportunities.')
#         return redirect('authentication:home')

#     if request.method == 'POST':
#         form = OpportunityForm(request.POST)
#         if form.is_valid():
#             opportunity = form.save(commit=False)
#             opportunity.ngo = request.user.ngoprofile
#             opportunity.save()
#             messages.success(request, 'Opportunity created successfully!')
#             return redirect('opportunities')

#     else:
#         form = OpportunityForm()

#     return render(request, 'create.html', {'form': form})


@login_required
def createOpportunity(request):
    # Check if user has an NGOProfile
    if not hasattr(request.user, 'ngo_profile'):
        print(1)
        messages.error(request, 'Only NGOs can create opportunities.')
        return redirect('authentication:home')
    
    ngo_profile = request.user.ngo_profile  # Corrected related_name

    # Ensure the user role is 'ngo' and they are verified
    if request.user.role != 'ngo':
        print(2)
        messages.error(request, 'Only users registered as NGOs can create opportunities.')
        return redirect('authentication:home')

    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            opportunity = form.save(commit=False)
            opportunity.ngo = ngo_profile  # Assign the NGOProfile
            opportunity.save()
            messages.success(request, 'Opportunity created successfully!')
            return redirect('opportunities:opportunities')

    else:
        form = OpportunityForm()

    return render(request, 'create.html', {'form': form})
