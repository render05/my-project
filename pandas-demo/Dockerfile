FROM python:slim
WORKDIR /app
COPY requirement.txt .
run pip install -r requirement.txt
COPY pandas-demo.py .
CMD ["python","pandas-demo.py"]