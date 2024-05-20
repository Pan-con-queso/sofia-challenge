FROM python:3.10.13
ENV PYTHONUNBUFFERED True

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r  requirements.txt

ENV APP_HOME .
WORKDIR $APP_HOME
COPY /bonus $APP_HOME/bonus

EXPOSE 8080
CMD ["uvicorn", "bonus:app", "--host", "0.0.0.0", "--port", "8080"]