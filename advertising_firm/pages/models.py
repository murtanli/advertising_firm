from django.contrib.auth.models import User as AuthUser
from django.db import models

class Level(models.Model):
    levels = [
        ('Без уровня', 'Без уровня'),
        ('Первый уровень', 'Первый уровень'),
        ('Второй уровень', 'Второй уровень'),
        ('Третий уровень', 'Третий уровень'),
        ('Четвертый уровень', 'Четвертый уровень')
    ]
    disc = [
        (0, 0),
        (5, 5),
        (10, 10),
        (15, 15),
        (20, 20),
    ]
    LevelID = models.AutoField(primary_key=True)
    LevelName = models.CharField(max_length=255, choices=levels, null=True, blank=True)
    Discount = models.IntegerField(choices=disc, null=True, blank=True)

    def __str__(self):
        return self.LevelName if self.LevelName else "Без уровня"
class Profile(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    FullName = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)
    LevelID = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return self.FullName

class Service(models.Model):
    ServiceID = models.AutoField(primary_key=True)
    ServiceName = models.CharField(max_length=255)
    Description = models.TextField()
    Price = models.IntegerField()

    def __str__(self):
        return self.ServiceName

class Order(models.Model):
    status = [
        ('В обработке', 'В обработке'),
        ('Принята', 'Принята'),
        ('В разработке', 'В разработке'),
        ('Выполнен', 'Выполнен')
    ]

    OrderID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(Profile, on_delete=models.CASCADE)
    Description = models.TextField()
    OrderDate = models.DateTimeField(auto_now_add=True)
    Status = models.CharField(max_length=50, choices=status, default='В обработке')
    TotalAmount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'Order {self.OrderID} by {self.UserID}'

class OrderDetail(models.Model):
    OrderDetailID = models.AutoField(primary_key=True)
    OrderID = models.ForeignKey(Order, on_delete=models.CASCADE)
    ServiceID = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    Price = models.IntegerField()
    Discount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'Detail {self.OrderDetailID} for Order {self.OrderID}'

class Employee(models.Model):
    roles = [
        ('Дизайнер', 'Дизайнер'),
        ('Пост печатник', 'Пост печатник')
    ]
    EmployeeID = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, null=True, blank=True)
    FullName = models.CharField(max_length=255)
    Role = models.CharField(max_length=255, choices=roles)
    orderd_work = models.ManyToManyField(OrderDetail, null=True, blank=True)

    def __str__(self):
        return self.FullName

class Review(models.Model):
    ReviewID = models.AutoField(primary_key=True)
    FullName = models.CharField(max_length=255, null=True, blank=True)
    number_phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=30, null=True, blank=True)
    UserID = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    ServiceID = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    Rating = models.IntegerField(null=True, blank=True)
    Comment = models.TextField()

    def __str__(self):
        return f'Review {self.ReviewID} by {self.UserID}'
