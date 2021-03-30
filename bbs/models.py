from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail

class BBSType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

class BBS(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=50)
    bbs_type = models.ForeignKey(BBSType, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)    

    def get_url(self):
        return reverse('bbs_detail', kwargs={'bbs_pk': self.pk})

    def get_email(self):
        return self.author.email

    def __str__(self):
        return "<BBS: %s>" % self.title

    class Meta:
        ordering = ['-created_time']
