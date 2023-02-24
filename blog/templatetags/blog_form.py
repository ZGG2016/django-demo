from django import template

from blog.forms import PersonForm

register = template.Library()


@register.inclusion_tag('_form.html', takes_context=True)
def show_person_form(context):

    form = PersonForm()
    return {'form': form}
