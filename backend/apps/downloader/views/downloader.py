import requests
import ujson

from typing import Dict, Any, List

from django.conf import settings
from django.db import transaction 
from rest_framework.views import APIView
from rest_framework.response import Response

from downloader.models import Product, Attribute, ImageModel
from downloader.serializers import ProductReadSerializer
from downloader.utils import add_attributes


class DownloaderView(APIView):

    @transaction.atomic
    def get(self, request, *args, **kwargs):

        request_url = settings.REQUEST_URL
        response = requests.get(request_url)

        if response.status_code == 200:

            products_data = self.get_data(response)
            if isinstance(products_data, Response):
                return products_data

            _ids = list(map(lambda product: product['id'], products_data))

            self.check_and_save_new_products(products_data, _ids)

            products = Product.objects.filter(_id__in=_ids).prefetch_related('attributes', 'image')
            serializer = ProductReadSerializer(products, many=True)
            return Response(serializer.data)

        return Response({
            "message": "Error occured while fetching",
            "code": response.status_code,
            "error": response.content
        })

    def get_data(self, response: requests.Response):
        try:
            products_data = ujson.loads(response.content)['offers']
        except ValueError:
            return Response({
                "message": "Response data is malformed",
                "code": 400,
                "status": "RESPONSE_MALFORMED",
            })
        except KeyError:
            return Response({
                "message": "Response data keys are changed",
                "code": 400,
                "status": "RESPONSE_DATA_CHANGED",
            })
        
        return products_data
    
    def check_and_save_new_products(self, products_data: Dict[str, Any], _ids: List[int]) -> None:
        """Checks and saves new products, old saved products don't be updated."""

        # need to use for checking if product has already been saved.
        product_ids = Product.objects.filter(_id__in=_ids).only('_id').values_list('_id', flat=True)

        for product in products_data:
            # I have understood that, I need to download data only, and 
            # no need to update objects all time. 
            if product['id'] in product_ids:
                continue

            attributes = product.pop('attributes', [])
            image = product.pop('image', {})
            product['_id'] = product.pop('id')

            new_product, created = Product.objects.get_or_create(
                **product
            )

            attributes = list(map(lambda attr: add_attributes(new_product, attr), attributes))
            Attribute.objects.bulk_create(attributes)

            if image:
                ImageModel.objects.get_or_create(**image, product=new_product)
