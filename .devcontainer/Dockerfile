FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

USER vscode

ARG AIRFLOW_VERSION=2.9.2
ARG TDENGINE_CLIENT_VERSION=3.3.3.0
ARG TDENGINE_CLIENT_PLATFORM=Linux-arm64

# Install Airflow
WORKDIR /home/vscode/airflow
RUN python -m pip install --upgrade pip
RUN pip install apache-airflow==${AIRFLOW_VERSION}

# Install TDengine client
WORKDIR /home/vscode/tdengine
RUN curl -s https://www.taosdata.com/assets-download/3.0/TDengine-client-${TDENGINE_CLIENT_VERSION}-${TDENGINE_CLIENT_PLATFORM}.tar.gz \
    --output tdengine-client.tar.gz
RUN tar -xf tdengine-client.tar.gz --directory . --strip-components=1 \
    && rm tdengine-client.tar.gz
RUN ./install_client.sh

# Install dependencies of TDengine provider
ADD requirements.txt ./tdengine-provider-requirements.txt
RUN pip install -r tdengine-provider-requirements.txt

# Init & start airflow
RUN python -m airflow db migrate
ENTRYPOINT ["airflow standalone"]
