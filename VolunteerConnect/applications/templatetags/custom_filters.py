from django import template

register = template.Library()

@register.filter
def get_attendance(attendances, volunteer_id):
    return attendances.get(volunteer_id, None)
