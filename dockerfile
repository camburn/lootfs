FROM ubuntu

RUN apt update; apt install git python3 python3-pip python3-venv

ENV VIRTUAL_ENV=/opt/venv
RUN PYTHON3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run the application:
COPY loots .
CMD ["gunicorn", "loots.wsgi"]
