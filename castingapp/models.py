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
    def __str__(self):
        return self.user.username
    
class SentCard(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='cards')
    accepted = models.BooleanField(default=False)
    desitiondate = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username}-{self.accepted}-{self.desitiondate}'
    
class CardItem(models.Model):
    card = models.ForeignKey(SentCard,on_delete=models.CASCADE,related_name='items')
    talent = models.ForeignKey(Profile,on_delete=models.CASCADE)
    
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
        verbose_name = 'News'
        verbose_name_plural = 'News'
    
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
    
class Contact_us(models.Model):
    full_name = models.CharField(max_length=50)
    title = models.CharField(max_length=120)
    message = models.TextField(null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    
    def __str__(self):
        return self.full_name + ' ' + self.title