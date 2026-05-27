FROM public.ecr.aws/lambda/python:3.11-arm64

COPY requirements.txt .
RUN pip install -r requirements.txt --target /var/task

COPY . /var/task/

WORKDIR /var/task

CMD ["handler.handler"]