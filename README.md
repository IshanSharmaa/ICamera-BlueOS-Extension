# ICamera-BlueOS-Extension
This is an Enhanced Camera BlueOS Extension. This Feature is used for Underwater Vehicle Cameras with BlueOS. It reduces The Blueness and Enhances The underwater camera video.

docker buildx create --name multiarch --driver docker-container --use

docker run --rm --privileged multiarch/qemu-user-static --reset

docker buildx build --platform linux/amd64,linux/arm/v7 . -t achyutabharadwajaeronuts/exa:Ecamera --output type=registry
docker pull achyutabharadwajaeronuts/exa:Ecamera

docker run -it achyutabharadwajaeronuts/exa:Ecamera

docker run -it --privileged achyutabharadwajaeronuts/exa:Ecamera

Username: achyutabharadwaj.aeronuts@gmail.com
password: DockerSucks1


ENTRYPOINT cd /app/static && python -m http.server 80


{
  "ExposedPorts": {
    "80/tcp": {}
  },
  "HostConfig": {
    "Privileged": true,
    "Binds": [
      "/root/.config:/root/.config"
    ],
    "PortBindings": {
      "80/tcp": [
        {
          "HostPort": ""
        }
      ]
    }
  }
}




Blue 
# Use the official Python image with the specified version
FROM python:3.9-slim-bullseye

# Set the working directory in the container
WORKDIR /opt/build

# Install system dependencies
RUN apt-get update && apt-get upgrade -y

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
    
RUN apt-get update && \
    apt-get install -y cmake
RUN apt-get update && \
    apt-get install -y git
RUN apt-get update && \
    apt-get install -y pkg-config
RUN apt-get update && \
    apt-get install -y libjpeg-dev
RUN apt-get update && \
    apt-get install -y libtiff-dev
RUN apt-get update && \
    apt-get install -y libpng-dev
RUN apt-get update && \
    apt-get install -y libavcodec-dev
RUN apt-get update && \
    apt-get install -y libavformat-dev
RUN apt-get update && \
    apt-get install -y libswscale-dev
RUN apt-get update && \
    apt-get install -y libv4l-dev
RUN apt-get update && \
    apt-get install -y libxvidcore-dev
RUN apt-get update && \
    apt-get install -y libx264-dev
RUN apt-get update && \
    apt-get install -y libfontconfig1-dev
RUN apt-get update && \
    apt-get install -y libcairo2-dev
RUN apt-get update && \
    apt-get install -y libgdk-pixbuf2.0-dev
RUN apt-get update && \
    apt-get install -y libpango1.0-dev
RUN apt-get update && \
    apt-get install -y libgtk2.0-dev
RUN apt-get update && \
    apt-get install -y libgtk-3-dev
RUN apt-get update && \
    apt-get install -y libatlas-base-dev
RUN apt-get update && \
    apt-get install -y gfortran
   

# Install NumPy using pip
RUN pip install numpy==1.19.5

# Copy the application code into the container
COPY app /app

# Install your application
RUN python /app/setup.py install
RUN pip install --upgrade pip setuptools wheel
RUN apt-get install python-is-python3
RUN apt-get update --fix-missing && apt-get install -y \
    python3-opencv 
RUN apt-get install libssl-dev

RUN apt-get install -y libhdf5-dev 
RUN apt-get install -y libhdf5-serial-dev 
RUN apt-get install -y python3-pyqt5 
RUN pip install --upgrade pip setuptools wheel
RUN pip install opencv-python==4.5.3.56
# Expose the necessary port
EXPOSE 80/tcp

LABEL version="1.0.1"
# TODO: Add a Volume for persistence across boots
LABEL permissions='\
{\
  "ExposedPorts": {\
    "80/tcp": {}\
  },\
  "HostConfig": {\
    "Binds":["/root/.config:/root/.config"],\
    "PortBindings": {\
      "80/tcp": [\
        {\
          "HostPort": ""\
        }\
      ]\
    }\
  }\
}'
LABEL authors='[\
    {\
        "name": "Krish Kataria",\
        "email": "krishk.aeronuts@gmail.com"\
    }\
]'
LABEL company='{\
        "about": "",\
        "name": "Aeronuts",\
        "email": ""\
    }'
LABEL type="example"
LABEL readme=''
LABEL links='{\
        "website": "",\
        "support": ""\
    }'
LABEL requirements="core >= 1.1"


# Set the entry point
ENTRYPOINT cd /app && python main.py


.











# Use the official Python image with the specified version
# Use the official Python image with the specified ver
FROM suntorytimed/resourcespace:latest

# Set the working directory in the container
WORKDIR /opt/build
RUN apt-get update -y --fix-missing && apt-get upgrade -y
RUN apt-get install -y git cmake
RUN apt-get install -y pkg-config
RUN apt-get install -y libssl-dev build-essential

RUN apt-get install -y python-is-python3
RUN pip install --upgrade pip
RUN pip install setuptools
RUN pip install wheel
RUN pip install numpy 
# RUN pip install opencv-python
# Install system dependencies

RUN apt-get update --fix-missing && apt-get install -y \
    python3-opencv

# Copy the application code into the container
COPY app /app
RUN python /app/setup.py install
# Expose the necessary port
EXPOSE 80/tcp

LABEL version="1.0.1"
# TODO: Add a Volume for persistence across boots
LABEL permissions='\
{\
  "ExposedPorts": {\
    "80/tcp": {}\
  },\
  "HostConfig": {\
    "Binds":["/root/.config:/root/.config"],\
    "PortBindings": {\
      "80/tcp": [\
        {\
          "HostPort": ""\
        }\
      ]\
    }\
  }\
}'
LABEL authors='[\
    {\
        "name": "Ishan Sharma",\
        "email": "Ishan23569@gmail.com"\
    }\
]'
LABEL company='{\
        "about": "",\
        "name": "Aeronuts",\
        "email": ""\
    }'
LABEL type="example"
LABEL readme=''
LABEL links='{\
        "website": "",\
        "support": ""\
    }'
LABEL requirements="core >= 1.1"


# Set the entry point
ENTRYPOINT cd /app && python main.py

