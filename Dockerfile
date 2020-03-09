FROM debian:latest

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-rpi.gpio \
    libtiff5-dev \ 
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libfreetype6-dev \ 
    liblcms2-dev \ 
    libwebp-dev \
    python3-setuptools  --no-install-recommends


RUN pip3 install --no-binary pillow pillow requests
RUN pip3 install Adafruit_SSD1306 pyserial

RUN mkdir /home/MAPS6_Minimum_Viable_Product


COPY . /home/MAPS6_Minimum_Viable_Product

WORKDIR /MAPS6_Minimum_Viable_Product


CMD python3 PI_test.py
