from django.db import models
from django.contrib.auth.models import AbstractUser
class MyUser(AbstractUser):
    qq = models.CharField('FaceBook Account', max_length=20)
    weChat = models.CharField('Ins Account', max_length=20)
    mobile = models.CharField('Phone Number', max_length=11, unique=True)
    score = models.IntegerField('Score', default=100)
    disscore = models.IntegerField('Disscore', default=100)
    scoregap = models.IntegerField('Scoregap', default=0)
    sumcomment = models.IntegerField('Sumcomment', default=1)
    img = models.CharField('User Image', max_length=20)
    def total(self):
        return self.score - self.disscore
