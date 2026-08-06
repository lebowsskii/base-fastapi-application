import asyncio

from loguru import logger

shutdown_event = asyncio.Event()


def handle_shutdown():
    logger.warning("received shutdown signal, setting shutdown_event...")
    shutdown_event.set()
