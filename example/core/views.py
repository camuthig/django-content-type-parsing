from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django_content_parsing.request import HttpRequest


# Create your views here.


def index(request):
    return JsonResponse({"message": "Hello, world!"})


@csrf_exempt
def write_json(request: HttpRequest):
    return JsonResponse({"message": f"JSON message: {request.data['message']}"})


@csrf_exempt
def write_file(request: HttpRequest):
    data = request.data
    f = request.FILES.get("file")
    return JsonResponse({
        "file_message": f"{f.read().decode('utf-8')}",
        "text_message": f"File message: {request.POST['message']}",
    })


@csrf_exempt
def write_form(request: HttpRequest):
    print(request.data)
    return JsonResponse({"message": f"Form message: {request.data['message']}"})