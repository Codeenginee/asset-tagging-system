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


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_api(request):
    return Response({
        "message": "JWT Authentication Successful!",
        "user": request.user.username
    })


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
@login_required(login_url="login")

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

@login_required(login_url="login")

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

@login_required(login_url="login")

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

@login_required(login_url="login")

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

@login_required(login_url="login")


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

@login_required(login_url="login")
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

@login_required(login_url="login")

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

@login_required(login_url="login")

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






@api_view(['POST'])
def login_api(request):

    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is None:
        return Response(
            {"error": "Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    refresh = RefreshToken.for_user(user)

    return Response({
        "message": "Login Successful",
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "username": user.username,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def results_api(request):

    search = request.GET.get("search", "")

    images = AssetImage.objects.all()

    if search:
        images = images.filter(
            Q(image__icontains=search) |
            Q(detections__tag__icontains=search)
        ).distinct()

    data = []

    for image in images:

        detections = DetectionResult.objects.filter(image=image)

        tags = []

        for detection in detections:
            tags.append({
                "tag": detection.tag,
                "confidence": detection.confidence
            })

        data.append({
            "id": image.id,
            "image": image.image.url,
            "uploaded_at": image.uploaded_at if hasattr(image, "uploaded_at") else None,
            "detections": tags
        })

    return Response({
        "status": "success",
        "total_images": images.count(),
        "total_detections": DetectionResult.objects.count(),
        "results": data
    }, status=status.HTTP_200_OK)

@api_view(['POST'])

def upload_api(request):

    if 'image' not in request.FILES:
        return Response(
            {"error": "No image uploaded"},
            status=status.HTTP_400_BAD_REQUEST
        )

    image = request.FILES['image']

    asset = AssetImage.objects.create(
        image=image
    )

    return Response({
        "message": "Image uploaded successfully",
        "image_id": asset.id,
        "image_url": asset.image.url
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def detect_api(request):

    image_id = request.data.get("image_id")

    if not image_id:
        return Response(
            {"error": "image_id is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    image = get_object_or_404(
        AssetImage,
        id=image_id
    )

    # Call your existing detection function
    detections = detect_objects(
        image.image.path,
        "person, car, dog, cat"
    )

    return Response({
        "message": "Detection completed",
        "detections": detections
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_api(request):

    user = request.user

    return Response({
        "status": "success",
        "message": "User Profile Retrieved Successfully",
        "data": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "is_active": user.is_active,
            "date_joined": user.date_joined
        }
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_api(request):

    try:
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {
                    "status": "error",
                    "message": "Refresh token is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response(
            {
                "status": "success",
                "message": "Logout successful."
            },
            status=status.HTTP_200_OK
        )

    except Exception:
        return Response(
            {
                "status": "error",
                "message": "Invalid or expired refresh token."
            },
            status=status.HTTP_400_BAD_REQUEST
        )