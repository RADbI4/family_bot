# first stage
FROM python:3.8
COPY . /src
WORKDIR /src
RUN  pip install -r requirements.txt
ADD ./family_bot_runner.py /
CMD [ "python", "-u", "./family_bot_runner.py" ]
