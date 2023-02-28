# syntax=docker/dockerfile:1.4
# FROM pytorch/pytorch
FROM python:3.10

# Configure apt and install packages
RUN apt-get update -y && \
    apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-dev \
    git \
    unzip \
    wget \
    # cleanup
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists

WORKDIR /app

COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . .

RUN wget https://github.com/JaidedAI/EasyOCR/releases/download/v1.3/english_g2.zip
RUN wget https://github.com/JaidedAI/EasyOCR/releases/download/v1.6.1/cyrillic_g2.zip
RUN wget https://github.com/JaidedAI/EasyOCR/releases/download/pre-v1.1.6/craft_mlt_25k.zip
RUN mkdir ~/.EasyOCR
RUN mkdir ~/.EasyOCR/model
RUN unzip english_g2.zip -d ~/.EasyOCR/model
RUN unzip cyrillic_g2.zip -d ~/.EasyOCR/model
RUN unzip craft_mlt_25k.zip -d ~/.EasyOCR/model
RUN rm english_g2.zip
RUN rm cyrillic_g2.zip
RUN rm craft_mlt_25k.zip


ENV FLASK_APP server.py
ENV FLASK_RUN_PORT 8000
ENV FLASK_RUN_HOST 0.0.0.0


EXPOSE 8000

# CMD ["sleep","3600"]
# CMD ["flask", "run"]

# ENTRYPOINT ["python3"]
# CMD ["server.py"]

# CMD ["python3", "server.py"]
CMD ["flask", "run"]