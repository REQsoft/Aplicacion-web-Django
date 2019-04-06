from .models import Icon,Folder

def ctx_dict(request):
    ctx = {}
    icons = list(Icon.objects.all())
    folders = list(Folder.objects.all())
    ctx['icons'] = icons
    ctx['folders'] = folders
    return ctx