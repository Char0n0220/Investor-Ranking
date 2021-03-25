FROM python:3.7.5-slim
COPY . /Investor-Ranking
WORKDIR /Investor-Ranking
RUN python3 -m pip install -r requirements.txt
ENTRYPOINT ["python3","run_pipeline.py"]