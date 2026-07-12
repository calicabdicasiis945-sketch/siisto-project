from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# 1. PROFILE MODEL (Wixii ku saabsan qofka)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dherer = models.FloatField(help_text="Height in cm", null=True, blank=True)
    miisaan_hadda = models.FloatField(help_text="Current weight in kg", null=True, blank=True)
    hadaf = models.CharField(max_length=200, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

# 2. CUNTO MODEL (Waxaan ku darnay Calories iyo Protein)
class Cunto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nooca_cuntada = models.CharField(max_length=200)
    calories = models.IntegerField(default=0)
    protein = models.IntegerField(default=0)
    taariikhda = models.DateField(default=timezone.now)

    def __str__(self):
        return self.nooca_cuntada

# 3. JIMICSI MODEL
class Jimicsi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    magaca_jimicsiga = models.CharField(max_length=200)
    taariikhda = models.DateField(default=timezone.now)

# 4. WEIGHT LOG MODEL (Si loo raadraaco miisaanka isbeddelaya)
class WeightLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    miisaanka = models.FloatField()
    taariikhda = models.DateTimeField(auto_now_add=True)

# 5. ROUTINE90 MODEL
class Routine90(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    maalinta = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)