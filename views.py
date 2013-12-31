from django.shortcuts import render
from django_facebook.api import get_facebook_graph, FacebookUserConverter, get_persistent_graph
from django_facebook.decorators import facebook_required
import json

city_map = list();

@facebook_required
def home(request):
  graph = get_persistent_graph(request)
  #me  = graph.permissions()

  #me = graph.fql("SELECT friends_about_me,friends_location,friends_hometown FROM permissions WHERE uid = me()")
  #me = graph.fql("SELECT uid, name,current_address,current_location,relationship_status FROM user WHERE uid = me()")
  me = graph.fql("SELECT current_location,pic_square FROM user WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = me())")
  #me = graph.fql('SELECT name FROM user WHERE uid = me()')
  #me1 = graph.fql("SELECT uid, name, pic_square FROM user WHERE uid = me() OR uid IN (SELECT uid2 FROM friend WHERE uid1 = me())")
  
  g = list()
  for li in me:
    s = li.get('current_location')
    if s is not None:
       t = list()
       t.append(s.get('city').encode('ascii','ignore'))
       t.append(s.get('latitude'))
       t.append(s.get('longitude'))
       #t.append(s.get('country'))
       #t.append(s.get('state'))
       s1 = li.get('pic_square')
       if s1 is not None:
         t.append(s1.encode('ascii','ignore'))
       g.append(t) 
  g = json.dumps(g)
  return render(request, 'hellodjango/templates/map.html', {'me':me,'locations':g})

def pp(request):
  return render(request, 'hellodjango/templates/pp.html')

def tos(request):
  return render(request, 'hellodjango/templates/tos.html')

def usupp(request):
  return render(request, 'hellodjango/templates/tos.html')

def map(request):
   graph = get_persistent_graph(request)
   pics = graph.fql("SELECT pic_square FROM user WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = me())")
   pic = list()
   for li in pics:
     s = li.get('pic_square')
     if s is not None:
       pic.append(s.encode('ascii','ignore'))
   pic=json.dumps(pic)  
   return render(request,'hellodjango/templates/mmap.html',{'pic':pic})


@facebook_required
def friend_list(request,city):
   graph = get_persistent_graph(request)
   city_list = list();
   for val in  city_map:
     if(city in val):
       val.pop(2)
       city_list.insert(0,val)
   #return render(request,'hellodjango/templates/home.html',{'me':city_list,'locations':city_map})
   return render(request,'hellodjango/templates/collage.html',{'pic':city_list})

@facebook_required
def rev_geocode(request):
  graph = get_persistent_graph(request)

  me = graph.fql("SELECT uid,current_location,pic_square FROM user WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = me())")
  g = list()
  for li in me:
    s = li.get('current_location')
    #uid = li.get('id');
    if s is not None:
       t = list()
       city = (s.get('city').encode('ascii','ignore'))
       city = city.strip();
       city_clean = city.lower()
       uid = li.get('uid')
       pic_square = li.get('pic_square').encode('ascii','ignore')
       user_tuple = list();
       user_tuple.insert(1, uid)       
       user_tuple.insert(2, pic_square)
       user_tuple.insert(3, city_clean)
       city_map.insert(0,user_tuple)
       t.append(city)
       t.append(s.get('latitude'))
       t.append(s.get('longitude'))
       s1 = li.get('pic_square')
       if s1 is not None:
         t.append(s1.encode('ascii','ignore'))
       g.append(t)
  g = json.dumps(g)
  return render(request, 'hellodjango/templates/rev_geocode.html', {'me':me,'locations':g})
  #return render(request, 'hellodjango/templates/home.html', {'me':city_map,'locations':li})
