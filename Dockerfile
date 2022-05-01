FROM python:3.7.4-alpine3.10

RUN apt-get update && \
    apt-get install --no-install-recommends -y curl

ENV CONDA_AUTO_UPDATE_CONDA=false \
    PATH=/opt/miniconda/bin:$PATH

RUN curl -sLo ~/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-py37_4.11.0-Linux-x86_64.sh \
    && chmod +x ~/miniconda.sh \
    && ~/miniconda.sh -b -p /opt/miniconda \
    && rm ~/miniconda.sh \
    && sed -i "$ a PATH=/opt/miniconda/bin:\$PATH" /etc/environment

# Installing python dependencies
RUN python3 -m pip --no-cache-dir install --upgrade pip && \
    python3 --version && \
    pip3 --version

COPY ./requirements.txt .
RUN pip3 --timeout=300 --no-cache-dir install -r requirements.txt

# Copy app files
COPY ./ /app
WORKDIR /app/
ENV PYTHONPATH=/app
RUN ls -lah /app/*

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

EXPOSE 8000