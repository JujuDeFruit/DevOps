FROM python:slim
EXPOSE 8050

# Install python and pip
RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get install -y iputils-ping 

# Workdir folder -> arg non consistent env var
ARG FOLDER="/builds/printerfaceadmin/group5"

RUN mkdir FOLDER

# Eq. to move to folder
WORKDIR FOLDER

# Copy needed folder and files
COPY connection ./connection
COPY requirements.txt .
COPY READ_ME.md .

# install dependencies
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python", "connection/interface.py"]
