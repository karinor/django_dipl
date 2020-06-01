from django import template
register = template.Library()

@register.filter(name='field_class')
def css(field):
    return field.as_widget(attrs={"class": 'simple-form-control form-control'})