FROM python:slim

ARG user
ARG password

WORKDIR /app
COPY . .

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    make \
    gcc \
    zlib1g-dev \
    libjpeg-dev\
    gcc \
    libfreetype6-dev\
    musl-dev\
    && pip install --only-binary :all numpy \
    && pip install -r requirements.txt \
    && apt-get remove -y --purge make gcc build-essential gcc musl-dev\
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
                                            
#RUN pip install numpy
#RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# RUN pip install -r requirements.txt


RUN python3 init.py -l $user -p $password -d testingDB.sqlite

CMD ["python3", "run.py"]