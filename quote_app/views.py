from django.shortcuts import render, redirect
from django.contrib import messages 
from .models import User, Quote 
import bcrypt


# Create your views here.
def index(request):
    return render(request,'index.html')
# might have to edit return function to say 'quotes/index.html' if the page does not render properly

def register(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create(
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )
        request.session['user_id'] = user.id
        request.session['greeting'] = user.email
        return redirect('/quotes')
        # this will redirect us to the quotes url


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = user.id
        request.session['greeting'] = user.email
        return redirect('/quotes')
        # this will also redirect us to the quotes url


def dashboard(request):
    # check to see if the user loggedin or registered by checking their session
    # if "user_id" not in request.session:
    #     return redirect('/')
    # the above may not be necessary
    context = {
        'all_quotes': Quote.objects.all(),
        'this_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request,'dashboard.html', context)
        # this will redirect us to the quotes url


def create_quote(request):
    errors = Quote.objects.quote_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    else:
        user = User.objects.get(id=request.session['user_id'])
        quote = Quote.objects.create(
            quoted_by = request.POST['quoted_by'],
            message = request.POST['message'],
            posted_by = user
        )
        return redirect('/quotes')
        # this will update the dashbaord to include a new quote


def users(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        'all_quotes': Quote.objects.filter(posted_by=user),
        'user': user,
        # 'quote': Quote.objects.get(id=user_id),
        # might need to change 'quote' to user to display indivdual user info with their quotes
        'current_user': User.objects.get(id=request.session['user_id'])
        # might need to change this to display quotes created by this specific user
    }
    return render(request,'users.html',context)
    # this will render us to an individal user page that displays quotes they posted


def update(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    quote.message = request.POST['message']
    quote.save()
    return users(request,request.session['user_id'])
    # return redirect('/quotes')
    # this will redirect us to a page that will aallow us to edit a quote


def edit(request, quote_id):
    context={
        'quote': Quote.objects.get(id=quote_id)
    }
    # quote.description = request.POST['description']
    # quote.save()
    return render(request,'edit.html', context)
    # this will redirect us to a page that will aallow us to edit a quote


def delete(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    quote.delete()
    return users(request,request.session['user_id'])
    # this will redirect us back to the same page but will be updated to no longer show quote that was deleted


def favorite(request, quote_id):
    user = User.objects.get(id=request.session['user_id'])
    quote = Quote.objects.get(id=quote_id)
    quote.favorited_by.add(user)
    return dashboard(request)
    #redirects to quotes page with the 


def unfavorite(request, quote_id):
    user = User.objects.get(id=request.session['user_id'])
    quote = Quote.objects.get(id=quote_id)
    quote.favorited_by.remove(user)
    return dashboard(request)


def logout(request):
    request.session.flush()
    return redirect('/')
    # logs user out of dashboard

