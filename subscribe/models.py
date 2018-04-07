from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=250, primary_key=True)

    def __str__(self):
        return self.name

    def __lt__(self, other):
        return self.name < other.name


class User(models.Model):
    email = models.CharField(max_length=250, primary_key=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.email + " : " + str(self.location)
