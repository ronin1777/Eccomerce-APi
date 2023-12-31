from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from treebeard.mp_tree import MP_Node

from shop.apps.catalog.manager import CategoryQuerySet
from shop.libs.db.fields import UpperCaseCharField
from shop.libs.db.model import AuditableModel
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError




# Create your models here.
class Category(MP_Node):
    title = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=2048, null=True, blank=True)
    is_public = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    objects = CategoryQuerySet.as_manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class OptionGroup(models.Model):
    title = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Option Group"
        verbose_name_plural = "Option Groups"


class OptionGroupValue(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    group = models.ForeignKey(OptionGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Option Group Value"
        verbose_name_plural = "Option Group Values"


class ProductClass(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=2048, null=True, blank=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    track_stock = models.BooleanField(default=True)
    require_shipping = models.BooleanField(default=True)

    options = models.ManyToManyField('Option', blank=True)

    @property
    def has_attribute(self):
        return self.attributes.exists()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Product Class"
        verbose_name_plural = "Product Classes"


class ProductAttribute(models.Model):
    class AttributeTypeChoice(models.TextChoices):
        text = 'text'
        integer = 'integer'
        float = 'float'
        option = 'option'
        multi_option = 'multi_option'

    product_class = models.ForeignKey(ProductClass, on_delete=models.CASCADE, null=True, related_name='attributes')
    title = models.CharField(max_length=64)
    type = models.CharField(max_length=16, choices=AttributeTypeChoice.choices, default=AttributeTypeChoice.text)
    option_group = models.ForeignKey(OptionGroup, on_delete=models.PROTECT, null=True, blank=True)
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Product Attribute"
        verbose_name_plural = "Product Attributes"


class Option(models.Model):
    class OptionTypeChoice(models.TextChoices):
        text = 'text'
        integer = 'integer'
        float = 'float'
        option = 'option'
        multi_option = 'multi_option'

    title = models.CharField(max_length=64)
    type = models.CharField(max_length=16, choices=OptionTypeChoice.choices, default=OptionTypeChoice.text)
    option_group = models.ForeignKey(OptionGroup, on_delete=models.PROTECT, null=True, blank=True)
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Option"
        verbose_name_plural = "Option"

class AvailabilityStatuses:
    in_stock = (1, 'in stock')
    awaiting_arrival = (2, 'awaiting arrival')
    low_in_stock = (3, 'low in stock')
    out_of_stock = (4, 'out of stock')


class Product(AuditableModel):
    AVAILABILITY_STATUSES = (
        AvailabilityStatuses.in_stock,
        AvailabilityStatuses.awaiting_arrival,
        AvailabilityStatuses.low_in_stock,
        AvailabilityStatuses.out_of_stock
    )
    class ProductTypeChoice(models.TextChoices):
        standalone = 'standalone'
        parent = 'parent'
        child = 'child'

    availability_status = models.IntegerField(default=1, choices=AVAILABILITY_STATUSES)
    structure = models.CharField(max_length=16, choices=ProductTypeChoice.choices, default=ProductTypeChoice.standalone)
    parent = models.ForeignKey("self", related_name="children", on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=128, null=True, blank=True)
    upc = UpperCaseCharField(max_length=24, unique=True, null=True, blank=True, help_text=_())
    is_public = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=128, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    rating = GenericRelation(Rating)
    slug = models.SlugField(unique=True, allow_unicode=True)
    price = models.IntegerField()


    product_class = models.ForeignKey(ProductClass, on_delete=models.PROTECT, null=True, blank=True,
                                      related_name='products')
    attributes = models.ManyToManyField(ProductAttribute, through='ProductAttributeValue')
    recommended_products = models.ManyToManyField('catalog.Product', through='ProductRecommendation', blank=True)
    categories = models.ManyToManyField(Category, related_name='categories')
    product_options = models.ManyToManyField(Option, blank=True)


    def _clean_standalone(self):
        """
        Validates a stand-alone product
        """
        if not self.product_class:
            raise ValidationError(_("Your product must have a product class."))
        if self.parent_id:
            raise ValidationError(_("Only child products can have a parent."))

    def _clean_child(self):
        """
        Validates a child product
        """
        if not self.parent_id:
            raise ValidationError(_("A child product needs a parent."))
        if self.parent_id and not self.parent.is_parent:
            raise ValidationError(
                _("You can only assign child products to parent products.")
            )
        if self.product_class:
            raise ValidationError(_("A child product can't have a product class."))
        if self.pk and self.categories.exists():
            raise ValidationError(_("A child product can't have a category assigned."))
        if self.pk and self.product_options.exists():
            raise ValidationError(_("A child product can't have options."))

    def _clean_parent(self):
        """
        Validates a parent product.
        """
        self._clean_standalone()
        if self.has_stockrecords:
            raise ValidationError(_("A parent product can't have stockrecords."))


    @property
    def main_image(self):
        if self.images.exists():
            return self.images.first()
        else:
            return None

    @property
    def avg_rating(self):
        ratings = Rating.objects.filter(content_type__model='product', object_id=self.id)
        if ratings.exists():
            total_ratings = sum(rating.rating for rating in ratings)
            return total_ratings / ratings.count()
        return 0

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    @property
    def num_stockrecords(self):
        return self.stock_records.count()

    @property
    def has_stockrecords(self):
        """
        Test if this product has any stockrecords
        """
        if self.id:
            return self.stock_records.exists()
        return False


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)

    value_text = models.TextField(null=True, blank=True)
    value_integer = models.IntegerField(null=True, blank=True)
    value_float = models.FloatField(null=True, blank=True)
    value_option = models.ForeignKey(OptionGroupValue, on_delete=models.PROTECT, null=True, blank=True)
    value_multi_option = models.ManyToManyField(OptionGroupValue, blank=True,
                                                related_name='multi_valued_attribute_value')

    class Meta:
        verbose_name = "Attribute Value"
        verbose_name_plural = "Attribute Values"
        unique_together = ('product', 'attribute')


class ProductRecommendation(models.Model):
    primary = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='primary_recommendation')
    recommendation = models.ForeignKey(Product, on_delete=models.CASCADE)
    rank = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ('primary', 'recommendation')
        ordering = ('primary', '-rank')


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ForeignKey('media.Image', on_delete=models.PROTECT)

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('display_order',)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

        for index, image in enumerate(self.product.images.all()):
            image.display_order = index
            image.save()
