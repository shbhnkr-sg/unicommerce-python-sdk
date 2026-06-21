from unicommerce.config import UnicommerceConfig
from unicommerce.auth import AuthManager
from unicommerce.transport import AsyncTransport
from unicommerce.resources.sale_orders import AsyncSaleOrders
from unicommerce.resources.inventory import AsyncInventory
from unicommerce.resources.products import AsyncProducts
from unicommerce.resources.fulfillment import AsyncFulfillment
from unicommerce.resources.inbound import AsyncInbound
from unicommerce.resources.returns import AsyncReturns
from unicommerce.resources.facilities import AsyncFacilities
from unicommerce.resources.export_jobs import AsyncExportJobs


class AsyncUnicommerce:
    def __init__(self, tenant: str, username: str, password: str, **kwargs):
        self._config = UnicommerceConfig(tenant=tenant, username=username, password=password, **kwargs)
        self._auth = AuthManager(self._config)
        self._transport = AsyncTransport(self._config, self._auth)

        self.sale_orders = AsyncSaleOrders(self._transport)
        self.inventory = AsyncInventory(self._transport)
        self.products = AsyncProducts(self._transport)
        self.fulfillment = AsyncFulfillment(self._transport)
        self.inbound = AsyncInbound(self._transport)
        self.returns = AsyncReturns(self._transport)
        self.facilities = AsyncFacilities(self._transport)
        self.export_jobs = AsyncExportJobs(self._transport)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.close()

    async def close(self):
        await self._transport.close()
