FROM python:3.10.11-alpine3.18
USER root
COPY src/ /app
RUN pip install -r /app/requirements.txt
EXPOSE 8000
ENTRYPOINT [ "/app/entrypoint.sh" ]