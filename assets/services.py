import os
import torch
from PIL import Image, ImageDraw

from transformers import (
    AutoProcessor,
    AutoModelForZeroShotObjectDetection
)

from .models import DetectionResult

MODEL_ID = "IDEA-Research/grounding-dino-tiny"

processor = AutoProcessor.from_pretrained(MODEL_ID)
model = AutoModelForZeroShotObjectDetection.from_pretrained(MODEL_ID)


def detect_objects(image_path, prompt):
    image = Image.open(image_path).convert("RGB")

    inputs = processor(
        images=image,
        text=prompt,
        return_tensors="pt"
    )

    with torch.no_grad():
        outputs = model(**inputs)

    results = processor.post_process_grounded_object_detection(
        outputs=outputs,
        input_ids=inputs.input_ids,
        threshold=0.25,
        text_threshold=0.20,
        target_sizes=[image.size[::-1]]
    )

    return results


def draw_boxes(image_path, detections, asset_image, tag):

    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    # Delete previous results
    DetectionResult.objects.filter(image=asset_image).delete()

    for result in detections:

        boxes = result["boxes"]
        scores = result["scores"]
        labels = result["labels"]

        if len(boxes) == 0:
            continue

        # Highest confidence detection
        best_index = scores.argmax().item()

        box = boxes[best_index].tolist()
        score = scores[best_index].item()
        label = tag

        # Get tag name
        if isinstance(label, str):
            tag_name = label
        elif isinstance(label, dict):
            tag_name = label.get("value", "")
        else:
            tag_name = str(label)

        tag_name = tag_name.strip()

        # Save to database
        DetectionResult.objects.create(
            image=asset_image,
            tag=tag_name,
            confidence=round(score, 2),
            bbox=[
                round(box[0]),
                round(box[1]),
                round(box[2]),
                round(box[3]),
            ]
        )

        # Draw Bounding Box
        x1, y1, x2, y2 = box

        draw.rectangle(
            [(x1, y1), (x2, y2)],
            outline="red",
            width=3
        )

        draw.text(
            (x1, y1 - 15),
            f"{tag_name} ({score:.2f})",
            fill="red"
        )

        break

    # Save result image
    result_dir = os.path.join(
        os.path.dirname(image_path),
        "..",
        "results"
    )

    os.makedirs(result_dir, exist_ok=True)

    output_path = os.path.join(
        result_dir,
        os.path.basename(image_path)
    )

    image.save(output_path)

    return output_path