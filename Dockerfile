FROM hemanhp/djbase:4.2.4

RUN pip install --upgrade pip

COPY ./requirements /requirements
COPY ./scripts /scripts
COPY ./src /src

WORKDIR src

EXPOSE 8000

RUN /py/bin/pip install --no-cache-dir -r /requirements/development.txt


RUN chmod -R +x /scripts && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    adduser --disabled-password --no-create-home djshop && \
    chmod -R 755 /vol

ENV PATH="/scripts:/py/bin:$PATH"


CMD ["run.sh"]