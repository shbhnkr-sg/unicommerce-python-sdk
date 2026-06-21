from unicommerce.transport.async_transport import AsyncTransport
from unicommerce.transport.sync_transport import SyncTransport


class BaseResource:
    def __init__(self, transport: SyncTransport):
        self._transport = transport


class AsyncBaseResource:
    def __init__(self, transport: AsyncTransport):
        self._transport = transport
