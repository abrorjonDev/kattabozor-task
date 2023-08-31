from django.contrib import admin

from downloader.models import Product, Attribute, ImageModel


class AttributeInline(admin.TabularInline):
    model = Attribute
    fields = ('id', 'name', 'value')
    extra = 0


class ImageInline(admin.TabularInline):
    model = ImageModel
    fields = ('id', 'width', 'height', 'url')
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [AttributeInline, ImageInline]


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    ...


@admin.register(ImageModel)
class ImageModelAdmin(admin.ModelAdmin):
    ...
