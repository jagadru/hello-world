FROM python:3.6.4

ADD . /srv/pricing_app

WORKDIR /srv/pricing_app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:3101", "app.server:MainApp.wsgi"]
