# UNTESTED. Minimal image for the data-only checks (pure standard library).
# Stage tools (GCC 13.3, Cppcheck 2.13.0, libclang) are installed by the stage repositories.
FROM python:3.12-slim
WORKDIR /artifact
COPY . /artifact
CMD ["make", "check"]
