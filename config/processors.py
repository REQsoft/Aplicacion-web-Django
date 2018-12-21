from .models import Icon

def ctx_dict(request):
    ctx = {}
    icons = list(Icon.objects.all())
    ctx['icons'] = icons
    return ctx