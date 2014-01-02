from django.shortcuts import render
from django_facebook.api import get_facebook_graph, FacebookUserConverter, get_persistent_graph
from django_facebook.decorators import facebook_required
from django.http import HttpResponse
from math import radians, cos, sin, asin, sqrt
from haversine import haversine
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
   city_temp = city;
   city.replace("%20"," ");
   city_list = list();
   for val in city_map:
     if(city == val[2]):
       dup_check = False
       for users in city_list:
         if( val[0] == users[0] ):
           dup_check=True
       if(dup_check == False ):
         city_list.insert(0,val)
   ret_val = json.dumps([dict(mpn=pn) for pn in city_list])
   # return city_list
   return HttpResponse(json.dumps(city_list), content_type="application/json")
   #return ret_val
   #return render(request,'hellodjango/templates/home.html',{'me':city_temp,'me1':city})
   #return render(request,'hellodjango/templates/collage.html',{'pic':city_list,'city':city})

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
       uid = li.get('uid')
       pic_square = li.get('pic_square').encode('ascii','ignore')
       lat = s.get('latitude')
       lang = s.get('longitude')
       user_tuple = list();
       
       cond = False
       for val in g:
         lat2 = val[1]
         lang2 = val[2]
         ll1 = (lat,lang)
         ll2 = (lat2,lang2)
         if(haversine(ll1,ll2) <= 50):
           cond == True
           city = val[0]
           break
       
       city_clean = city.lower()
       user_tuple.insert(1, uid)       
       user_tuple.insert(2, pic_square)
       user_tuple.insert(3, city_clean)
       
       city_map.insert(0,user_tuple)
       if(cond == False):
         t.append(city)
         t.append(lat)
         t.append(lang)
         s1 = li.get('pic_square')
         if s1 is not None:
           t.append(s1.encode('ascii','ignore'))
         g.append(t)
  g = json.dumps(g)
  #return render(request,'hellodjango/templates/home.html',{'me':city_map})
  return render(request, 'hellodjango/templates/rev_geocode.html', {'me':me,'locations':g})
  #return render(request, 'hellodjango/templates/home.html', {'me':city_map,'locations':li})
