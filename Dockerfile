FROM debian:latest

ARG user
ARG password

WORKDIR /app
COPY . .
RUN rm /app/TelloBeep/database/db.sqlite

RUN apt-get update && apt-get upgrade -y

RUN apt-get install python3 sqlite3 python3-pip -y 

# RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
RUN pip install -r requirements.txt


RUN python3 init.py -l $user -p $password

CMD ["python3", "run.py"]
