from django import template
register = template.Library()

@register.simple_tag
def greet_user(message,username):
    return f"{message}, {username}!!!"

@register.simple_tag(takes_context=True)
def contextual_greet_user(context, message):
    return f"{message}, {context['username']}!!!!"