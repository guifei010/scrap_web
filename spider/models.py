from django.db import models

# Create your models here.
# models文件是定义ORM的


class KeyWord(models.Model):
    keyword = models.CharField(unique=True, max_length=32)

    def __str__(self):
        return self.keyword


class SearchTask(models.Model):
    keyword = models.ForeignKey(KeyWord, verbose_name="关键词", on_delete=models.CASCADE)
    SITE_CHOICE = (
        ('taobao', "淘宝"),
    )
    site = models.CharField("网站", choices=SITE_CHOICE, max_length=32)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    max_limit = models.IntegerField("最大抓取个数", default=50)
    describe = models.TextField("描述", default='', blank=True)

    def __str__(self):
        return '%s-%s-%s' % (self.keyword, self.site, self.create_time)


class ItemData(models.Model):
    search_task = models.ForeignKey(SearchTask, verbose_name="搜索任务", on_delete=models.CASCADE)
    index = models.IntegerField("序号")
    title = models.CharField('名称', max_length=128)
    image = models.FileField('图片', upload_to='item_images/')
    price = models.FloatField('价格')
    location = models.CharField('发货地', max_length=32)
    seller = models.CharField('商家', max_length=32)
    view_sales = models.FloatField('购买人数')

    def __str__(self):
        return '%d-名字为：%s-售价：%s元-评论数：%s' % (self.index, self.title, self.price, self.view_sales)
        # return '%d-名字为：%s-售价：%s元 ' % (self.index, self.title, self.price)





