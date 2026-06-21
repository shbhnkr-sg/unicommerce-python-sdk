from unicommerce.config import UnicommerceConfig
from unicommerce.auth import AuthManager
from unicommerce.transport import SyncTransport
from unicommerce.resources.sale_orders import SaleOrders
from unicommerce.resources.inventory import Inventory
from unicommerce.resources.products import Products
from unicommerce.resources.fulfillment import Fulfillment
from unicommerce.resources.inbound import Inbound
from unicommerce.resources.returns import Returns
from unicommerce.resources.facilities import Facilities
from unicommerce.resources.export_jobs import ExportJobs


class Unicommerce:
    def __init__(self, tenant: str, username: str, password: str, **kwargs):
        self._config = UnicommerceConfig(tenant=tenant, username=username, password=password, **kwargs)
        self._auth = AuthManager(self._config)
        self._transport = SyncTransport(self._config, self._auth)

        self.sale_orders = SaleOrders(self._transport)
        self.inventory = Inventory(self._transport)
        self.products = Products(self._transport)
        self.fulfillment = Fulfillment(self._transport)
        self.inbound = Inbound(self._transport)
        self.returns = Returns(self._transport)
        self.facilities = Facilities(self._transport)
        self.export_jobs = ExportJobs(self._transport)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def close(self):
        self._transport.close()
