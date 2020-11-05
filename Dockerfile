# set web server root as working dir
WORKDIR /Student-Forum/
# install required packages
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# copy all files
COPY . .

# expose port 8000
EXPOSE 8000

# start flask app using Gunicorn
CMD gunicorn -w 4 -b :8000 src.app:app
