# Use python 3.10.x
FROM python:3.10

# Code will go in 'code' folder.
WORKDIR /code

# Copy enviroment settings into source.
COPY ./.env /code/.env

# Copy requirements file into source.
COPY ./requirements.txt /code/requirements.txt

# Run pip and install dependencies in 'requirements.txt'
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy source code into '/code/src'.
COPY ./src /code/src

# Run server on port 80.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "81"]

