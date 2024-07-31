FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

USER vscode

# Install TDengine client
WORKDIR /home/vscode/tdengine
RUN curl -s https://www.taosdata.com/assets-download/3.0/TDengine-client-3.3.0.0-Linux-arm64.tar.gz --output tdengine-client.tar.gz
RUN tar -xf tdengine-client.tar.gz --directory . --strip-components=1 \
    && rm tdengine-client.tar.gz
RUN ./install_client.sh

# Install airflow
WORKDIR /home/vscode/airflow
COPY --chown=vscode --chmod=0755 constraints.txt .
RUN pip install 'apache-airflow==2.9.2' --constraint constraints.txt

# Install other dependencies
RUN pip install taospy
RUN pip install pytest-mock
