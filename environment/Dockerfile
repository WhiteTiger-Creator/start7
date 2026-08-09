FROM public.ecr.aws/docker/library/python:3.13-slim-bookworm@sha256:01f42367a0a94ad4bc17111776fd66e3500c1d87c15bbd6055b7371d39c124fb

ENV DEBIAN_FRONTEND=noninteractive

# Least-volatile layers first: fix the working directory before the apt and
# dependency layers so a change to those never invalidates the WORKDIR layer.
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        tmux \
        asciinema \
    && rm -rf /var/lib/apt/lists/*

# /app/data/effective_rate_table.json ships STALE exactly as the mis-billing
# left it; the filed base tariff and the amendment filings beside it are the
# sources the responder has to consolidate back into the authoritative table.
COPY app/ /app/
RUN cp /app/workflow/rate_bill.py /app/workflow/.rate_bill.original \
    && chmod a-w /app/workflow/.rate_bill.original
