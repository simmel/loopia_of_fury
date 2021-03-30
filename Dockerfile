FROM python:3.7-slim-buster AS build

WORKDIR /usr/src

COPY poetry.lock pyproject.toml ./
COPY loopia_of_fury/ ./loopia_of_fury/

RUN pip install . --no-cache-dir -t /venv

# Distroless don't currently have version tags
# FROM gcr.io/distroless/python3-debian10@sha256:33ddd28c748279670ad4d7ca9ad088c233f2f7bef6daf0a6ed00fc89490dffce
FROM gcr.io/distroless/python3-debian10:debug

COPY --from=build /venv /venv
ENV PYTHONPATH=/venv

# ENTRYPOINT ["/usr/bin/python3", "/app/main.py"]
ENTRYPOINT ["/usr/bin/python3", "/venv/bin/loopia_of_fury"]
CMD ["--help"]
