FROM python:3.8

RUN apt-get update && apt-get install --yes libgdal-dev

ENV PYTHONUNBUFFERED 1
RUN mkdir /streamlit

WORKDIR /streamlit

COPY requirements.txt /streamlit

RUN pip install -r requirements.txt

COPY . /streamlit

EXPOSE 8501

CMD ["streamlit", "run", "Welcome!.py"]

ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8