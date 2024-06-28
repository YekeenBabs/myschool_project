# templatetags/custom_filters.py

from django import templates

register = templates.Library()

@register.filter(name='get_week_range')
def get_week_range(start, end):
    return range(start, end + 1)

@register.filter(name='get_assignments_for_week')
def get_assignments_for_week(assignments, week):
    return [assignment for assignment in assignments if assignment.week == week]
