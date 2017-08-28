#!/usr/bin/env python3
import asyncio
from src import gateway

loop = asyncio.get_event_loop()
loop.run_until_complete(gateway.run())
loop.close()