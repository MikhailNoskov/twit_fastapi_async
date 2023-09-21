from celery import Celery
from PIL import Image
import io

celery_app = Celery(__name__)
celery_app.conf.broker_url = 'redis://localhost:6379'
celery_app.conf.result_backend = 'redis://localhost:6379'


@celery_app.task
def resize_image(path, file_bytes, size_mb=2):
    if len(file_bytes) > 2 * 1024 * 1024:  # 2Mb
        print('Big file')
        input_stream = io.BytesIO(file_bytes)
        image = Image.open(input_stream)

        # Calculate resize ratio
        ratio = 2 * 1024 * 1024 / len(file_bytes)
        new_width = int(image.width * ratio)
        new_height = int(image.height * ratio)

        image = image.resize((new_width, new_height))

        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        # Convert to lower quality JPEG
        output_stream = io.BytesIO()
        image.save(output_stream, 'JPEG', quality=70)
        resized_bytes = output_stream.getvalue()

    else:
        resized_bytes = file_bytes
    with open(path, "wb") as f:
        f.write(resized_bytes)
    print('File saved')