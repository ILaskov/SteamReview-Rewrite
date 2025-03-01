from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    """
    Adds a CSS class to the HTML element.
    Usage: {{ form.field_name|add_class:"your-class-name" }}
    """
    return value.as_widget(attrs={'class': arg})
