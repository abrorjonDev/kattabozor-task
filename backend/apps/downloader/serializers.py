from rest_framework import serializers

from downloader.models import Product


class ProductReadSerializer(serializers.ModelSerializer):
    attributes = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
    
    def get_attributes(self, instance):
        return instance.attribute_qs
    
    def get_image(self, instance):
        if instance.image_data:
            return instance.image_data

