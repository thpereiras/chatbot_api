FROM python:3.7.9-alpine3.13

MAINTAINER pereirasthiago

WORKDIR /app
ENV WORKDIR=/app

RUN apk add --no-cache --virtual=build_deps g++ && \
    pip install --no-cache-dir spacy==2.1.8 && \
    pip install --no-cache-dir ChatterBot==1.1.0a7 && \
    pip install --no-cache-dir PyYAML==5.3.1 && \
    pip install --no-cache-dir chatterbot-corpus==1.2.0 && \
    python -m spacy download en && \
    python -m spacy download pt && \
    pip install --no-cache-dir Flask==1.1.2 && \
    pip install --no-cache-dir PyMySQL==1.0.2 && \
    pip install --no-cache-dir Flask-Cors==3.0.10 && \
    apk add --no-cache libstdc++ && \
    pip install --no-cache-dir flask-marshmallow==0.14.0 && \
    pip install --no-cache-dir Flask-SQLAlchemy==2.4.4 && \
    pip install --no-cache-dir marshmallow-sqlalchemy==0.24.2 && \
    pip install --no-cache-dir Flask-JWT-Extended==4.0.2 && \
    apk add --no-cache python3-dev libffi-dev && \
    pip install --no-cache-dir Flask-Bcrypt==0.7.1 && \
    apk del g++ python3-dev libffi-dev && \
    apk del build_deps

CMD ["sh"]
