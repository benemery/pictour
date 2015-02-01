from django import template

register = template.Library()

@register.assignment_tag()
def tour_completed(user, tour):
    """Has the user completed this tour?"""
    return user.tours.filter(tour=tour, completed=True).exists()