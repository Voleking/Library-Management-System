from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

class MemberLevel(models.Model):
    """会员级别
    member-level(level,days,numbers,fee)
    会员级别（会员级别，最长出借天数，最多借书册书，会费）
    """
    level = models.CharField(max_length=5)
    days = models.IntegerField()
    numbers = models.IntegerField()
    fee = models.FloatField()

    def __str__(self):
        return self.level

class Profile(models.Model):
    """读者信息
    readers(read_id,user.username,sex,birthday,phone,mobile,card_name,card_ID,level,user.date_joined)
    读者（读者编号，姓名，性别，出生日期，电话，手机，证件名称，证件编号，会员级别，办证日期）
    """
    reader_id = models.CharField(max_length=5)
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    sex = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')))
    birthday = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    mobile = models.CharField(max_length=15)
    card_name = models.CharField(max_length=8)
    card_id = models.CharField(max_length=20)
    level = models.ForeignKey(MemberLevel, on_delete=models.CASCADE,)
    egistrationDate = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.reader_id + " " + self.user.username

class BookCategory(models.Model):
    """图书类别
    book-category(category_id,category)
    图书类别（类别编号，类别名称）
    """
    category_id = models.CharField(max_length=5)
    category = models.CharField(max_length=128)

    def __str__(self):
        return self.category

class Book(models.Model):
    """图书信息
    book(book_id,name,author,publishing,category,price,date_in,quantity_in,quantity_out, quantity_loss)
    图书（图书编号，书名，作者，出版社，类别，单价，入库日期，入库数量，出借数量，遗失数量）
    """
    book_id = models.CharField(max_length=5)
    name = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    publishing = models.CharField(max_length=128)
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE,)
    price = models.FloatField()
    date_in = models.DateField()
    quantity_in = models.IntegerField()
    quantity_out = models.IntegerField()
    quantity_loss = models.IntegerField()

    def __str__(self):
        return self.book_id + " 《" + self.name + "》—— " + self.author;

class Borrow(models.Model):
    """借阅信息
    borrow(reader,book,date_borrow,date_return,loss)
    借阅（读者，图书，出借日期，应还日期，遗失）
    """
    reader = models.ForeignKey('Profile', on_delete=models.CASCADE,)
    book = models.ForeignKey('Book', on_delete=models.CASCADE,)
    date_borrow = models.DateField(auto_now_add=True)
    date_return = models.DateField(editable=False)
    is_lost = models.BooleanField(default=False, editable=False)
    is_returned = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return str(self.reader) + " " + str(self.book)

    def save(self):
        if not self.id:
            from datetime import date, timedelta
            self.date_return = date.today() + timedelta(days=self.reader.level.days)
            self.book.quantity_out += 1
            self.book.save()
            super(Borrow, self).save()

    @property
    def is_overdue(self):
        return date.today() > self.date_return

class LossReporting(models.Model):
    """挂失
    loss-reporting(reader-id,loss-date)
    挂失（读者编号，挂失日期）
    """
    reader = models.ForeignKey('Profile', on_delete=models.CASCADE, )
    loss_date = models.DateField(auto_now_add=True)

    def save(self):
        if not self.id:
            self.reader.user.is_active = False
            self.reader.user.save()
            super(LossReporting, self).save()

    def delete(self):
        self.reader.user.is_active = True
        self.reader.user.save()
        super(LossReporting, self).delete()

    def __str__(self):
        return str(self.reader)
