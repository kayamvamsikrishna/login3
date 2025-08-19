from django.shortcuts import render
from app1.forms import *

from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail # send_email ,THIS IS FOR SENDING ONLY ONE MAIL, 
                                    # IF WE WANT TO SEND MULTIPLE MAILS MEANS USE   send_mass_mail 

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse



def home(request):
        if request.session.get('username'):
            username = request.session.get('username', request.user.username)
            pf= request.user.profile
            pic = pf.profile_pic.url 
            d = {'username': username, 'pic': pic}
            return render(request, 'home.html', d)
        else:
            pic='/media/default.jpg'
            d = {'pic': pic}
            return render(request, 'home.html',d)


def registration(request):
    EUFO=UserForm()#form object1 
    EPFO=ProfileForm()#form object2
    if request.user.is_authenticated:
            logout_url = reverse('user_logout')  # This generates the correct URL path
            html = f'''
                <html>
                    <body><br>
                        <h6>IF YOU WANT TO LOG OUT THEN TAP HERE:</h6>
                        <br>
                        <a href="{logout_url}" class="nav-link">Logout</a>
                    </body>
                </html>'''
            return HttpResponse(f'User is already logged in. You are unable to register a new user.<br>Try to logout first:<br>{html}')
    d={'EUFO':EUFO,'EPFO':EPFO}
    if request.method=='POST' and request.FILES: #initially it get false
        NMUFDO=UserForm(request.POST)
        NMPFDO=ProfileForm(request.POST,request.FILES)
        if NMUFDO.is_valid() and NMPFDO.is_valid():
            MUFDO=NMUFDO.save(commit=False)# to convert the data
            pw=NMUFDO.cleaned_data['password']
            MUFDO.set_password(pw) #to encript the data
            MUFDO.save()
            MPFDO=NMPFDO.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()

# SENDING OF MAILS
            
            send_mail('registration',
                       'thank you for registration',
                       'kayamvamsikrishna@gmail.com',
                       [MUFDO.email],
                       fail_silently=False

            )
            login_url = reverse('user_login')
            html = f'''<html>
                            <body><br>
                                    <h6>IF U WANT TO GET LOGIN THEN TAP HERE </h6>
                                <br>
                                <a href="{login_url}">USER LOGIN</a>
                            </body>
                        </html>'''
            return HttpResponse(f'REGISTRATION IS DONE SUCCESSFULLY {html}')
        else:
            registration_url = reverse('registration')
            html = f'''
            <html>
                <body><br>
                         <h6>TRY AGAIN PLEASE TAP HERE </h6>
                        <br>
                    <a href="{registration_url}">REGISTRATION</a>
                </body>
            </html>'''
            return HttpResponse(f'DATA IS INVALID{html}')
    return render(request,'registration.html',d)


def user_login(request):
    if request.method == 'POST':
        username = request.POST['un']
        password = request.POST['pw']

        # Empty field check
        if username == '' or password == '':
            return render(request, 'user_login.html')

        # Authenticate user
        AUO = authenticate(username=username, password=password)

        if AUO and AUO.is_active:
            login(request, AUO)
            request.session['username'] = username  # optional
            send_mail('user_login',
                       'Alert an unknown device is detected',
                       'kayamvamsikrishna@gmail.com',
                       [AUO.email],
                       fail_silently=False

            )
            return HttpResponseRedirect(reverse('home'))

        elif User.objects.filter(username=username).exists():
            # User exists but password might be wrong
            return render(request, 'user_login.html', {'error': 'Invalid password. Please try again.'})

        else:
            # User doesn't exist, suggest registration
            registration_url = reverse('registration')
            html = f'''
            <html>
                <body><br>
                    <h6>USER NOT FOUND. PLEASE REGISTER --- TAP HERE</h6><br>
                    <a href="{registration_url}">REGISTRATION</a>
                </body>
            </html>'''
            return HttpResponse(html)

    # GET request
    return render(request, 'user_login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def reset_password(request):
    if request.method=='POST':
        password=request.POST['password']
        username=request.POST['username']
        LUO=User.objects.filter(username=username)
        if LUO and password!='':
            UO=LUO[0]
            UO.set_password(password)
            UO.save()
            send_mail('reset_password',
                       'Successfully reset your password',
                       'kayamvamsikrishna@gmail.com',
                       [UO.email],
                       fail_silently=False

            )
            login_url = reverse('user_login')
            html = f'''
            <html>
                <body><br>
                         <h6>IF U WANT TO GET LOGIN THEN TAP HERE </h6>
                        <br>
                    <a href="{login_url}">USER LOGIN</a>
                </body>
            </html>
            '''
            return HttpResponse(f'SUCCESFULLY MODIFYING THE PASSWORD {html}')
        elif (username=='' and password=='') or (username=='' and password):
            return render(request,'reset_password.html')
        elif (LUO and password==''):
            return render(request,'reset_password.html')
        else:
            registration_url = reverse('registration')
            html = f'''
            <html>
                <body><br>
                         <h6>PLEASE REGISTER TAP HERE </h6>
                        <br>
                    <a href="{registration_url}">REGISTRATION</a>
                </body>
            </html>'''
            return HttpResponse(f'USERNAME NOT FOUND{html}')
    return render(request,'reset_password.html')