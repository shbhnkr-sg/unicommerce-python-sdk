from unicommerce.models.fulfillment import (
    InvoiceResponse,
    ShippingManifestResponse,
    ShippingPackageResponse,
    TrackShipmentResponse,
)
from unicommerce.resources.base import AsyncBaseResource, BaseResource


class AsyncFulfillment(AsyncBaseResource):
    async def create_invoice(self, shipping_package_code: str) -> InvoiceResponse:
        return await self._transport.request(
            path="/oms/shippingPackage/createInvoice",
            body={"shippingPackageCode": shipping_package_code},
            response_model=InvoiceResponse,
            safe_to_retry=False,
        )

    async def get_invoice(self, invoice_code: str) -> InvoiceResponse:
        return await self._transport.request(
            path="/oms/shippingPackage/getInvoice",
            body={"invoiceCode": invoice_code},
            response_model=InvoiceResponse,
            safe_to_retry=True,
        )

    async def create_shipping_package(
        self, sale_order_code: str, items: list
    ) -> ShippingPackageResponse:
        return await self._transport.request(
            path="/oms/shippingPackage/create",
            body={"saleOrderCode": sale_order_code, "items": items},
            response_model=ShippingPackageResponse,
            safe_to_retry=False,
        )

    async def get_shipping_package(self, shipping_package_code: str) -> ShippingPackageResponse:
        return await self._transport.request(
            path="/oms/shippingPackage/getShippingPackageDetails",
            body={"shippingPackageCode": shipping_package_code},
            response_model=ShippingPackageResponse,
            dto_key="shippingPackageDetailDTO",
            safe_to_retry=True,
        )

    async def create_manifest(
        self, channel: str, shipping_provider: str
    ) -> ShippingManifestResponse:
        return await self._transport.request(
            path="/oms/shippingManifest/create",
            body={"channel": channel, "shippingProvider": shipping_provider},
            response_model=ShippingManifestResponse,
            safe_to_retry=False,
        )

    async def get_manifest(self, code: str) -> ShippingManifestResponse:
        return await self._transport.request(
            path="/oms/shippingManifest/get",
            body={"code": code},
            response_model=ShippingManifestResponse,
            safe_to_retry=True,
        )

    async def track_shipment(self, tracking_number: str) -> TrackShipmentResponse:
        return await self._transport.request(
            path="/oms/shipment/track",
            body={"trackingNumber": tracking_number},
            response_model=TrackShipmentResponse,
            safe_to_retry=True,
        )

    async def create_label(self, shipping_package_code: str) -> ShippingPackageResponse:
        return await self._transport.request(
            path="/oms/shippingPackage/createLabel",
            body={"shippingPackageCode": shipping_package_code},
            response_model=ShippingPackageResponse,
            safe_to_retry=False,
        )


class Fulfillment(BaseResource):
    def create_invoice(self, shipping_package_code: str) -> InvoiceResponse:
        return self._transport.request(
            path="/oms/shippingPackage/createInvoice",
            body={"shippingPackageCode": shipping_package_code},
            response_model=InvoiceResponse,
            safe_to_retry=False,
        )

    def get_invoice(self, invoice_code: str) -> InvoiceResponse:
        return self._transport.request(
            path="/oms/shippingPackage/getInvoice",
            body={"invoiceCode": invoice_code},
            response_model=InvoiceResponse,
            safe_to_retry=True,
        )

    def create_shipping_package(self, sale_order_code: str, items: list) -> ShippingPackageResponse:
        return self._transport.request(
            path="/oms/shippingPackage/create",
            body={"saleOrderCode": sale_order_code, "items": items},
            response_model=ShippingPackageResponse,
            safe_to_retry=False,
        )

    def get_shipping_package(self, shipping_package_code: str) -> ShippingPackageResponse:
        return self._transport.request(
            path="/oms/shippingPackage/getShippingPackageDetails",
            body={"shippingPackageCode": shipping_package_code},
            response_model=ShippingPackageResponse,
            dto_key="shippingPackageDetailDTO",
            safe_to_retry=True,
        )

    def create_manifest(self, channel: str, shipping_provider: str) -> ShippingManifestResponse:
        return self._transport.request(
            path="/oms/shippingManifest/create",
            body={"channel": channel, "shippingProvider": shipping_provider},
            response_model=ShippingManifestResponse,
            safe_to_retry=False,
        )

    def get_manifest(self, code: str) -> ShippingManifestResponse:
        return self._transport.request(
            path="/oms/shippingManifest/get",
            body={"code": code},
            response_model=ShippingManifestResponse,
            safe_to_retry=True,
        )

    def track_shipment(self, tracking_number: str) -> TrackShipmentResponse:
        return self._transport.request(
            path="/oms/shipment/track",
            body={"trackingNumber": tracking_number},
            response_model=TrackShipmentResponse,
            safe_to_retry=True,
        )

    def create_label(self, shipping_package_code: str) -> ShippingPackageResponse:
        return self._transport.request(
            path="/oms/shippingPackage/createLabel",
            body={"shippingPackageCode": shipping_package_code},
            response_model=ShippingPackageResponse,
            safe_to_retry=False,
        )
