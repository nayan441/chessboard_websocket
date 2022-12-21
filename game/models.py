from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Game(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name="owner")
    opponent = models.ForeignKey(User, on_delete=models.CASCADE,related_name="opponent", null=True)
    owner_side= models.CharField(max_length=10, default="white")
    owner_online = models.BooleanField(default=False)
    opponent_online = models.BooleanField(default=False)
    fen = models.CharField(max_length=92, null=True, blank=True)
    pgn = models.TextField(null=True, blank=True)
    winner = models.CharField(max_length=20, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    CHOICES=(
        (1,"Game Created. Waiting for opponent"),
        (2,"Game Started"),
        (3,"Game Ended"))
    status = models.IntegerField(default=1,choices=CHOICES)

    
    def __str__(self):
        return f"Game {self.id} -> {self.owner} vs {self.opponent}"


from django.contrib.auth.models import User
from faker import Faker

fakegen= Faker()

def populate(N=5):
    with open("users.json",'a', encoding = 'utf-8') as f:
        for entry in range(N):
            fakename = fakegen.name()
            username = fakename.replace(" ","")
            fake_name= fakename.split()
            fake_first_name = fake_name[0]
            fake_last_name = fake_name[1]
            fake_email= fakegen.email()
            f.write("{'username':'%s', 'password':'Qwerty@12345', 'email':'%s'},\n"% (username,fake_email))
            print(fakename, fake_email)
            try:
                user = User.objects.get_or_create(username= username, first_name = fake_last_name,
                                last_name= fake_last_name,email = fake_email, password="Qwerty@12345")[0]
            except:
                pass

# populate(10)
if __name__ == '__main__':
    print('populating databases......................')
    print('populated')