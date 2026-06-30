from django.db import models

class Dataset(models.Model):

    name = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name

class AssetImage(models.Model):
    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True
    )

    image = models.ImageField(
        upload_to="uploads/"
    )

    status = models.CharField(
        max_length=20,
        default="pending"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.image.name
    
class DetectionResult(models.Model):

    image = models.ForeignKey(
        AssetImage,
        on_delete=models.CASCADE,
        related_name='detections'
    )

    tag = models.CharField(
        max_length=255
    )

    confidence = models.FloatField()

    bbox = models.JSONField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.tag
    
   

