from django.shortcuts import render
from django_facebook.api import get_facebook_graph, FacebookUserConverter, get_persistent_graph
from django_facebook.decorators import facebook_required
import json

@facebook_required
def home(request):
  graph = get_persistent_graph(request)
  #me  = graph.permissions()

  #me = graph.fql("SELECT friends_about_me,friends_location,friends_hometown FROM permissions WHERE uid = me()")
  me = graph.fql("SELECT uid, name,current_address,current_location,relationship_status FROM user WHERE uid = me()")
  me1 = graph.fql("SELECT current_location,pic_square FROM user WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = me())")
  #me = graph.fql('SELECT name FROM user WHERE uid = me()')
  #me1 = graph.fql("SELECT uid, name, pic_square FROM user WHERE uid = me() OR uid IN (SELECT uid2 FROM friend WHERE uid1 = me())")
  
  g = list()
  for li in me1:
    s = li.get('current_location')
    if s is not None:
       t = list()
       t.append(s.get('city').encode('ascii','ignore'))
       t.append(s.get('latitude'))
       t.append(s.get('longitude'))
       s1 = li.get('pic_square')
       if s1 is not None:
         t.append(s1.encode('ascii','ignore'))
       g.append(t) 
  g = json.dumps(g)
  return render(request, 'hellodjango/templates/map.html', {'me':me,'me1':me1,'locations':g})

def pp(request):
  return render(request, 'hellodjango/templates/pp.html')

def tos(request):
  return render(request, 'hellodjango/templates/tos.html')

def usupp(request):
  return render(request, 'hellodjango/templates/tos.html')

def map(request):
   return render(request,'hellodjango/templates/mmap.html')
