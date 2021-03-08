FROM nginx
WORKDIR /app
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY ./sources.list /etc/apt/sources.list
COPY ./qi-server .
COPY ./qi-frontend/dist /usr/share/nginx/html
RUN echo "installing python3"
RUN cd /app && apt-get update -y && apt install python3 -y && apt install python3-pip -y
RUN echo "installing Qi server requirement"
RUN cd /app && pip3 install -r requirements.txt
RUN cd /app && pip3 install uwsgi
RUN cd /app && chmod a+x start.sh
CMD ["./start.sh"]
