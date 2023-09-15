from django.template import Library


register = Library()
french_months = [
    "janvier", "février", "mars", "avril", "mai", "juin", "juillet",
    "aout", "septembre", "octobre", "novembre", "décembre"
]


@register.filter
def get_instance_type(instance):
    return type(instance).__name__


@register.filter
def format_time_created(time_created):
    if time_created == "":
        return time_created
    return time_created.strftime(f"%H:%M, %d {french_months[time_created.month-1]} %Y")


@register.simple_tag(takes_context=True)
def format_author(context, user):
    if context["user"] == user:
        return "Vous avez"
    else:
        return f"{str(user).capitalize()} a"


@register.filter(name='times')
def times(number):
    return range(number)


@register.filter
def subtract(rating):
    return 5 - rating
