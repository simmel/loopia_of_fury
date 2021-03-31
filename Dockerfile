ARG PYTHON_VERSION=3.7
FROM python:${PYTHON_VERSION}-slim-buster AS build

WORKDIR /usr/src

COPY poetry.lock pyproject.toml ./
COPY loopia_of_fury/ ./loopia_of_fury/

RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH
ENV PYTHONPATH=/venv/lib/python${PYTHON_VERSION}/site-packages
RUN pip install .

# Distroless don't currently have version tags
# FROM gcr.io/distroless/python3-debian10@sha256:33ddd28c748279670ad4d7ca9ad088c233f2f7bef6daf0a6ed00fc89490dffce
# There's no real difference so always run the debug container
# REPOSITORY                           TAG                          IMAGE ID       CREATED              SIZE
# loopia_of_fury                       debug                        acc34f12f15d   13 seconds ago       65MB
# loopia_of_fury                       prod                         0575b8564299   About a minute ago   63.9MB
FROM gcr.io/distroless/python3-debian10:debug@sha256:f6c3961ea6a177c21e31449e4833904e35434ba2038757771b0a2d3dc7958a31
ARG PYTHON_VERSION=3.7

COPY --from=build /venv /venv
ENV PATH=/venv/bin:$PATH
ENV PYTHONPATH=/venv/lib/python${PYTHON_VERSION}/site-packages

# Upgrade the venv so we get this containers python3
# Also, without --without-pip it will try to install pip which will fail.
RUN python3 -m venv --upgrade --without-pip /venv

ENTRYPOINT ["loopia_of_fury"]
CMD ["--help"]
