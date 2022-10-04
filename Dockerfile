FROM debian:latest
ARG user
ARG password

WORKDIR /app
COPY . .
RUN apt-get upgrade -y && apt-get update
RUN apt-get install python3 sqlite3 python3-pip -y 
# RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
RUN pip install -r requirements.txt

RUN python3 init.py -l $user -p $password

CMD ["python3", "run.py"]
