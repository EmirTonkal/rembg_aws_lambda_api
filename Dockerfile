FROM public.ecr.aws/lambda/python:3.11

COPY app/requirements.txt ./
RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt

COPY app/ ./app/

RUN python - <<'PY'
from rembg import remove
from PIL import Image
import io
img = Image.new('RGB', (4, 4), (255, 255, 255))
buf = io.BytesIO()
img.save(buf, format='PNG')
_ = remove(buf.getvalue())
print('u2net prefetched')
PY

CMD ["app.handler"]
