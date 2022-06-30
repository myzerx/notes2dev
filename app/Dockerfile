FROM python:3.10.5-alpine
COPY . /app
WORKDIR /app
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev
RUN pip install -r requirements.txt
RUN pip install PyMySQL
RUN pip install Flask
RUN pip install Flask-MySQL
ENTRYPOINT ["python"]
CMD ["rest.py"]
EXPOSE 5000