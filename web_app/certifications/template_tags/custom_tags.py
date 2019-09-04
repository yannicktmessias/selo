from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def page_found(reports, page):
    if len(reports[page]) > 0:
        return (reports[page])[0].page_found
    return False

# https://stackoverflow.com/questions/50703556/get-dictionary-value-by-key-in-django-template