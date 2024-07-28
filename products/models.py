from django.db import models
from categories.models import Category
from suppliers.models import Supplier
from .utils import check_product_status

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    expiry_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField()#auto_now_add=True
    updated_at = models.DateTimeField(auto_now=True)
    low_stock_threshold = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.name

    def get_status(self):
        return check_product_status(self)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.supplier.update_last_active()

    def delete(self, *args, **kwargs):
        supplier = self.supplier
        super().delete(*args, **kwargs)
        supplier.update_last_active()