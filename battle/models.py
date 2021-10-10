from django.db import models

# Create your models here.

# stats model that keeps track of win loss record of bots
class Player(models.Model):
    name = models.CharField(max_length=100)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    def __str__(self):
        return self.name + ": (" + str(self.wins) + "-" + str(self.losses) + ")"

class HighScore(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.name + ": " + str(self.score)