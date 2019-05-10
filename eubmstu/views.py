from django.http import HttpResponse

from eubmstu.settings import BASE_DIR


def favicon(request):
    image_data = open(BASE_DIR + '/static/favicon.ico', "rb").read()
    return HttpResponse(image_data, content_type="image/x-icon")