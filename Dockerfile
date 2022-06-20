FROM --platform=$TARGETPLATFORM python:3.9-slim-buster
WORKDIR /app
COPY ./sources.list /etc/apt/sources.list
COPY ./qi-server /app/
RUN rm -rf /app/*.ics && rm -rf /app/config.ini
RUN echo "installing nginx"
RUN cd /app && apt-get update -y && apt install nginx gcc -y && rm -rf /var/lib/apt/lists/*
RUN echo "installing Qi server requirement"
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN cd /app && pip3 install -r requirements.txt && pip3 install uwsgi
RUN cd /app && chmod a+x start.sh
EXPOSE 80
COPY ./nginx.conf /etc/nginx/sites-available/default
COPY ./qi-frontend/dist /usr/share/nginx/html
CMD ["./start.sh"]
