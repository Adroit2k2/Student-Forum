# set web server root as working dir
WORKDIR /mysite/
# copy all files
COPY . .

# expose port 8000
EXPOSE 8000

# start flask app using Gunicorn
CMD web: gunicorn mysite/mysite.wsgi --log-file -
