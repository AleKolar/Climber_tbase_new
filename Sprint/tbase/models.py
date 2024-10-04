from django.db import models


class User(models.Model):
    email = models.EmailField(primary_key=True)
    fam = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    otc = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)


class Coords(models.Model):
    id = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()


class PerevalAdded(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    beautyTitle = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    connect = models.TextField()
    add_time = models.DateTimeField()
    winter_level = models.CharField(max_length=10)
    summer_level = models.CharField(max_length=10)
    autumn_level = models.CharField(max_length=10)
    spring_level = models.CharField(max_length=10)
    coord = models.ForeignKey(Coords, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('new', 'new'), ('pending', 'pending'), ('accepted', 'accepted'),
                                                      ('rejected', 'rejected')], default='new')


class PerevalImages(models.Model):
    id = models.AutoField(primary_key=True)
    image_name = models.CharField(max_length=255)


class PerevalImagesRelation(models.Model):
    pereval = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE)
    image = models.ForeignKey(PerevalImages, on_delete=models.CASCADE)
