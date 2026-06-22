from unicommerce.models.base import UnicommerceResponse
from unicommerce.models.fulfillment import (
    CreateInvoiceAndLabelResponse,
    CreateShippingPackageResponse,
    GetInvoiceDetailResponse,
    InvoiceLabelResponse,
    ShippingManifestResponse,
    ShippingPackageResponse,
    ShippingPackageSearchResponse,
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

    async def search_shipping_packages(
        self, **filters,
    ) -> ShippingPackageSearchResponse:
        return await self._transport.request(
            path="/oms/shippingPackage/search",
            body=filters,
            response_model=ShippingPackageSearchResponse,
            safe_to_retry=True,
        )

    async def edit_shipping_package(
        self, *, shipping_package_code: str, **kwargs,
    ) -> UnicommerceResponse:
        return await self._transport.request(
            path="/oms/shippingPackage/edit",
            body={"shippingPackageCode": shipping_package_code, **kwargs},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def split_shipping_package(
        self, *, shipping_package_code: str, split_packages: list[dict],
    ) -> UnicommerceResponse:
        return await self._transport.request(
            path="/oms/shippingPackage/split",
            body={
                "shippingPackageCode": shipping_package_code,
                "splitPackages": split_packages,
            },
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def modify_shipping_package(
        self, *, sale_order_code: str, sale_order_item_codes: list[str],
    ) -> UnicommerceResponse:
        return await self._transport.request(
            path="/oms/shippingPackage/modify",
            body={
                "saleOrderCode": sale_order_code,
                "saleOrderItemCodes": sale_order_item_codes,
            },
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def get_shipping_packages(
        self, *, status_code: str | None = None,
    ) -> UnicommerceResponse:
        body: dict = {}
        if status_code is not None:
            body["statusCode"] = status_code
        return await self._transport.request(
            path="/oms/shippingPackage/getShippingPackages",
            body=body,
            response_model=UnicommerceResponse,
            safe_to_retry=True,
        )

    async def create_invoice_by_sale_order(
        self, *, sale_order_code: str, sale_order_item_codes: list[str], **kwargs,
    ) -> InvoiceLabelResponse:
        return await self._transport.request(
            path="/invoice/createInvoiceBySaleOrderCode",
            body={
                "saleOrderCode": sale_order_code,
                "saleOrderItemCodes": sale_order_item_codes,
                **kwargs,
            },
            response_model=InvoiceLabelResponse,
            safe_to_retry=False,
        )

    async def create_invoice_with_details(
        self, *, sale_order_code: str, invoice: dict, **kwargs,
    ) -> InvoiceLabelResponse:
        return await self._transport.request(
            path="/createInvoiceWithDetails",
            body={
                "saleOrderCode": sale_order_code,
                "invoice": invoice,
                **kwargs,
            },
            response_model=InvoiceLabelResponse,
            safe_to_retry=False,
        )

    # get_invoice_pdf: GET request returning PDF binary - needs special handling
    # get_shipping_label_pdf: GET request returning PDF binary - needs special handling

    async def check_serviceability(
        self, *, pincode: str, cash_on_delivery: bool,
    ) -> UnicommerceResponse:
        return await self._transport.request(
            path="/oms/saleOrder/getServiceability",
            body={"pincode": pincode, "cashOnDelivery": cash_on_delivery},
            response_model=UnicommerceResponse,
            safe_to_retry=True,
        )

    async def create_invoice_and_allocate_provider(
        self, *, shipping_package_code: str, **kwargs,
    ) -> CreateInvoiceAndLabelResponse:
        return await self._transport.request(
            path="/oms/shippingPackage/createInvoiceAndAllocateShippingProvider",
            body={"shippingPackageCode": shipping_package_code, **kwargs},
            response_model=CreateInvoiceAndLabelResponse,
            safe_to_retry=False,
        )

    async def allocate_shipping_provider(
        self, *, shipping_package_code: str, **kwargs,
    ) -> UnicommerceResponse:
        return await self._transport.request(
            path="/oms/shippingPackage/allocateShippingProvider",
            body={"shippingPackageCode": shipping_package_code, **kwargs},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def add_package_to_manifest(
        self, *, shipping_manifest_code: str, shipping_package_codes: list[str],
    ) -> UnicommerceResponse:
        return await self._transport.request(
            path="/oms/shippingManifest/addShippingPackage",
            body={
                "shippingManifestCode": shipping_manifest_code,
                "shippingPackageCodes": shipping_package_codes,
            },
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def create_and_close_manifest(
        self, **kwargs,
    ) -> UnicommerceResponse:
        return await self._transport.request(
            path="/oms/shippingManifest/createclose",
            body=kwargs,
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def close_manifest(
        self, *, shipping_manifest_code: str,
    ) -> UnicommerceResponse:
        return await self._transport.request(
            path="/oms/shippingManifest/close",
            body={"shippingManifestCode": shipping_manifest_code},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def dispatch(
        self, *, shipping_package_code: str,
    ) -> UnicommerceResponse:
        return await self._transport.request(
            path="/oms/shippingPackage/dispatch",
            body={"shippingPackageCode": shipping_package_code},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def force_dispatch(
        self, *, shipping_package_code: str, **kwargs,
    ) -> UnicommerceResponse:
        return await self._transport.request(
            path="/oms/shippingPackage/forceDispatch",
            body={"shippingPackageCode": shipping_package_code, **kwargs},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def create_and_dispatch(
        self,
        *,
        sale_order_code: str,
        sale_order_item_info: list[dict],
        shipping_package_info: dict,
        invoice_info: dict | None = None,
    ) -> UnicommerceResponse:
        body: dict = {
            "saleOrderCode": sale_order_code,
            "saleOrderItemInfo": sale_order_item_info,
            "shippingPackageInfo": shipping_package_info,
        }
        if invoice_info is not None:
            body["invoiceInfo"] = invoice_info
        return await self._transport.request(
            path="/oms/shippingPackage/createAndDispatchBySaleOrderItemCode",
            body=body,
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def mark_delivered(
        self,
        *,
        sale_order_code: str,
        sale_order_item_codes: list[str],
        pod_code: str | None = None,
    ) -> UnicommerceResponse:
        body: dict = {
            "saleOrderCode": sale_order_code,
            "saleOrderItemCodes": sale_order_item_codes,
        }
        if pod_code is not None:
            body["podCode"] = pod_code
        return await self._transport.request(
            path="/saleOrderItem/markDelivered",
            body=body,
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def create_picklist(
        self,
        *,
        shipping_package_codes: list[str],
        destination: str | None = None,
    ) -> UnicommerceResponse:
        if destination is not None:
            path = "/oms/picker/picklist/manual/create"
            body: dict = {
                "shippingPackageCodes": shipping_package_codes,
                "destination": destination,
            }
        else:
            path = "/oms/picker/picklist/staging/manual/create"
            body = {"shippingPackageCodes": shipping_package_codes}
        return await self._transport.request(
            path=path,
            body=body,
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def create_or_update_reason(
        self, *, name: str, value: str,
    ) -> UnicommerceResponse:
        return await self._transport.request(
            path="/uiCustomList/createOrUpdate",
            body={"name": name, "value": value},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def update_seal_id(
        self,
        *,
        shipping_package_code: str,
        shipping_package_type_code: str,
        spt_item_seal_id: str,
        shipment_actual_weight_calculation_required: bool | None = None,
    ) -> UnicommerceResponse:
        body: dict = {
            "shippingPackageCode": shipping_package_code,
            "shippingPackageTypeCode": shipping_package_type_code,
            "sptItemSealId": spt_item_seal_id,
        }
        if shipment_actual_weight_calculation_required is not None:
            body["shipmentActualWeightCalculationRequired"] = (
                shipment_actual_weight_calculation_required
            )
        return await self._transport.request(
            path="/package/update",
            body=body,
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def update_seal_id_bulk(
        self, *, packages: list[dict],
    ) -> UnicommerceResponse:
        return await self._transport.request(
            path="/package/updateMultiple",
            body={"packages": packages},
            response_model=UnicommerceResponse,
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

    def search_shipping_packages(
        self, **filters,
    ) -> ShippingPackageSearchResponse:
        return self._transport.request(
            path="/oms/shippingPackage/search",
            body=filters,
            response_model=ShippingPackageSearchResponse,
            safe_to_retry=True,
        )

    def edit_shipping_package(
        self, *, shipping_package_code: str, **kwargs,
    ) -> UnicommerceResponse:
        return self._transport.request(
            path="/oms/shippingPackage/edit",
            body={"shippingPackageCode": shipping_package_code, **kwargs},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def split_shipping_package(
        self, *, shipping_package_code: str, split_packages: list[dict],
    ) -> UnicommerceResponse:
        return self._transport.request(
            path="/oms/shippingPackage/split",
            body={
                "shippingPackageCode": shipping_package_code,
                "splitPackages": split_packages,
            },
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def modify_shipping_package(
        self, *, sale_order_code: str, sale_order_item_codes: list[str],
    ) -> UnicommerceResponse:
        return self._transport.request(
            path="/oms/shippingPackage/modify",
            body={
                "saleOrderCode": sale_order_code,
                "saleOrderItemCodes": sale_order_item_codes,
            },
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def get_shipping_packages(
        self, *, status_code: str | None = None,
    ) -> UnicommerceResponse:
        body: dict = {}
        if status_code is not None:
            body["statusCode"] = status_code
        return self._transport.request(
            path="/oms/shippingPackage/getShippingPackages",
            body=body,
            response_model=UnicommerceResponse,
            safe_to_retry=True,
        )

    def create_invoice_by_sale_order(
        self, *, sale_order_code: str, sale_order_item_codes: list[str], **kwargs,
    ) -> InvoiceLabelResponse:
        return self._transport.request(
            path="/invoice/createInvoiceBySaleOrderCode",
            body={
                "saleOrderCode": sale_order_code,
                "saleOrderItemCodes": sale_order_item_codes,
                **kwargs,
            },
            response_model=InvoiceLabelResponse,
            safe_to_retry=False,
        )

    def create_invoice_with_details(
        self, *, sale_order_code: str, invoice: dict, **kwargs,
    ) -> InvoiceLabelResponse:
        return self._transport.request(
            path="/createInvoiceWithDetails",
            body={
                "saleOrderCode": sale_order_code,
                "invoice": invoice,
                **kwargs,
            },
            response_model=InvoiceLabelResponse,
            safe_to_retry=False,
        )

    # get_invoice_pdf: GET request returning PDF binary - needs special handling
    # get_shipping_label_pdf: GET request returning PDF binary - needs special handling

    def check_serviceability(
        self, *, pincode: str, cash_on_delivery: bool,
    ) -> UnicommerceResponse:
        return self._transport.request(
            path="/oms/saleOrder/getServiceability",
            body={"pincode": pincode, "cashOnDelivery": cash_on_delivery},
            response_model=UnicommerceResponse,
            safe_to_retry=True,
        )

    def create_invoice_and_allocate_provider(
        self, *, shipping_package_code: str, **kwargs,
    ) -> CreateInvoiceAndLabelResponse:
        return self._transport.request(
            path="/oms/shippingPackage/createInvoiceAndAllocateShippingProvider",
            body={"shippingPackageCode": shipping_package_code, **kwargs},
            response_model=CreateInvoiceAndLabelResponse,
            safe_to_retry=False,
        )

    def allocate_shipping_provider(
        self, *, shipping_package_code: str, **kwargs,
    ) -> UnicommerceResponse:
        return self._transport.request(
            path="/oms/shippingPackage/allocateShippingProvider",
            body={"shippingPackageCode": shipping_package_code, **kwargs},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def add_package_to_manifest(
        self, *, shipping_manifest_code: str, shipping_package_codes: list[str],
    ) -> UnicommerceResponse:
        return self._transport.request(
            path="/oms/shippingManifest/addShippingPackage",
            body={
                "shippingManifestCode": shipping_manifest_code,
                "shippingPackageCodes": shipping_package_codes,
            },
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def create_and_close_manifest(
        self, **kwargs,
    ) -> UnicommerceResponse:
        return self._transport.request(
            path="/oms/shippingManifest/createclose",
            body=kwargs,
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def close_manifest(
        self, *, shipping_manifest_code: str,
    ) -> UnicommerceResponse:
        return self._transport.request(
            path="/oms/shippingManifest/close",
            body={"shippingManifestCode": shipping_manifest_code},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def dispatch(
        self, *, shipping_package_code: str,
    ) -> UnicommerceResponse:
        return self._transport.request(
            path="/oms/shippingPackage/dispatch",
            body={"shippingPackageCode": shipping_package_code},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def force_dispatch(
        self, *, shipping_package_code: str, **kwargs,
    ) -> UnicommerceResponse:
        return self._transport.request(
            path="/oms/shippingPackage/forceDispatch",
            body={"shippingPackageCode": shipping_package_code, **kwargs},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def create_and_dispatch(
        self,
        *,
        sale_order_code: str,
        sale_order_item_info: list[dict],
        shipping_package_info: dict,
        invoice_info: dict | None = None,
    ) -> UnicommerceResponse:
        body: dict = {
            "saleOrderCode": sale_order_code,
            "saleOrderItemInfo": sale_order_item_info,
            "shippingPackageInfo": shipping_package_info,
        }
        if invoice_info is not None:
            body["invoiceInfo"] = invoice_info
        return self._transport.request(
            path="/oms/shippingPackage/createAndDispatchBySaleOrderItemCode",
            body=body,
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def mark_delivered(
        self,
        *,
        sale_order_code: str,
        sale_order_item_codes: list[str],
        pod_code: str | None = None,
    ) -> UnicommerceResponse:
        body: dict = {
            "saleOrderCode": sale_order_code,
            "saleOrderItemCodes": sale_order_item_codes,
        }
        if pod_code is not None:
            body["podCode"] = pod_code
        return self._transport.request(
            path="/saleOrderItem/markDelivered",
            body=body,
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def create_picklist(
        self,
        *,
        shipping_package_codes: list[str],
        destination: str | None = None,
    ) -> UnicommerceResponse:
        if destination is not None:
            path = "/oms/picker/picklist/manual/create"
            body: dict = {
                "shippingPackageCodes": shipping_package_codes,
                "destination": destination,
            }
        else:
            path = "/oms/picker/picklist/staging/manual/create"
            body = {"shippingPackageCodes": shipping_package_codes}
        return self._transport.request(
            path=path,
            body=body,
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def create_or_update_reason(
        self, *, name: str, value: str,
    ) -> UnicommerceResponse:
        return self._transport.request(
            path="/uiCustomList/createOrUpdate",
            body={"name": name, "value": value},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def update_seal_id(
        self,
        *,
        shipping_package_code: str,
        shipping_package_type_code: str,
        spt_item_seal_id: str,
        shipment_actual_weight_calculation_required: bool | None = None,
    ) -> UnicommerceResponse:
        body: dict = {
            "shippingPackageCode": shipping_package_code,
            "shippingPackageTypeCode": shipping_package_type_code,
            "sptItemSealId": spt_item_seal_id,
        }
        if shipment_actual_weight_calculation_required is not None:
            body["shipmentActualWeightCalculationRequired"] = (
                shipment_actual_weight_calculation_required
            )
        return self._transport.request(
            path="/package/update",
            body=body,
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def update_seal_id_bulk(
        self, *, packages: list[dict],
    ) -> UnicommerceResponse:
        return self._transport.request(
            path="/package/updateMultiple",
            body={"packages": packages},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )
