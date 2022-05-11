FROM python:3.9.7

RUN mkdir -p /usr/src/countbot/

WORKDIR /usr/src/countbot/

COPY . /usr/src/countbot/

RUN pip install -r requirements.txt

CMD ["python", "bot.py"]