# -*- coding: utf-8 -*-
import json
import time
import random
import logging

import click
import gevent
import zmq.green as zmq
import gevent.monkey
from flask import Flask
from flask import Response
from flask import request
from agentzero.core import SocketManager

from flask_prometheus import monitor
from prometheus_client import Gauge
from prometheus_client import Counter
from prometheus_client import Histogram
from prometheus_client import CollectorRegistry
from prometheus_client import push_to_gateway
from prometheus_client.exposition import generate_latest

gevent.monkey.patch_all()

TODO_GROUPS = {"Work": []}
TODO_ITEMS = {
    "Prometheus": [
        "Install",
        "Configure",
        "Write a small application",
        "Instrument application",
        "Generate graph",
        "Create slack alert",
    ]
}

context = zmq.Context()
zmq_poll_timeout = 30  # miliseconds
sockets = SocketManager(zmq, context)
logger = sockets.get_logger("logs")
registry = CollectorRegistry()

class Metrics(object):

    http_request_latency = Histogram(
        "http_request_latency_seconds",
        "Flask HTTP Request Latency",
        ["method", "endpoint"],
        registry=registry,
    )

    http_request_count = Counter(
        "http_request_count",
        "Flask Request Count",
        ["method", "endpoint", "http_status"],
        registry=registry,
    )


def setup_application():
    app = Flask(__name__)

    def record_stats():
        request.start_time = time.time()

    def poll_zmq(response):
        logger.info(
            "handled request, will poll zmq for %s miliseconds", zmq_poll_timeout
        )
        sockets.engage(zmq_poll_timeout)
        return response

    def send_metrics(response):
        request_latency = time.time() - request.start_time
        Metrics.http_request_latency.labels(request.method, request.path).observe(
            request_latency
        )
        Metrics.http_request_count.labels(
            request.method, request.path, response.status_code
        ).inc()
        push_to_gateway('localhost:9091', job='pushed_flask', registry=registry)
        return response

    app.before_request(record_stats)
    app.after_request(send_metrics)
    app.after_request(poll_zmq)
    return app


app = setup_application()

@app.route("/")
@app.route("/<path:path>")
def get_todo_items(path='/'):
    time.sleep(random.uniform(0.0, 1.14))
    logger.info("PATH: %s", path)
    return Response(json.dumps([TODO_ITEMS] * random.randint(1, 1024), indent=None), content_type="application/json")


@app.route("/metrics")
def get_prometheus():
    return Response(generate_latest(registry), content_type='text/plain')


@click.command()
@click.option("--http-port", default=5000, help="the http port to listen to")
@click.option("--http-host", default="0.0.0.0", help="the http host to listen to")
@click.option("--debug", default=False, is_flag=True)
def cli(http_port, http_host, debug):
    """Simple web server that"""
    app.run(host=http_host, port=http_port, debug=debug)


if __name__ == "__main__":
    cli()
