FROM python:3.8.3-slim
COPY requirements.txt .

RUN pip install --user -r requirements.txt
RUN mkdir -p /log

WORKDIR /src

COPY ./src .

ENTRYPOINT ["python", "openHABSkill.py"]