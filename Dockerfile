FROM joyzoursky/python-chromedriver:3.9-selenium
WORKDIR /app
COPY ./sources.list /etc/apt/sources.list
COPY ./qi-server .
RUN echo "installing nginx"
RUN cd /app && apt-get update -y && apt install nginx -y
RUN echo "installing Qi server requirement"
RUN cd /app && pip3 install -r requirements.txt
RUN cd /app && pip3 install uwsgi
RUN cd /app && chmod a+x start.sh
EXPOSE 80
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY ./qi-frontend/dist /usr/share/nginx/html
CMD ["./start.sh"]
