FROM python:3.13-slim

WORKDIR /app

# Deps for opencv-python (WSL)
RUN apt-get update && apt-get install ffmpeg libgl1 libsm6 libxext6 libxcb-xinerama0 -y

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ENV QT_QPA_PLATFORM=offscreen
EXPOSE 8889/udp
EXPOSE 8890/udp
EXPOSE 11111/udp
EXPOSE 11112/udp
EXPOSE 5000

CMD ["python", "manual-control.py"]
