from django.shortcuts import (
    render,
    redirect
)
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm

from django.db.models import Q

from .models import AssetImage


from .models import Dataset


from .models import (
    AssetImage,
    DetectionResult
)

from .services import (
    detect_objects
)
from .services import (
    detect_objects,
    draw_boxes
)
from django.shortcuts import get_object_or_404, redirect


import json
from django.contrib.auth import authenticate
import csv
from django.http import HttpResponse

from .models import DetectionResult

from django.http import JsonResponse



def home(request):

    return render(

        request,

        "home.html"

    )
from django.contrib import messages

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Registration successful. Please login."
            )

            return redirect("login")

        else:

            print(form.errors)

            messages.error(
                request,
                "Please correct the errors below."
            )

    else:

        form = RegisterForm()

    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )
def login_view(request):

    if request.method == "POST":

        username = request.POST.get(

            "username"

        )

        password = request.POST.get(

            "password"

        )

        user = authenticate(

            request,

            username=username,

            password=password

        )

        if user is not None:

            login(

                request,

                user

            )

            return redirect(

                "upload"

            )

        else:

            return render(

                request,

                "login.html",

                {

                    "error":

                    "Invalid Username or Password"

                }

            )

    return render(

        request,

        "login.html"

    )

@login_required
def logout_view(request):

    logout(request)

    return redirect(

        "home"

    )

@login_required
def upload_images(request):

    if request.method == "POST":

        files = request.FILES.getlist(
            "images"
        )

        for file in files:

            AssetImage.objects.create(
                image=file
            )

        return redirect(
            'dashboard'
        )

    return render(
        request,
        'upload.html'
    )

@login_required
def process_tags(request):

    if request.method == "POST":

        raw_tags = request.POST.get("tags", "")

        try:
            tag_data = json.loads(raw_tags)
            tags = [item["value"].strip() for item in tag_data]
        except Exception:
            tags = [
                tag.strip()
                for tag in raw_tags.split(",")
                if tag.strip()
            ]

        images = AssetImage.objects.filter(status="pending")

        for image in images:

            DetectionResult.objects.filter(image=image).delete()

            image.status = "processing"
            image.save()

            for tag in tags:

                detections = detect_objects(
                    image.image.path,
                    tag
                )

                draw_boxes(
                    image.image.path,
                    detections,
                    image,
                    tag
                )

            image.status = "completed"
            image.save()

        return redirect("results")

    return render(
        request,
        "dashboard.html"
    )
@login_required
def results(request):

    search = request.GET.get("search", "")

    images = AssetImage.objects.all()

    if search:

        images = images.filter(
            Q(image__icontains=search) |
            Q(detections__tag__icontains=search)
        ).distinct()

    context = {

        "images": images,
        "search": search,
        "total_images": images.count(),
        "total_detections": DetectionResult.objects.count(),

    }

    return render(
        request,
        "results.html",
        context
    )


def export_csv(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response['Content-Disposition'] = (
        'attachment; filename="detections.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'Image Name',
        'detection.tag',
        'Confidence',
        'BBox'
    ])

    detections = DetectionResult.objects.select_related(
        'image'
    )

    for detection in detections:

        writer.writerow([
            detection.image.image.name,
            detection.tag,
            detection.confidence,
            detection.bbox
        ])

    return response



def export_json(request):

    detections = DetectionResult.objects.select_related(
        "image"
    )

    data = []

    for detection in detections:

        data.append({

            "image_name":
            detection.image.image.name,

            "tag":
            detection.tag,

            "confidence":
            detection.confidence,

            "bbox":
            detection.bbox

        })

    response = HttpResponse(
        json.dumps(
            data,
            indent=4
        ),
        content_type="application/json"
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="detections.json"'

    return response 


def bulk_upload(request):

    if request.method == "POST":

        dataset_name = request.POST.get(
            "dataset_name"
        )

        dataset = Dataset.objects.create(
            name=dataset_name
        )

        files = request.FILES.getlist(
            "images"
        )

        for file in files:

            AssetImage.objects.create(
                dataset=dataset,
                image=file,
                status="pending"
            )

        return redirect(
            "dashboard"
        )

    return render(
        request,
        "assets/bulk_upload.html"
    )


def delete_image(request, image_id):

    image = get_object_or_404(
        AssetImage,
        id=image_id
    )

    # Delete image file from media folder
    if image.image:
        image.image.delete()

    image.delete()

    return redirect("results")


def process_images_view(request):
    if request.method == "POST":
        raw_tags = request.POST.get('tags', '') # This comes from Tagify as '[{"value":"car"}]'
        
        # Safe JSON parsing
        clean_tags = []
        if raw_tags:
            try:
                # Convert the JSON string into a Python list of dictionaries
                tag_data_list = json.loads(raw_tags)
                # Extract just the plain text string out of each object
                clean_tags = [item['value'] for item in tag_data_list]
            except json.JSONDecodeError:
                # Fallback if the string happens to be plain comma-separated text
                clean_tags = [t.strip() for t in raw_tags.split(',') if t.strip()]

        # --- Your Object Detection Logic Here ---
        # When you filter detections, use the clean_tags array:
        # e.g., image.detections.filter(tag__in=clean_tags)
        
    return render(request, 'results.html')

