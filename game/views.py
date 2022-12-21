import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Game
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User
from django.db.models import Q

# REGISTER
class register(View):
    def get(self, request):
        
        return render(request, "registration/signup.html")
    def post(self, request):
        first_name=request.POST["fname"]
        last_name=request.POST["lname"]
        username=request.POST["username"]
        email=request.POST["email"]
        password=request.POST["password"]
        passwordconf=request.POST["passwordconf"]
        if password != passwordconf:
            messages.add_message(request, messages.ERROR, "Passwords do not match")
            return HttpResponseRedirect(reverse("register"))
        try:
            User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        except:
            messages.add_message(request, messages.ERROR, "This username already exists!")
            return HttpResponseRedirect(reverse("register"))
        messages.add_message(request, messages.SUCCESS, "User successfully registered! Login now...")
        return HttpResponseRedirect("/accounts/login/")




#INDEX PAGE
@login_required
def index(request):
    x=request.user
    return render(request, "game/lobby.html",)

# INVITES
@login_required
def ongoing(request):
    games = []
    l = Game.objects.all().filter(owner=request.user).filter(status=1)
    g = Game.objects.all().filter(Q(owner=request.user) | Q(opponent=request.user)).filter(status=2)
    for i in g:
        x = {}
        x["game_id"] = i.id

        if i.owner == request.user:
            x["opponent"] = i.opponent
            x["side"] = i.owner_side
        else:
            x["opponent"] = i.owner
            if i.owner_side == "white":
                x["side"] = "black"
            else:
                x["side"] = "white"
        x["link"] = f"/game/{i.pk}"
        games.append(x) 
    return render(request, "game/ongoing.html", { "ongoing": games})

# CREATE INVITE
class createGame(LoginRequiredMixin, View):
    def get(self, request):
        our_user = User.objects.exclude(id=request.user.id)
        players = []
        for i in our_user:
            players.append(i.username)
        return render(request,"game/create.html",{'players':players})

    def post(self, request):
 
        username = request.POST["username"]
        side = random.choice(['black','white'])
        level = "Begineer"
        if username and not (username == "nouser"):
            try:
                our_user = User.objects.get(username=username)
                if our_user ==  request.user:
                    messages.add_message(request, messages.ERROR, "You can't play a game with yourself!")
                    return HttpResponseRedirect(reverse("create"))
                g = Game.objects.create(owner=request.user, opponent=our_user, owner_side=side, status=2)

                return HttpResponseRedirect('/game/'+str(g.pk))

            except Exception as e:
                messages.add_message(request, messages.ERROR, "Somthing went wrong")
                return HttpResponseRedirect(reverse("create"))
        else:
            messages.add_message(request, messages.ERROR, "No user found")
            return HttpResponseRedirect(reverse("create"))

# PUBLICALLY HOSTING
@login_required
def game(request, game_id):
    game = get_object_or_404(Game,pk=game_id)
    if game.status == 3:
        messages.add_message(request, messages.ERROR, "This game has already been completed! Start another")
        return HttpResponseRedirect(reverse("lobby"))
    if request.user != game.owner:
        if game.opponent == None:
            game.opponent = request.user
            game.status = 2
            game.save()
            messages.add_message(request, messages.SUCCESS, "You have joined this game successfully")
            return HttpResponseRedirect(reverse("lobby"))
    return render(request, "game/game.html", {"game_id":game_id})


    
#COMPLETED
@login_required
def completed(request):
    games=[]
    g = Game.objects.all().filter(Q(owner=request.user) | Q(opponent=request.user)).filter(status=3)
    for i in g:
        x = {}
        x["result"] = ""
        x["game_id"] = i.id

        if i.owner == request.user:
            x["opponent"] = i.opponent
            x["side"] = i.owner_side

            if i.winner == "White wins":
                if i.owner_side == "white":
                    x["result"] = "You won this match"
                else:
                    x["result"] = "You lost this match"
            elif i.winner == "Black wins":

                if i.owner_side == "black":
                    x["result"] = "You won this match"
                else:
                    x["result"] = "You lost this match"
            else:
                x["result"] = i.winner
        else:

            x["opponent"] = i.owner 
            if i.owner_side == "white":
                x["side"] = "black"
            else:
                x["side"] = "white"
                
            if i.winner == "Black wins":
                if i.owner_side == "white":
                    x["result"] = "You won this match"
                else:
                    x["result"] = "You lost this match"
            elif i.winner == "White wins":
                if i.owner_side == "black":
                    x["result"] = "You won this match"
                else:
                    x["result"] = "You lost this match"
            else:
                x["result"] = i.winner
        games.append(x)
    return render(request, "game/completed.html", {"completed": games})
