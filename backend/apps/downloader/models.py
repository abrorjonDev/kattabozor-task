from django.db import models
from django.forms import model_to_dict
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    _id = models.IntegerField(_('Kattabozor server ID'), db_index=True)
    name = models.CharField(_("Name"), max_length=255)
    brand = models.CharField(_("Brand"), max_length=255)
    category = models.CharField(_("Category"), max_length=500)
    merchant = models.CharField(_("Merchant"), max_length=255, default='')

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self) -> str:
        return self.name

    @property
    def attribute_qs(self):
        return self.attributes.values('name', 'value')

    @property
    def image_data(self):
        return model_to_dict(self.image, exclude=('id', 'product'))


class Attribute(models.Model):
    product = models.ForeignKey("downloader.Product", models.CASCADE, related_name='attributes', db_index=True)
    name = models.CharField(_("Name"), max_length=255)
    value = models.CharField(_("Value"), max_length=255)

    def __str__(self) -> str:
        return "%s: %s - %s" % (self.product, self.name, self.value)


class ImageModel(models.Model):
    width = models.IntegerField(_("Width"), default=0)
    height = models.IntegerField(_("Height"), default=0)
    url = models.URLField(_("URL")) # I easyly used URLField, not ImageField
    product = models.OneToOneField("downloader.Product", models.CASCADE, related_name='image', db_index=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self) -> str:
        return str(self.product)
