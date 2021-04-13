ARG PYTHON_VERSION=3.7
FROM python:${PYTHON_VERSION}-slim-buster AS build

WORKDIR /usr/src

COPY poetry.lock pyproject.toml ./
COPY loopia_of_fury/ ./loopia_of_fury/

RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH
ENV PYTHONPATH=/venv/lib/python${PYTHON_VERSION}/site-packages
RUN pip install .

# venv won't overwrite symlinks when they point to non-existing files...
## python3 -m venv --upgrade /venv
#Error: [Errno 2] No such file or directory: '/venv/bin/python3': '/venv/bin/python3'
RUN rm -f /venv/bin/python*

# Distroless don't currently have version tags
# FROM gcr.io/distroless/python3-debian10@sha256:33ddd28c748279670ad4d7ca9ad088c233f2f7bef6daf0a6ed00fc89490dffce
# There's no real difference so always run the debug container
# REPOSITORY                           TAG                          IMAGE ID       CREATED              SIZE
# loopia_of_fury                       debug                        acc34f12f15d   13 seconds ago       65MB
# loopia_of_fury                       prod                         0575b8564299   About a minute ago   63.9MB
FROM gcr.io/distroless/python3-debian10:debug@sha256:396827c703e8f43f6483d2e723592ea3bfaeafc5d327bcfca9cddaed74ead3cf
ARG PYTHON_VERSION=3.7

COPY --from=build /venv /venv
ENV PATH=/venv/bin:$PATH
ENV PYTHONPATH=/venv/lib/python${PYTHON_VERSION}/site-packages

# Upgrade the venv so we get this containers python3
# Also, without --without-pip it will try to install pip which will fail.
RUN python3 -m venv --upgrade --without-pip /venv

ENTRYPOINT ["loopia_of_fury"]
CMD ["--help"]
