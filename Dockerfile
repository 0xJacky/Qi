FROM --platform=linux/amd64 python:3.9-slim-buster
WORKDIR /app
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
COPY ./qi-server /app/
RUN rm -rf /app/*.ics && rm -rf /app/config.ini
RUN echo "installing nginx"
RUN apt-get update -y && apt install nginx -y && rm -rf /var/lib/apt/lists/*
RUN echo "installing Qi server requirement"
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install -r requirements.txt && pip3 install uwsgi
RUN chmod a+x start.sh
EXPOSE 80
COPY ./nginx.conf /etc/nginx/sites-available/default
COPY ./qi-frontend/dist /usr/share/nginx/html
CMD ["./start.sh"]
