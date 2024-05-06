FROM python:3.10
MAINTAINER Rayan Lee bopp <rayanleeboppcastoulooraya@gmail.com>
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
EXPOSE 5000
EXPOSE 3306
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]
