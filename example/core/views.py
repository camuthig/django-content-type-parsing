from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django_content_parsing.request import HttpRequest


def index(request):
    return JsonResponse({"message": "Hello, world!"})


@csrf_exempt
def write_json(request: HttpRequest):
    return JsonResponse({"message": f"JSON message: {request.data['message']}"})


@csrf_exempt
def write_file(request: HttpRequest):
    data = request.data
    f = request.files.get("file")
    return JsonResponse({
        "file_message": f"{f.read().decode('utf-8')}",
        "text_message": f"File message: {data['message']}",
    })


@csrf_exempt
def write_form(request: HttpRequest):
    return JsonResponse({"message": f"Form message: {request.data['message']}"})


@csrf_exempt
def write_json_old(request):
    return JsonResponse({"message": f"JSON message: {request.POST['message']}"})


@csrf_exempt
def write_file_old(request):
    data = request.POST
    f = request.FILES.get("file")
    return JsonResponse({
        "file_message": f"{f.read().decode('utf-8')}",
        "text_message": f"File message: {data['message']}",
    })


@csrf_exempt
def write_form_old(request):
    return JsonResponse({"message": f"Form message: {request.POST['message']}"})


@csrf_exempt
def json_form_data(request):
    return JsonResponse({"message": f"JSON message: {request.form_data['message']}"})


@csrf_exempt
def form_form_data(request):
    return JsonResponse({"message": f"Form message: {request.form_data['message']}"})


@csrf_exempt
def invalid_data_after_post(request):
    post_data = request.POST
    data_data = request.data  # This will throw an error!
    return JsonResponse({"message": f"JSON message: {request.data['message']}"})


@csrf_exempt
def invalid_post_after_data(request):
    data_data = request.data
    post_data = request.POST  # This will throw an error!
    return JsonResponse({"message": f"JSON message: {request.data['message']}"})
