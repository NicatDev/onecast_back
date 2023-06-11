from django.db import models

from django.contrib.auth import get_user_model
from .utils import create_slug_shortcode
from account.models import Profile,Company,BaseMixin
User = get_user_model()



class BaseMixin(models.Model):
    slug = models.SlugField(unique=True,editable=False,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

#cardfav
class Favourites(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='favs')
    talent = models.ForeignKey(Profile,on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Favori'
        verbose_name_plural = 'Favoriler'
    
    def __str__(self):
        return self.user.username
    
class SentCard(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='cards')
    accepted = models.BooleanField(default=False)
    desitiondate = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Basket qutusu'
        verbose_name_plural = 'Basket qutulari'
    
    def __str__(self):
        return f'{self.user.username}-{self.accepted}-{self.desitiondate}'
    
class CardItem(models.Model):
    card = models.ForeignKey(SentCard,on_delete=models.CASCADE,related_name='items')
    talent = models.ForeignKey(Profile,on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Basketdeki talant'
        verbose_name_plural = 'Basketdeki talantlar'
    
    def __str__(self):
        return self.card.user.username
#magazine

class News(BaseMixin):
    title = models.CharField(max_length=120)
    content = models.TextField()
    image = models.ImageField(upload_to='media/news',null=True,blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'magazin xeber'
        verbose_name_plural = 'magazin xeberler'
    
    def save(self, *args, **kvargs):
        if not self.slug:
            self.slug = create_slug_shortcode(self,size=12, model_ = News)

        super(News, self).save(*args, **kvargs)
    
#Category
class Partners(models.Model):
    title = models.CharField(max_length=30)
    image = models.ImageField(upload_to='media/partners')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Partner'
        verbose_name_plural = 'Partnerler'
    
class Contact_us(models.Model):
    full_name = models.CharField(max_length=50)
    title = models.CharField(max_length=120)
    message = models.TextField(null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    
    class Meta:
        verbose_name = 'Mektub'
        verbose_name_plural = 'Mektublar'
    
    def __str__(self):
        return self.full_name + ' ' + self.title
    
class OneNews(BaseMixin):
    title = models.CharField(max_length=120)
    content = models.TextField()
    link = models.CharField(max_length=90,null=True,blank=True)
    image = models.ImageField()
    
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Bizim xeber'
        verbose_name_plural = 'Bizim xeberler'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kvargs):
        if not self.slug:
            self.slug = create_slug_shortcode(self,size=12, model_ = OneNews)

        super(OneNews, self).save(*args, **kvargs)
    
class OneNewsCover(models.Model):
    title = models.CharField(max_length=40)
    content = models.TextField(null=True,blank=True)
    image = models.ImageField()
    
    class Meta:

        verbose_name = 'Bizim Xeber Reklam'
        verbose_name_plural = 'Bizim xeber Reklamlar'
    
    def __str__(self):
        return self.title
    
class Notification(BaseMixin):

    title = models.CharField(max_length=70)
    content = models.TextField()
    talant = models.OneToOneField(Profile,on_delete=models.CASCADE,null=True,blank=True)
    company = models.OneToOneField(Company,on_delete=models.CASCADE,null=True,blank=True)
    for_model = models.BooleanField(default=False)
    for_actor = models.BooleanField(default=False)
    for_company = models.BooleanField(default=False)
    for_child = models.BooleanField(default=False)
    for_none_users = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Bildiris'
        verbose_name_plural = 'Bildirisler'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kvargs):
        if not self.slug:
            self.slug = create_slug_shortcode(self,size=12, model_ = Notification)

        super(Notification, self).save(*args, **kvargs)
    

    
class ConfirmHistory(BaseMixin):
    company = models.OneToOneField(Company,on_delete=models.SET_NULL,null=True,blank=True)
    talents = models.TextField(null=True,blank=True)
    accepted = models.BooleanField(default = False)
    rejected = models.BooleanField(default = False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Company muracieti'
        verbose_name_plural = 'Company muracietleri'
    
    def __str__(self):
        return self.company.company_name
    