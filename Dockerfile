FROM python:slim

ARG user
ARG password

WORKDIR /app
COPY . .

RUN apt-get update && \
    apt-get install -y \
    build-essential libssl-dev libffi-dev libjpeg-dev zlib1g-dev libfreetype6-dev libpng-dev \
    python3-dev cargo\
    rustc\
    && python -m pip install --upgrade pip\
    && pip install --only-binary :all numpy \
    && pip install --only-binary :all cryptography==3.3.2\
    && pip install -r requirements.txt\
    && apt-get remove -y --purge make gcc build-essential gcc musl-dev\
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
                                            
#RUN pip install numpy
#RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# RUN pip install -r requirements.txt

RUN python3 init.py -l $user -p $password

CMD ["python3", "run.py"]
