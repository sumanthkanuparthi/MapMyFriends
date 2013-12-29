from django.shortcuts import render
from django_facebook.api import get_facebook_graph, FacebookUserConverter, get_persistent_graph
from django_facebook.decorators import facebook_required

@facebook_required
def home(request):
  graph = get_persistent_graph(request)
  #me = graph.fql("SELECT uid, name,current_address,current_location,relationship_status FROM user WHERE uid = me()")
  me = graph.fql("SELECT uid, name,current_address,current_location,relationship_status FROM user WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = me())")
  #me = graph.fql('SELECT name FROM user WHERE uid = me()')

  return render(request, 'hellodjango/templates/home.html', {'me':me})

def pp(request):
  return render(request, 'hellodjango/templates/pp.html')

def tos(request):
  return render(request, 'hellodjango/templates/tos.html')

def usupp(request):
  return render(request, 'hellodjango/templates/tos.html')
