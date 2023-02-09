from django import template


register = template.Library()


@register.filter()
def censor(value):
    words = ('редиска', 'fuck')
    if not isinstance(value, str):
        raise TypeError(f"unresolved type '{type(value)}' expected type 'str'")

    for word in value.split():
        if word.lower() in words:
            value = value.replace(word, f"{word[0]}{'*' * (len(word))}")
    return value
