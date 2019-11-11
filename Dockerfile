FROM python:3.6

WORKDIR /root
RUN git clone https://github.com/Prokuma/line-drawing-twitter-bot.git
WORKDIR /root/line-drawing-twitter-bot
RUN pip install -r requirements.txt
CMD python app.py
