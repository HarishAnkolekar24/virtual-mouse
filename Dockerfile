FROM python:2.7
CMD mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -qqy x11-apps

RUN pip install opencv-python==3.4.9.31
RUN pip install scikit-image
RUN pip install pyautogui

COPY index.py /usr/src/app/

ENTRYPOINT [ "python", "index.py" ]