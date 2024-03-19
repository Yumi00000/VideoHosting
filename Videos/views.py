from Videos.models import Video


def videos(request):
    video = Video.objects.get()
    return "ok"
