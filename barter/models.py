from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail
from PIL import Image

class BarterType(models.Model):
    """换品类型模型类"""
    type_name = models.CharField(max_length=20, verbose_name='种类名称')
    image = models.ImageField(upload_to='bartertype', verbose_name='商品类型图片',blank=True, null=True)

    class Meta:
        verbose_name = '换品种类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.type_name

class Barter(models.Model, ReadNumExpandMethod):
    status_choices = (
        (0, '下线'),
        (1, '上线')
    )
    where_choices = (
        (0, '奉贤'),
        (1, '徐汇')
    )
    name = models.CharField(max_length=50,verbose_name='换品名称')
    barter_type = models.ForeignKey(BarterType,verbose_name='换品类型',on_delete=models.CASCADE)
    content = RichTextUploadingField(verbose_name='换品描述')
    image = models.ImageField(upload_to='barter/%Y%m%d/', verbose_name='换品图片',blank=True, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='卖家')
    want_barter = models.CharField(max_length=500, blank=True, null=True,verbose_name='想换物品')
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    where = models.SmallIntegerField(default=0, choices=where_choices, verbose_name='所在校区')
    status = models.SmallIntegerField(default=1, choices=status_choices, verbose_name='状态')
    isDelete = models.BooleanField(verbose_name='是否删除', default=False)

    # 保存时处理图片
    def save(self, *args, **kwargs):
        # 调用原有的 save() 的功能
        barter = super(Barter, self).save(*args, **kwargs)

        # 固定宽度缩放图片大小
        if self.image and not kwargs.get('update_fields'):
            image = Image.open(self.image)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.image.path)
        return barter

    def get_email(self):
        return self.seller.email

    def get_url(self):
        return reverse('barter_detail', kwargs={'barter_pk': self.pk})

    def get_user(self):
        return self.seller

    def __str__(self):
        return "<Barter: %s>" % self.name

    class Meta:
        verbose_name = '换品'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

class Application(models.Model):
    status_choices = (
        (0, '待查阅'),
        (1, '失败'),
        (2, '成功')
    )
    order_id = models.CharField(max_length=50, default='')
    seller = models.ForeignKey(User, verbose_name='卖家',related_name='seller', on_delete=models.CASCADE)
    sell_barter = models.ForeignKey(Barter, related_name='sell_barter', on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, verbose_name='买家',related_name='buyer', on_delete=models.CASCADE)
    buy_barter = models.ForeignKey(Barter, related_name='buy_barter', on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=0, choices=status_choices, verbose_name='状态')
    isDelete = models.BooleanField(verbose_name='是否删除', default=False)

    def __str__(self):
        return self.buyer.username

    class Meta:
        verbose_name = '交易记录表'
        verbose_name_plural = verbose_name
