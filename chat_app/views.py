from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf

from chat_app.forms import *
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from django.utils import timezone




#go to login page
def login(request):
    c={}
    c.update(csrf(request))
    return render(request,'registration/login.html',c)

#logout function
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login")

#login function
def auth_view(request):
    username=request.POST.get('username','')
    password=request.POST.get('password','')
    user=auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect('/chatslist')
    else:
        return render(request,'registration/login.html',{'error':True,'msg':'Wrong username or passsword!'})

#register a user
def register(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    args={}
    args.update(csrf(request))
    args['form']=MyRegistrationForm()
    return render(request,'registration/register.html',args)


def register_success(request):
    return render(request,'registration/register_success.html')

#returns the home page
def home(request):
    return render(request, 'home.html')

#returns all the chat rooms the user can see
@login_required(login_url='/login/')
def chatslist(request):
    chatlist={}
    chatlist.update(csrf(request))
	# 1-1 chat room
    chatlist['chats0']=Chat.objects.filter(users=request.user,type=0)
	# private chat room 
    chatlist['chats1']=Chat.objects.filter(users=request.user,type=1)
	# public chat room
    chatlist['chats2']=Chat.objects.filter(type=2)
    return render(request,'chatslist.html', chatlist)

# returns the selected chat room page
@login_required(login_url = '/login/')
def chatroom(request, Chatroom_id):
    if Chatroom_id is None:
         return HttpResponseRedirect('/chatslist')
  #if the user does not belong to the chat return the chats list

    try:
        t=Chat.objects.get(id=Chatroom_id)
    except Chat.DoesNotExist:
        return HttpResponseRedirect('/chatslist')
	#see if the user belongs to the chat room
    if t.type !=2:
        try:
            Chat.objects.get(id=Chatroom_id,users=request.user)
        except Chat.DoesNotExist:
            return HttpResponseRedirect('/chatslist')

    chatid={}
    chatid.update(csrf(request))
    chatid['selectedchat']=Chat.objects.get(id=Chatroom_id)
	
    try:
        d=UserProfilePic.objects.get(user =  request.user)
        chatid['pic']=1
    except UserProfilePic.DoesNotExist:
        chatid['pic']=0


    return render(request,'chatroom.html',chatid)

# encapsulates the data into JSON format and 
# updates the messages in the selected chat room
@login_required(login_url='/login/')
@csrf_exempt
def chatroom_refresh (request,Chatroom_id):

    listMessages={}
    
    listMessages['selectedchat']=Chat.objects.get(id=Chatroom_id)
    s=Chat.objects.filter(id=Chatroom_id)
    listMessages['messages']=Message.objects.filter(chat=s)
    # Get request
    res = []
    for msgs in listMessages['messages']:
        try:
            d=UserProfilePic.objects.get(user =  msgs.username)
            d=1
        except UserProfilePic.DoesNotExist:
            d=0
        res.append({'img':d,'user_id':msgs.username.id,'username':msgs.username.username,'msg': msgs.message, 'timesent': msgs.timestamp.strftime('%I:%M %p | %d %b %y').lstrip('0')})

    data = json.dumps(res)
    
    return HttpResponse(data,content_type ='application/json')
    

# add a message to the selected chat room
@login_required(login_url='/login/')
def addMessage(request,Chatroom_id):
    a=Chat.objects.get(id=Chatroom_id)
    if 'q' in request.GET:
        mess = request.GET['q']

        # test to see if the text is empty
        test=mess
        test = test.replace(' ', '')
        if test=='' :
             return HttpResponseRedirect('/chatroom/'+Chatroom_id)

        
        c = Message(username = request.user,timestamp = timezone.now(),
                    chat = a,message=mess)
        
        c.save()


    return HttpResponseRedirect('/chatroom/'+Chatroom_id)



# displays the selected profile page
@login_required(login_url = '/login/')
def profile(request, profile_id):

    try:
        User.objects.get(id = profile_id)
    except User.DoesNotExist:
        return HttpResponseRedirect('/chatslist')

    P = {}
    P['Prof'] = User.objects.get(id = profile_id)
    s=User.objects.get(id = profile_id)
    try:
      P['Pic']=UserProfilePic.objects.get(user =  s)

    except UserProfilePic.DoesNotExist:
        P['Pic']= "";


    return render(request, 'profile/profilePage.html', P)

# updates the selected profile
@login_required(login_url = '/login/')
def update_profile(request, profile_id):


    a=User.objects.get(id = profile_id)

    if request.method == 'POST':

        form = ProfileUpdate(request.POST, instance=a)
        
        if form.is_valid():

            form.save()
            return HttpResponseRedirect('/profile/'+str(a.id))

    args={}
    args.update(csrf (request))
    args['form'] = ProfileUpdate(instance= a)
    return render(request,'profile/edit_profile.html', args)


# changes the profile picture of a user
def changeImage(request,profile_id):
    if request.method == 'POST':

        form = UserProfilePicForm(request.POST,request.FILES)

        if form.is_valid():

            try:
                UserProfilePic.objects.get(user = request.user).delete()



            except UserProfilePic.DoesNotExist:
                print("error")

            instance = form.save(commit=False)

            instance.user=request.user


            instance.save()


            return HttpResponseRedirect('/profile/'+str(profile_id))

    args={}
    args.update(csrf(request))
    args['form']=UserProfilePicForm()

    return render(request,'profile/changeImage.html',args)


# adds a contact and creates a 1-1 chat room with that contact
@login_required(login_url='/login/')
def addContact(request,profile_id):


    if 'q' in request.GET:
        name = request.GET['q']

        a=User.objects.get(id=profile_id)
        try:
            b=User.objects.get(username = name)
        except User.DoesNotExist:
            return render(request,'profile/add_contact.html',{'error':True,'msg':'User does not exist'})
        try:
          s=Chat.objects.filter(users=request.user, type=0 )


        except Chat.DoesNotExist:
            return render(request,'profile/add_contact.html',{'error':True,'msg':'User already added'})

        for i in s:

            if b in i.users.all():
                return render(request,'profile/add_contact.html',{'error':True,'msg':'User already added'})


        # create private 1-1 room
        ch = Chat( type = 0 , name = request.user.username + name)

        #forces the id to increment
        ch.save(force_insert=True)

        

        ch.users.add(request.user, b)

        return HttpResponseRedirect('/profile/'+str(request.user.id))


    return render(request, 'profile/add_contact.html')


# creates a private or public room
@login_required(login_url='/login/')
def createRoom(request,profile_id):

    if 'q' in request.GET:
        na = request.GET['q']

        # test to see if the text is empty
        test=na
        test = test.replace(' ', '')
        if test=='' :
             return render(request,'profile/createRoom.html',{'error':True,'msg':'Name can not be empty'})

        try:

            c=Chat.objects.get(name = na)

        except Chat.DoesNotExist:
				# gets the room type
                try:
                    ty = request.GET['roomType']
                    ty=2
                except KeyError:
                    ty=1

                ch = Chat( type = ty , name =  na)

                ch.save(force_insert=True)

                ch.users.add(request.user)

                return HttpResponseRedirect('/profile/'+str(request.user.id))

        return render(request,'profile/createRoom.html',{'error':True,'msg':'Name taken'})

    return render(request, 'profile/createRoom.html')






# adds a user to the private chat room
@login_required(login_url='/login/')
def addToChat(request, Chatroom_id):

   t={}
   t['ch_id']= Chatroom_id

   if 'q' in request.GET:
        na = request.GET['q']

        try:
           a=User.objects.get(username=na)
        except User.DoesNotExist:
            return render(request,'addToChat.html',{'error':True,'msg':'User does not exist'})


        try:
           b=Chat.objects.get(id = Chatroom_id)

        except Chat.DoesNotExist:
             return render(request,'addToChat.html',{'error':True,'msg':'Chat does not exist'})

        for i in b.users.all():
            if a == i:
                return render(request,'addToChat.html',{'error':True,'msg':'User already in chat'})



        b.users.add(a)

        return HttpResponseRedirect('/chatroom/'+str(Chatroom_id))

   return render(request, 'addToChat.html',t)


# returns the profile page of the user you searched for
@login_required(login_url='/login/')
def search(request):
    if 'q' in request.GET:
        na = request.GET['q']

        try:
           a=User.objects.get(username=na)
        except User.DoesNotExist:
            return render(request,'search.html',{'error':True,'msg':'User does not exist'})



        return HttpResponseRedirect('/profile/'+str(a.id))

    return render(request, 'search.html')