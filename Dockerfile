FROM python:3.7-alpine
RUN mkdir /app
WORKDIR /app
RUN apk add libevent-dev build-base libffi-dev

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

ADD src/ /app/src
ADD app.py /app

CMD exec python app.py $PORT