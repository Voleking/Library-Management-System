from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """读者信息
    readers(id,user.username,sex,birthday,phone,mobile,card_name,card_ID,level,user.date_joined)
    读者（读者编号，姓名，性别，出生日期，电话，手机，证件名称，证件编号，会员级别，办证日期）
    TODO: test instance.user.is_superuser = instance.user.is_is_staff = False;
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    sex = models.CharField(max_length=1,
                           choices=(('M', 'Male'), ('F', 'Female')))
    birthday = models.DateField()
    phone = models.CharField(max_length=15)
    mobile = models.CharField(max_length=15)
    card_name = models.CharField(max_length=20)
    card_ID = models.CharField(max_length=20)
    level = models.IntegerField() # 初级会员，中级会员，高级会员
    # egistrationDate = models.DateField() <--- user.date_joined

    def __str__(self):
        return self.user.name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.user.is_superuser = instance.user.is_is_staff = False;
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Book(models.Model):
    """图书信息
    book(id,name,author,publishing,category_id,price,date_in,quantity_in,quantity_out, quantity_loss)
    图书（图书编号，书名，作者，出版社，类别，单价，入库日期，入库数量，出借数量，遗失数量）
    """
    name = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    publishing = models.CharField(max_length=128)
    category_id = models.IntegerField()
    price = models.FloatField()
    date_in = models.DateTimeField()
    quantity_in = models.IntegerField()
    quantity_out = models.IntegerField()
    quantity_loss = models.IntegerField()

    def __str__(self):
        return "Title: " + self.name + " Author: " + self.author;

class Borrow(models.Model):
    """借阅信息
    borrow(reader,book,date_borrow,date_return,loss)
    借阅（读者，图书，出借日期，应还日期，遗失）
    """
    reader = models.ForeignKey('Profile', on_delete=models.CASCADE, )
    book = models.ForeignKey('Book', on_delete=models.CASCADE, )
    data_borrow = models.DateField()
    data_return = models.DateField()
    loss = models.BooleanField(True)

    def __str__(self):
        return self.reader + " " + self.book

class BookCategory(models.Model):
    """图书类别
    book-category(id,category)
    图书类别（类别编号，类别名称）
    """
    category = models.CharField(max_length=128)

    def __str__(self):
        return self.category

class MemberLevel(models.Model):
    """会员级别
    member-level(level,days,numbers,fee)
    会员级别（会员级别，最长出借天数，最多借书册书，会费）
    """
    level = models.IntegerField()
    days = models.IntegerField()
    numbers = models.IntegerField()
    fee = models.FloatField()

    def __str__(self):
        return self.level

class LossReporting(models.Model):
    """挂失
    loss-reporting(reader-id,loss-date)
    挂失（读者编号，挂失日期）
    """
    reader = models.ForeignKey('Profile', on_delete=models.CASCADE, )
    loss_date = models.DateTimeField()

    def __str__(self):
        return self.reader
