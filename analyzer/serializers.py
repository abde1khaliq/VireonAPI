from rest_framework import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import io
import requests

import logging
logger = logging.getLogger(__name__)

class AnalyzeContentSerializer(serializers.Serializer):
    user_input = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    image_url = serializers.URLField(required=False)

    def _process_image_file(self, image):
        valid_mime_types = {
            "image/png": "PNG",
            "image/jpeg": "JPEG",
            "image/webp": "WEBP",
            "image/avif": "AVIF",
            "image/gif": "GIF"
        }

        content_type = getattr(image, "content_type", None)
        logger.info(f"Processing uploaded image with content type: {content_type}")

        if content_type not in valid_mime_types:
            readable = ", ".join(valid_mime_types.keys())
            logger.warning(f"Unsupported image format: {content_type}")
            raise serializers.ValidationError(
                f"Unsupported image format: {content_type}. Supported formats: {readable}"
            )

        try:
            img = Image.open(image)
            img.verify()
            logger.info("Image verification passed")
        except Exception as e:
            logger.error(f"Image verification failed: {e}")
            raise serializers.ValidationError(
                f"Invalid image file. Could not process: {str(e)}"
            )

        image.file.seek(0)
        img = Image.open(image)
        output = io.BytesIO()
        img.save(output, format="PNG")
        output.seek(0)
        image.file = output
        image.content_type = "image/png"
        logger.info("Image successfully converted to PNG")
        return image



    def _download_and_convert_url(self, url):
        logger.info(f"Downloading image from URL: {url}")
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            img = Image.open(io.BytesIO(response.content))
            img.verify()
            img = Image.open(io.BytesIO(response.content))  # Reopen after verify
            logger.info("Downloaded image verified successfully")
        except Exception as e:
            logger.error(f"Failed to download or verify image: {e}")
            raise serializers.ValidationError(
                f"Invalid image URL. Could not process: {str(e)}"
            )

        output = io.BytesIO()
        img.save(output, format="PNG")
        output.seek(0)
        logger.info("Image from URL successfully converted to PNG")

        return InMemoryUploadedFile(
            file=output,
            field_name="image",
            name="downloaded.png",
            content_type="image/png",
            size=output.getbuffer().nbytes,
            charset=None
        )


    def validate(self, data):
        text = data.get("user_input")
        image = data.get("image")
        image_url = data.get("image_url")

        logger.info("Validating input data")
        provided_inputs = sum(bool(x) for x in [text, image, image_url])
        logger.debug(f"Inputs received — text: {bool(text)}, image: {bool(image)}, image_url: {bool(image_url)}")

        if provided_inputs == 0:
            logger.warning("No input provided")
            raise serializers.ValidationError(
                "Please provide either text or image input."
            )
        if provided_inputs > 1:
            logger.warning("Multiple input types provided")
            raise serializers.ValidationError(
                "Only one type of input is allowed at a time: text, image file, or image URL."
            )

        if image:
            logger.info("Image file detected")
            data["image"] = self._process_image_file(image)
            data["detected_content_type"] = "image"
        elif image_url:
            logger.info("Image URL detected")
            data["image"] = self._download_and_convert_url(image_url)
            data["detected_content_type"] = "image"
        else:
            logger.info("Text input detected")
            data["detected_content_type"] = "text"

        logger.info(f"Content type resolved: {data['detected_content_type']}")
        return data