from unicommerce.models.fulfillment import (
    CreateInvoiceAndLabelResponse,
    CreateShippingPackageResponse,
    GetInvoiceDetailResponse,
    InvoiceLabelResponse,
    ShippingManifestResponse,
    ShippingPackageResponse,
    UpdateTrackingStatusResponse,
)
from unicommerce.resources.base import AsyncBaseResource, BaseResource


class AsyncFulfillment(AsyncBaseResource):
    async def create_invoice(
        self, *, shipping_package_code: str
    ) -> InvoiceLabelResponse:
        return await self._transport.request(
            path="/oms/shippingPackage/createInvoice",
            body={"shippingPackageCode": shipping_package_code},
            response_model=InvoiceLabelResponse,
            safe_to_retry=False,
        )

    async def get_invoice_details(
        self,
        *,
        shipping_package_code: str,
        is_return: bool = False,
        payment_detail_required: bool = False,
    ) -> GetInvoiceDetailResponse:
        return await self._transport.request(
            path="/invoice/details/get",
            body={
                "shippingPackageCode": shipping_package_code,
                "return": is_return,
                "paymentDetailRequired": payment_detail_required,
            },
            response_model=GetInvoiceDetailResponse,
            safe_to_retry=True,
        )

    async def get_invoice_label(
        self, *, shipping_package_code: str
    ) -> InvoiceLabelResponse:
        return await self._transport.request(
            path="/oms/shippingPackage/getInvoiceLabel",
            body={"shippingPackageCode": shipping_package_code},
            response_model=InvoiceLabelResponse,
            safe_to_retry=True,
        )

    async def create_invoice_and_label(
        self,
        *,
        shipping_package_code: str,
        generate_uniware_shipping_label: bool = True,
    ) -> CreateInvoiceAndLabelResponse:
        return await self._transport.request(
            path="/oms/shippingPackage/createInvoiceAndGenerateLabel",
            body={
                "shippingPackageCode": shipping_package_code,
                "generateUniwareShippingLabel": generate_uniware_shipping_label,
            },
            response_model=CreateInvoiceAndLabelResponse,
            safe_to_retry=False,
        )

    async def create_shipping_package(
        self, *, sale_order_code: str, sale_order_item_codes: list[str]
    ) -> CreateShippingPackageResponse:
        return await self._transport.request(
            path="/oms/shippingPackage/create",
            body={
                "saleOrderCode": sale_order_code,
                "saleOrderItemCodes": sale_order_item_codes,
            },
            response_model=CreateShippingPackageResponse,
            safe_to_retry=False,
        )

    async def get_shipping_package(
        self, *, shipping_package_code: str
    ) -> ShippingPackageResponse:
        return await self._transport.request(
            path="/oms/shippingPackage/getShippingPackageDetails",
            body={"shippingPackageCode": shipping_package_code},
            response_model=ShippingPackageResponse,
            dto_key="shippingPackageDetailDTO",
            safe_to_retry=True,
        )

    async def create_manifest(
        self,
        *,
        channel: str,
        third_party_shipping: bool,
        shipping_provider_code: str | None = None,
        **kwargs,
    ) -> ShippingManifestResponse:
        body: dict = {"channel": channel, "thirdPartyShipping": third_party_shipping, **kwargs}
        if shipping_provider_code is not None:
            body["shippingProviderCode"] = shipping_provider_code
        return await self._transport.request(
            path="/oms/shippingManifest/create",
            body=body,
            response_model=ShippingManifestResponse,
            safe_to_retry=False,
        )

    async def get_manifest(
        self, *, shipping_manifest_code: str
    ) -> ShippingManifestResponse:
        return await self._transport.request(
            path="/oms/shippingManifest/get",
            body={"shippingManifestCode": shipping_manifest_code},
            response_model=ShippingManifestResponse,
            dto_key="shippingManifest",
            safe_to_retry=True,
        )

    async def update_tracking_status(
        self,
        *,
        provider_code: str,
        tracking_number: str,
        tracking_status: str,
        status_date: str | None = None,
        shipment_tracking_status_name: str | None = None,
        rto_tracking_number: str | None = None,
        rto_reason: str | None = None,
    ) -> UpdateTrackingStatusResponse:
        body: dict = {
            "providerCode": provider_code,
            "trackingNumber": tracking_number,
            "trackingStatus": tracking_status,
        }
        if status_date is not None:
            body["statusDate"] = status_date
        if shipment_tracking_status_name is not None:
            body["shipmentTrackingStatusName"] = shipment_tracking_status_name
        if rto_tracking_number is not None:
            body["rtoTrackingNumber"] = rto_tracking_number
        if rto_reason is not None:
            body["rtoReason"] = rto_reason
        return await self._transport.request(
            path="/oms/updateShipmentTrackingStatus",
            body=body,
            response_model=UpdateTrackingStatusResponse,
            safe_to_retry=False,
        )


class Fulfillment(BaseResource):
    def create_invoice(
        self, *, shipping_package_code: str
    ) -> InvoiceLabelResponse:
        return self._transport.request(
            path="/oms/shippingPackage/createInvoice",
            body={"shippingPackageCode": shipping_package_code},
            response_model=InvoiceLabelResponse,
            safe_to_retry=False,
        )

    def get_invoice_details(
        self,
        *,
        shipping_package_code: str,
        is_return: bool = False,
        payment_detail_required: bool = False,
    ) -> GetInvoiceDetailResponse:
        return self._transport.request(
            path="/invoice/details/get",
            body={
                "shippingPackageCode": shipping_package_code,
                "return": is_return,
                "paymentDetailRequired": payment_detail_required,
            },
            response_model=GetInvoiceDetailResponse,
            safe_to_retry=True,
        )

    def get_invoice_label(
        self, *, shipping_package_code: str
    ) -> InvoiceLabelResponse:
        return self._transport.request(
            path="/oms/shippingPackage/getInvoiceLabel",
            body={"shippingPackageCode": shipping_package_code},
            response_model=InvoiceLabelResponse,
            safe_to_retry=True,
        )

    def create_invoice_and_label(
        self,
        *,
        shipping_package_code: str,
        generate_uniware_shipping_label: bool = True,
    ) -> CreateInvoiceAndLabelResponse:
        return self._transport.request(
            path="/oms/shippingPackage/createInvoiceAndGenerateLabel",
            body={
                "shippingPackageCode": shipping_package_code,
                "generateUniwareShippingLabel": generate_uniware_shipping_label,
            },
            response_model=CreateInvoiceAndLabelResponse,
            safe_to_retry=False,
        )

    def create_shipping_package(
        self, *, sale_order_code: str, sale_order_item_codes: list[str]
    ) -> CreateShippingPackageResponse:
        return self._transport.request(
            path="/oms/shippingPackage/create",
            body={
                "saleOrderCode": sale_order_code,
                "saleOrderItemCodes": sale_order_item_codes,
            },
            response_model=CreateShippingPackageResponse,
            safe_to_retry=False,
        )

    def get_shipping_package(
        self, *, shipping_package_code: str
    ) -> ShippingPackageResponse:
        return self._transport.request(
            path="/oms/shippingPackage/getShippingPackageDetails",
            body={"shippingPackageCode": shipping_package_code},
            response_model=ShippingPackageResponse,
            dto_key="shippingPackageDetailDTO",
            safe_to_retry=True,
        )

    def create_manifest(
        self,
        *,
        channel: str,
        third_party_shipping: bool,
        shipping_provider_code: str | None = None,
        **kwargs,
    ) -> ShippingManifestResponse:
        body: dict = {"channel": channel, "thirdPartyShipping": third_party_shipping, **kwargs}
        if shipping_provider_code is not None:
            body["shippingProviderCode"] = shipping_provider_code
        return self._transport.request(
            path="/oms/shippingManifest/create",
            body=body,
            response_model=ShippingManifestResponse,
            safe_to_retry=False,
        )

    def get_manifest(
        self, *, shipping_manifest_code: str
    ) -> ShippingManifestResponse:
        return self._transport.request(
            path="/oms/shippingManifest/get",
            body={"shippingManifestCode": shipping_manifest_code},
            response_model=ShippingManifestResponse,
            dto_key="shippingManifest",
            safe_to_retry=True,
        )

    def update_tracking_status(
        self,
        *,
        provider_code: str,
        tracking_number: str,
        tracking_status: str,
        status_date: str | None = None,
        shipment_tracking_status_name: str | None = None,
        rto_tracking_number: str | None = None,
        rto_reason: str | None = None,
    ) -> UpdateTrackingStatusResponse:
        body: dict = {
            "providerCode": provider_code,
            "trackingNumber": tracking_number,
            "trackingStatus": tracking_status,
        }
        if status_date is not None:
            body["statusDate"] = status_date
        if shipment_tracking_status_name is not None:
            body["shipmentTrackingStatusName"] = shipment_tracking_status_name
        if rto_tracking_number is not None:
            body["rtoTrackingNumber"] = rto_tracking_number
        if rto_reason is not None:
            body["rtoReason"] = rto_reason
        return self._transport.request(
            path="/oms/updateShipmentTrackingStatus",
            body=body,
            response_model=UpdateTrackingStatusResponse,
            safe_to_retry=False,
        )
