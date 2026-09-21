
from django.db import models

class User(models.Model):
    Name=models.CharField(max_length=100)
    Email=models.EmailField(unique=True)
    Phone=models.IntegerField(null=True,blank=True)
    Image=models.FileField(null=True,blank=True)
    DOB=models.DateField(null=True,blank=True)
    Pass = models.CharField(max_length=100)
# Create your models here.




from django.db import models

class Watch(models.Model):

    BRAND_CHOICES = [
        ('Rolex', 'Rolex'),
        ('Titan', 'Titan'),
        ('Fastrack', 'Fastrack'),
        ('Casio', 'Casio'),
        ('Fossil', 'Fossil'),
        ('Timex', 'Timex'),
        ('Seiko', 'Seiko'),
        ('Citizen', 'Citizen'),
        ('Omega', 'Omega'),
        ('Tag Heuer', 'Tag Heuer'),
        ('Hublot', 'Hublot'),
        ('Patek Philippe', 'Patek Philippe'),
        ('Audemars Piguet', 'Audemars Piguet'),
        ('Breitling', 'Breitling'),
        ('IWC Schaffhausen', 'IWC Schaffhausen'),
        ('Jaeger-LeCoultre', 'Jaeger-LeCoultre'),
        ('Panerai', 'Panerai'),
        ('Richard Mille', 'Richard Mille'),
        ('Vacheron Constantin', 'Vacheron Constantin'),
    ]

    WATCH_TYPE_CHOICES = [
        ('Analog', 'Analog'),
        ('Digital', 'Digital'),
        ('Smartwatch', 'Smartwatch'),
        ('Hybrid', 'Hybrid'),

    ]

    STRAP_CHOICES = [
        ('Leather', 'Leather'),
        ('Metal', 'Metal'),
        ('Silicone', 'Silicone'),
        ('Nylon', 'Nylon'),
    ]

    brand = models.CharField(max_length=100, choices=BRAND_CHOICES)

    model_name = models.CharField(max_length=150)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    color = models.CharField(max_length=100)

    watch_type = models.CharField(
        max_length=20,
        choices=WATCH_TYPE_CHOICES
    )

    strap_material = models.CharField(
        max_length=20,
        choices=STRAP_CHOICES
    )

    dial_color = models.CharField(max_length=100)

    case_material = models.CharField(max_length=100)

    display_size = models.CharField(
        max_length=50,
        help_text="Dial size in mm"
    )

    water_resistant = models.BooleanField(default=False)

    warranty = models.CharField(max_length=50)

    battery_life = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="For smartwatches"
    )

    bluetooth = models.BooleanField(default=False)

    stock = models.PositiveIntegerField(default=0)

    image = models.ImageField(upload_to='watches/')

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} {self.model_name}"
    




class Cart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    watch = models.ForeignKey(
        Watch,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(default=1)

    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.Name} - {self.watch.model_name}"

class Wishlist(models.Model):

    watch = models.ForeignKey(
        Watch,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.watch.model_name

