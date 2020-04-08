"""Methods for command-line parsing."""
import argparse
import logging

import paho.mqtt.client as mqtt


def add_hermes_args(parser: argparse.ArgumentParser):
    """Add shared Hermes/MQTT command-line arguments."""
    parser.add_argument(
        "--host", default="localhost", help="MQTT host (default: localhost)"
    )
    parser.add_argument(
        "--port", type=int, default=1883, help="MQTT port (default: 1883)"
    )
    parser.add_argument("--username", help="MQTT username")
    parser.add_argument("--password", help="MQTT password")
    parser.add_argument(
        "--site-id",
        action="append",
        help="Hermes site id(s) to listen for (default: all)",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Print DEBUG messages to the console"
    )
    parser.add_argument(
        "--log-format",
        default="[%(levelname)s:%(asctime)s] %(name)s: %(message)s",
        help="Python logger format",
    )


def setup_logging(args: argparse.Namespace):
    """Set up Python logging."""
    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format=args.log_format)
    else:
        logging.basicConfig(level=logging.INFO, format=args.log_format)


def connect(client: mqtt.Client, args: argparse.Namespace):
    """Connect to MQTT broker."""
    if args.username:
        client.username_pw_set(args.username, args.password)

    client.connect(args.host, args.port)
