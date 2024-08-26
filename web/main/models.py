from django.db import models

class Certificate(models.Model):
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    date_issued = models.DateField()
    image = models.ImageField(upload_to='certificates/', null=True, blank=True)
    def __str__(self):
        return self.name

class Portfolio(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField()
    image = models.ImageField(upload_to='portfolio/', null=True, blank=True)

    def __str__(self):
        return self.title
    
class Microblog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='microblog/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class HomeSetting(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='home/', null=True, blank=True)

    def __str__(self):
        return self.title