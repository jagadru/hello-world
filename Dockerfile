FROM python:3.6.4

WORKDIR /pricing

RUN pip install gunicorn

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

CMD ["gunicorn", "-b", "0.0.0.0:3101", "application.app:MainApp.wsgi"]                                                            
