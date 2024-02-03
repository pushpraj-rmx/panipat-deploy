from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from unicodedata import decimal
from pyexpat import model
from email.policy import default
from django.utils.text import slugify
from tinymce.models import HTMLField


STATUS_CHOICE = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

RATING = (
    ("1", "★"),
    ("2", "★★"),
    ("3", "★★★"),
    ("4", "★★★★"),
    ("5", "★★★★★"),
)

COLOR = (
    ("red", "Red"),
    ("black", "Black"),
    ("pink", "Pink"),
    ("blue", "Blue"),
    ("orange", "Orange"),
)

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Main_category(models.Model):
    mid = ShortUUIDField(unique=True, max_length=30, prefix="main_cat", alphabet="abcdefgh12345")
    main_title = models.CharField(max_length=100)
    meta_description = models.CharField(max_length=100)
    meta_title = models.CharField(max_length=100)
    meta_tag = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category",default="maincategory.jpg")
    icon_img = models.ImageField(upload_to="categoryicon",default="maincategoryicon.jpg")

    class Meta:
        verbose_name_plural = "Main Categories"

    def main_category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def main_category_icon_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.icon_img.url))
    
    def get_absolute_url(self):
        return reverse('core:main_category', kwargs={'main_title': str(self.main_title)})
    
    def __str__(self):
        return self.main_title
    
class Category(models.Model):
    cid = ShortUUIDField(unique=True, max_length=30, prefix="cat", alphabet="abcdefgh12345")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    main_category = models.ForeignKey(Main_category, on_delete=models.SET_NULL, null=True)
    cat_title = models.CharField(max_length=100, default="Mobile & Laptop")
    meta_description = models.CharField(max_length=100)
    meta_title = models.CharField(max_length=100)
    meta_tag = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path, default="category.jpg")
    big_image = models.ImageField(upload_to=user_directory_path, default="bigcategory.jpg")


    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def category_big_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.big_image.url))
    
    def get_absolute_url(self):
        return reverse('core:inner-category', kwargs={'cat_title': str(self.cat_title)})
    
    def __str__(self):
        return self.cat_title
    

class Tags(models.Model):
    pass    

class Sub_categories(models.Model):
    ssid = ShortUUIDField(unique=True, max_length=30, prefix="sub_cat", alphabet="abcdefgh12345")   
    maincat = models.ForeignKey(Main_category, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    sub_cat_title = models.CharField(max_length=100, default="Mobile & Laptop")
    slug = models.SlugField(unique=True, max_length=150, blank=True, null=True)
    description = models.CharField(max_length=200)
    page_about_description = models.CharField(max_length=500)
    bottom_page_description = HTMLField()
    canonical_link = models.CharField(max_length=200)
    meta_description = models.CharField(max_length=200)
    meta_title = models.CharField(max_length=200)
    meta_tag = models.CharField(max_length=200)
    meta_robots = models.CharField(max_length=100)
    og_url = models.CharField(max_length=100)
    og_title = models.CharField(max_length=100)
    og_description = models.CharField(max_length=100)
    og_image = models.CharField(max_length=100)
    twitter_title = models.CharField(max_length=100)
    twitter_description = models.CharField(max_length=100)
    twitter_description = models.CharField(max_length=100)
    youtube_link = models.CharField(max_length=1000)
    image = models.ImageField(upload_to=user_directory_path, default="subcategory.jpg")
    main_page_img = models.ImageField(upload_to=user_directory_path, default="mainpageimg.jpg")

    class Meta:
        verbose_name_plural = "Sub Categories"

    def sub_category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def main_page_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.main_page_img.url))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.sub_cat_title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:sub-category', kwargs={'sub_cat_slug': str(self.slug)})
    
    def __str__(self):
        return self.sub_cat_title
    

class SubcategoryImages(models.Model):
    images = models.ImageField(upload_to="sub-categories-images", default="sub-category.jpg")
    sub_category = models.ForeignKey(Sub_categories, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Sub Categories Images"

    
class Company_name(models.Model):
    sid = ShortUUIDField(unique=True, max_length=50, prefix="Company_name", alphabet="abcdefgh12345")   
    maincat = models.ForeignKey(Main_category, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(Sub_categories, on_delete=models.SET_NULL, null=True)
    company_name_title = models.CharField(max_length=100, default="Mobile & Laptop")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    meta_description = models.CharField(max_length=100)
    meta_title = models.CharField(max_length=100)
    meta_tag = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    best_seller = models.BooleanField(default=False)
    curtain_fabric_category = models.BooleanField(default=False)
    fabric_use_upholstery_category = models.BooleanField(default=False)
    window_blinds_category = models.BooleanField(default=False)
    wall_panel_category = models.BooleanField(default=False)
    wallpaper_category = models.BooleanField(default=False)
    curtain_sofa_brands = models.BooleanField(default=False)
    mattresses_brands = models.BooleanField(default=False)
    window_blinds_brands = models.BooleanField(default=False)
    carpet_tile_for_office_brands = models.BooleanField(default=False)
    carpet_rolls_brands = models.BooleanField(default=False)
    rugs_brands = models.BooleanField(default=False)
    pillow_brands = models.BooleanField(default=False)
    hospital_walls_brands = models.BooleanField(default=False)
    wooden_laminate_flooring_brands = models.BooleanField(default=False)
    pvc_rubber_flooring_brands = models.BooleanField(default=False)
    curtains_rods_channel_brands = models.BooleanField(default=False)
    foam_material_brands = models.BooleanField(default=False)
    awning_canopy_brands = models.BooleanField(default=False)
    image = models.ImageField(upload_to=user_directory_path, default="subcategory.jpg")
    main_page_img = models.ImageField(upload_to=user_directory_path, default="mainpageimg.jpg")
    logo_img = models.ImageField(upload_to=user_directory_path, default="logo.jpg")

    class Meta:
        verbose_name_plural = "Company Name"

    def sub_category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def main_page_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.main_page_img.url))
    
    def logo_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.logo_img.url))
    
    def __str__(self):
        return self.company_name_title
    

class Product(models.Model):
    pid = ShortUUIDField(unique=True, max_length=30, prefix="sub_cat", alphabet="abcdefgh12345")
    main_category = models.ForeignKey(Main_category, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(Sub_categories, on_delete=models.SET_NULL, null=True)
    company_name = models.ForeignKey(Company_name, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100, default="Mobile & Laptop")
    product_slug = models.SlugField(unique=True, max_length=150, blank=True, null=True)
    description = models.TextField(null=True, blank=True, default="This is the product")
    bottom_page_description = HTMLField()
    canonical_link = models.CharField(max_length=200, default="N/A")
    meta_description = models.CharField(max_length=200, default="N/A")
    meta_title = models.CharField(max_length=200, default="N/A")
    meta_tag = models.CharField(max_length=200, default="N/A")
    meta_robots = models.CharField(max_length=100, default="N/A")
    og_url = models.CharField(max_length=100, default="N/A")
    og_title = models.CharField(max_length=100, default="N/A")
    og_description = models.CharField(max_length=100, default="N/A")
    og_image = models.CharField(max_length=100, default="N/A")
    twitter_title = models.CharField(max_length=100, default="N/A")
    twitter_description = models.CharField(max_length=100, default="N/A")
    twitter_description = models.CharField(max_length=100, default="N/A")
    price = models.DecimalField(max_digits=99999999999999, decimal_places=2, default="1.99")
    old_price = models.DecimalField(max_digits=99999999999, decimal_places=2, default="2.99")
    specifications = models.TextField(null=True, blank=True)
    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
    color = models.CharField(choices=COLOR, max_length=10, default="black")
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    best_deal = models.BooleanField(default=False)
    best_seller = models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True, max_length=50, prefix="sku", alphabet="12345678900")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True)
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")

    class Meta:
        verbose_name_plural = "Product"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.product_slug:
            self.product_slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:product', kwargs={'product_slug': self.product_slug})
    
    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price
    
class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Product Images"


class ProductVarient(models.Model):
    pid = ShortUUIDField(unique=True, max_length=30, prefix="sub_cat", alphabet="abcdefgh12345") 
    image = models.ImageField(upload_to=user_directory_path, default="productvarient.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100, default="Product Varient")
    description = models.TextField(null=True, blank=True, default="This is the product")
    price = models.DecimalField(max_digits=99999999999999, decimal_places=2, default="1.99")
    old_price = models.DecimalField(max_digits=99999999999, decimal_places=2, default="2.99")
    specifications = models.TextField(null=True, blank=True)
    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
    color = models.CharField(choices=COLOR, max_length=10, default="black")
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    sku = ShortUUIDField(unique=True, max_length=50, prefix="sku", alphabet="12345678900")
    updated = models.DateTimeField(null=True)
    date = models.DateField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Product Varient"

    def variant_images(self):
        return ProductVariantImages.objects.filter(product_variant=self)
    
    def __str__(self):
        return self.title

    def product_varient_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    

class ProductVariantImages(models.Model):
    product_variant = models.ForeignKey(ProductVarient, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path, default="productvarient.jpg")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Variant Images"

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9999999999, decimal_places=2, default="1.99")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")

    class Meta:
        verbose_name_plural = "Cart Order"



class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=999999999999, decimal_places=2, default="1.99")
    total = models.DecimalField(max_digits=999999999999, decimal_places=2, default="1.99")

    class Meta:
        verbose_name_plural = "Cart Order Items"


    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image.url))   



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
        verbose_name_plural = "Wishlists"

    def __str__(self):
        return self.product.title


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"


class Architecture(models.Model):
    aid = ShortUUIDField(unique=True, max_length=30, prefix="arch", alphabet="abcdefgh12345")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, default="CJS BHATIA...")
    contact = models.CharField(max_length=100, default="+91-")
    email = models.CharField(max_length=100, default="@gmail.com")
    address = models.CharField(max_length=100, default="South Delhi...")
    description = models.TextField(null=True, blank=True, default="about yourself...")
    instagram = models.CharField(max_length=100, default="@instagram.com")
    facebook = models.CharField(max_length=100, default="@facebook.com")
    linkedin = models.CharField(max_length=100, default="@linkedin.com")
    twitter = models.CharField(max_length=100, default="@twitter.com")
    meta_description = models.CharField(max_length=100)
    meta_title = models.CharField(max_length=100)
    meta_tag = models.CharField(max_length=100)
    featured = models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True, max_length=50, prefix="sku", alphabet="12345678900")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True)
    image = models.ImageField(upload_to=user_directory_path, default="architecture.jpg")

    class Meta:
        verbose_name_plural = "Architecture"

    def arch_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.name
    
class ArchitectureImages(models.Model):
    images = models.ImageField(upload_to="architecture-images", default="architecture.jpg")
    architecture = models.ForeignKey(Architecture, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Architecture Project Images"

class PrivacyPolicy(models.Model):
    privacy_policy_content = HTMLField()


    class Meta:
        verbose_name_plural = "Privacy Policy"


class Blogs(models.Model):
    blog_title = models.CharField(max_length=100)
    blog_image = models.ImageField(upload_to="blogs-images", default="blogs.jpg")
    blog_slug = models.SlugField(unique=True, max_length=150, blank=True, null=True) 
    blog_description = HTMLField()
    blog_tags = models.CharField(max_length=100)   
    canonical_link = models.CharField(max_length=200)
    meta_description = models.CharField(max_length=200)
    meta_title = models.CharField(max_length=200)
    meta_tag = models.CharField(max_length=200)
    meta_robots = models.CharField(max_length=100)
    og_url = models.CharField(max_length=100)
    og_title = models.CharField(max_length=100)
    og_description = models.CharField(max_length=100)
    og_image = models.CharField(max_length=100)
    twitter_title = models.CharField(max_length=100)
    twitter_description = models.CharField(max_length=100)
    twitter_description = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Blogs"


        


    






    

    
