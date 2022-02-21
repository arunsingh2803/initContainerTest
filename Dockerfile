FROM python:latest
COPY script.py /script.py
COPY requirements.txt /requirements.txt
RUN chmod 755 /script.py
RUN pip install -r requirements.txt
ENTRYPOINT [ "python3", "./script.py" ]
