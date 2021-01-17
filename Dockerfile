FROM python:3-alpine
COPY . /apps
WORKDIR /apps
RUN pip install -r requirements.txt
CMD ["python","-u","openweather_onecall_snow.py"]