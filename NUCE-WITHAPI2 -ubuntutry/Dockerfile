# Use the official Python image with the specified version
# Use the official Python image with the specified ver
# syntax=docker/dockerfile:1.3-labs
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
RUN apt-get install -y \
    libopencv-dev
RUN apt-get install -y sudo

# RUN pip install --upgrade opencv-python

# Copy the application code into the container
COPY app /app
RUN python /app/setup.py install
RUN usermod -aG video root
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
        "email": "Aeronuts.developer@gmail.com"\
    }'
LABEL type="video"
LABEL readme=''
LABEL links='{\
        "website": "",\
        "support": ""\
    }'
LABEL requirements="core >= 1.1"

# Set the entry point
CMD ["python", "-m", "http.server" "80"]
# ENTRYPOINT cd /app && python main.py  python -m http.server 80 && 
ENTRYPOINT cd /app && uvicorn main:app --host 0.0.0.0 --port 80 && python main.py