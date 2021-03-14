from django.db import models


class Contact(models.Model):
    phone_number = models.CharField(max_length=10, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return self.first_name + '_' + self.phone_number
