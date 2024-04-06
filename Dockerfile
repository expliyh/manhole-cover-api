FROM python:3.12-bookworm
LABEL authors="Expliyh"
RUN apt-get update && apt-get install cmake -y && apt-get clean
ADD . /workdir
WORKDIR /workdir
RUN pip install -r requirements.txt
ENV DATABASE_HOST=mariadb
ENV DATABASE_PORT=3306
ENV DATABASE_NAME=your_database_name
ENV DATABASE_USERNAME=your_username
ENV DATABASE_PASSWORD=your_password
ENV DEVELOPER_CHAT_ID=""
ENV DATABASE_PREFIX=""
ENV TZ=Asia/Shanghai
#RUN mkdir tmp
#VOLUME /workdir/tmp
ENTRYPOINT ["python3", "-m", "uvicorn", "main:app"]