
# Register your models here.
from django.contrib import admin

from .models import (
    AssetImage,
    DetectionResult,
    
)

admin.site.register(AssetImage)
admin.site.register(DetectionResult)
