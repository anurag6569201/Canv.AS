from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User

STATUS_CHOICES = (
    ('process', 'Processing'),
    ('shipped', 'Shipped'),
    ('deliver', 'Delivered'),
)

STATUS = (
    ('draft', 'Draft'),
    ('disable', 'Disabled'),
    ('rejected', 'Rejected'),
    ('in_review', 'In Review'),
    ('publish', 'Published'),
)

RATING = (
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★'),
)

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, max_length=22, prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category', default="category.jpg")

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" alt="Category Image" />' % self.image.url)

    def __str__(self):
        return self.title

class Tags(models.Model):
    pass

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, max_length=22, prefix="ven", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="Nestify")
    image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    coverimage = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    description = models.TextField(null=True, blank=True, default="I am a good vendor")
    address = models.CharField(max_length=100, default="District Maihar (485771) Madhya Pradesh")
    contact = models.CharField(max_length=100, default="+91 9098691543")
    chat_response_time = models.CharField(max_length=100, default="100")
    shipping_on_time = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" alt="Vendor Image" />' % self.image.url)

    def __str__(self):
        return self.title

class Product(models.Model):
    pid = ShortUUIDField(unique=True, max_length=22, alphabet="abcdefgh12345")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,related_name="category")
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True,related_name="vendors")
    title = models.CharField(max_length=100, default="Fresh pear")
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    description = models.TextField(null=True, blank=True, default="This is a product")
    delivery_address = models.TextField(null=True, blank=True, default="Near khare mai mandir (485771)")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    specification = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
   
    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True, max_length=10, prefix="sku", alphabet="abcdefgh12345")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" alt="Product Image" />' % self.image.url)

    def __str__(self):
        return self.title

    def get_percentage(self):
        new_price = 100-((self.price / self.old_price) * 100)
        return new_price

class ProductImages(models.Model):
    images = models.ImageField(upload_to="product_images", default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"

class CartOrderItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=200)

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" alt="Order Image" />' % self.image)

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    paid_track = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICES, max_length=30, default="processing")

    class Meta:
        verbose_name_plural = "Cart Orders"

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return self.product.title

    def get_rating(self):
        return self.rating

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlist"

    def __str__(self):
        return self.product.title

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"
