from django.db import models


class User(models.Model):
    email = models.EmailField(primary_key=True, unique=True)
    fam = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    otc = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)


class Coord(models.Model):
    latitude = models.FloatField(unique=True)
    longitude = models.FloatField(unique=True)
    height = models.IntegerField(unique=True)


class Level(models.Model):
    winter = models.CharField(max_length=10)
    summer = models.CharField(max_length=10)
    autumn = models.CharField(max_length=10)
    spring = models.CharField(max_length=10)



class PerevalAdded(models.Model):
    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    connect = models.TextField(blank=True)
    add_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coords = models.ForeignKey(Coord, on_delete=models.CASCADE)
    level = models.OneToOneField(Level, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('new', 'new'), ('pending', 'pending'), ('accepted', 'accepted'),
                                                      ('rejected', 'rejected')], default='new')


class Images(models.Model):
    data = models.TextField()
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
