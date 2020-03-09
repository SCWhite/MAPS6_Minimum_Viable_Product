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
    python3-setuptools  
#--no-install-recommends

RUN pip3 install --no-binary Pillow requests

#RUN pip3 install wheel
#RUN pip3 install --upgrade pip

#RUN apt-get install -y python3-wheel python-dev

RUN pip3 install Adafruit_SSD1306 pyserial
#RUN pip3 install adafruit-circuitpython-ssd1306
#RUN pip3 install pyserial

RUN pip3 install Pillow 

RUN mkdir /home/MAPS6_MVP


COPY . /home/MAPS6_MVP/
COPY ARIALUNI.TTF /home/

WORKDIR /home/MAPS6_MVP


CMD python3 PI_test.py
