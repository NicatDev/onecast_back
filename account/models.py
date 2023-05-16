from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
{"first_name":"Nicat","last_name":"Mammadov","email":"nicat254memmedov@gmail.com","eyecolor":"green","weight":35,
 "gender":"male","haircolor":"Red","growth":"137","education":"Bakalavr","age":23,"username":"nici","password":"123123","phone_number":"123123123"}
# Create your models here.


CATEGORY_CHOICES = [
    ('Top models', 'Top models'),
    ('Face models', 'Face models'),
    ('A Class models', 'A class models'),
    ('Promo models', 'Promo models'),
    ('Photo models', 'Photo models'),
    ('Catwalk models', 'Catwalk models'),
    ('Subtive models', 'Subtive models'),
    ('Fitness models', 'Fitness models'),
    ('Hijab models', 'Hijab models'),
    
]

ACTOR_CHOICES = [
    ('Bas rol', 'Bas rol'),
    ('Esas rollar', 'Esas rollar'),
    ('Elave rollar', 'Elave rollar'),
    ('Kutlevi rollar', 'Kutlevi rollar'),
    ('Klip cekilisi', 'Klip cekilisi'),
    ('Reklam cekilisi', 'Reklam cekilisi'),
    ('Hamisi', 'Hamisi'),
]

PRODUCTION_CHOICES = [
    ('Film studiyasi', 'Film studiyasi'),
    ('Reklam agentliyi', 'Reklam agentliyi'),
    ('Production', 'Production'),
    ('Kutlevi rollar', 'Kutlevi rollar'),
]

LANGUAGE_CHOICES = [
    ('Az', 'Az'),
    ('Rus', 'Rus'),
    ('Eng', 'Eng'),
    ('Tr', 'Tr'),
]
HAIR_COLOR = [
    ('Sari', 'Sari'),
    ('Qirmizi', 'Qirmizi'),
    ('Qara', 'Qara'),
    ('Kuren', 'Kuren'),
]

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Child', 'Child'),
]

class BaseMixin(models.Model):
    slug = models.SlugField(unique=True,editable=False,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Languages(models.Model):
    name = models.CharField(max_length=30,choices=LANGUAGE_CHOICES)
    
    def __str__(self):
        return self.name
    
class ModelCategory(models.Model):
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

class ActorCategory(models.Model):
    name = models.CharField(max_length=50, choices=ACTOR_CHOICES)

    def __str__(self):
        return self.name
    
class ProductionCategory(models.Model):
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

class Profile(BaseMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    eyecolor = models.CharField(max_length=14)
    weight = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    haircolor = models.CharField(max_length=14,choices=HAIR_COLOR)
    height = models.SmallIntegerField()
    education = models.TextField()
    age = models.PositiveIntegerField()
    cv = models.FileField(null=True,blank=True)
    image1 = models.ImageField(upload_to='media/images',null=True,blank=True)
    image2 = models.ImageField(upload_to='media/images',null=True,blank=True)
    image3 = models.ImageField(upload_to='media/images',null=True,blank=True)
    modelCategory = models.ManyToManyField('ModelCategory', related_name='modeltalents',blank=True)
    actorCategory = models.ManyToManyField('ActorCategory',related_name='actortalents',blank=True)
    is_active = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True)
    is_model = models.BooleanField(default=False)
    is_actor = models.BooleanField(default=False)
    is_child = models.BooleanField(default=False)
    is_premium = models.BooleanField(null=True,blank=True)

    class Meta:
        ordering = ['-is_premium', '-created_at']
        
    def __str__(self):
        return f'{self.first_name}-{self.last_name}-{self.age}'
    


    
class About_me(models.Model):
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE,related_name='about_me')
    content = models.TextField(null=True,blank=True)
    language = models.ManyToManyField('Languages',related_name='languages')
    instagram = models.CharField(max_length=100,null=True,blank=True)
    facebook = models.CharField(max_length=100,null=True,blank=True)
    linkedn = models.CharField(max_length=100,null=True,blank=True)
    
    class Meta:
        verbose_name = 'about me'
        verbose_name_plural = 'about_me'
        
    def __str__(self):
        return f'{self.profile.first_name}-{self.profile.last_name}'
        
               
class Company(BaseMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    company_name = models.CharField(max_length=20)
    company_website = models.CharField(max_length=30,null=True,blank=True)
    phone_number = models.CharField(max_length=20)
    about_company = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='media/company',null=True,blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.first_name}-{self.last_name}-{self.company_name}'
    
    
class Popular(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cover_photo = models.ImageField(upload_to='media/covers')
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.profile.first_name + '' + self.profile.last_name