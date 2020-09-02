FROM w3prog/camundaworker:v2
COPY ./requirements.txt /app/requirements.txt
WORKDIR app
RUN pip install -r requirements.txt
COPY ./worker /app/worker
COPY ./camunda /app/camunda
COPY ./main.py /app/main.py
COPY ./wait_for_camunda.sh /app/wait_for_camunda.sh
CMD ["bash","wait_for_camunda.sh"]
