FROM python:3.9
WORKDIR /server
COPY requirements.txt /server
RUN pip3 install --upgrade pip -r requirements.txt
COPY ./server /server
EXPOSE 8080
CMD ["python3", "server.py"]