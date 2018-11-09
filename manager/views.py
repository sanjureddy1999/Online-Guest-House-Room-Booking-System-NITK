from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from booking.models import *
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from booking.forms import GuestDetailsForm


# Create your views here.
def manager(request):
    try:
        if request.method == 'POST':
            username = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                if user.username and user.is_staff is True and user.is_superuser is False:
                    login(request, user)
                    return redirect('manager')
                else:
                    messages.warning(request, 'Email or Password does not match')
                    return redirect('login')
            else:
                messages.warning(request, 'Email or Password does not match')
                return redirect('login')
        else:
            user = request.user
            if user.username and user.is_staff is True and user.is_superuser is False:
                transactions = Transactions.objects.all().order_by('-start_date')
                guesthouse = GuestHouse.objects.all()
                print(transactions)
                page = request.GET.get('page', 1)
                paginator = Paginator(transactions, 4)
                try:
                    transactions = paginator.page(page)
                except PageNotAnInteger:
                    transactions = paginator.page(1)
                except EmptyPage:
                    transactions = paginator.page(paginator.num_pages)
                return render(request, 'manager/index.html', {'transactions': transactions, 'guesthouse': guesthouse})
            else:
                messages.warning(request, 'Email or Password does not match')
                return redirect('login')
    except Exception as e:
        messages.warning(request, str(e))
        return redirect('error')


def manager1(request, id):
    try:
        if request.method == 'POST':
            return redirect('manager')
        else:
            user = request.user
            if user.username and user.is_staff is True and user.is_superuser is False:
                transactions = Transactions.objects.all().order_by('-start_date').filter(guesthouse_id=id)
                print(transactions)
                guesthouse = GuestHouse.objects.all()
                page = request.GET.get('page', 1)
                paginator = Paginator(transactions, 4)
                try:
                    transactions = paginator.page(page)
                except PageNotAnInteger:
                    transactions = paginator.page(1)
                except EmptyPage:
                    transactions = paginator.page(paginator.num_pages)
                return render(request, 'manager/index.html', {'transactions': transactions, 'guesthouse': guesthouse})
            else:
                messages.warning(request, 'Email or Password does not match')
                return redirect('login')
    except Exception as e:
        messages.warning(request, str(e))
        return redirect('error')


def stats(request):
    try:
        if request.method == 'POST':
            return redirect('manager')
        else:
            user = request.user
            if user.username and user.is_staff is True and user.is_superuser is False:
                transactions = Transactions.objects.all().order_by('-start_date')
                guesthouse = GuestHouse.objects.all()
                print(transactions)
                start = datetime.date.today()-datetime.timedelta(days=10)
                day = []
                count = []
                while True:
                    day.append(str(start))
                    count.append(Transactions.objects.filter(date_book=start).__len__())
                    start = start + datetime.timedelta(days=1)
                    if start == datetime.date.today()+datetime.timedelta(days=1):
                        break
                print(day)
                print(count)
                return render(request, 'manager/stats.html', {'transactions': transactions, 'guesthouse': guesthouse, 'day': day, 'count': count})
            else:
                messages.warning(request, 'Email or Password does not match')
                return redirect('login')
    except Exception as e:
        messages.warning(request, str(e))
        return redirect('error')


def booking_details(request, id):
    try:
        if request.method == 'POST':
            return redirect('manager')
        else:
            user = request.user
            if user.username and user.is_staff is True and user.is_superuser is False:
                transactions = Transactions.objects.filter(id=id)
                guesthouse = GuestHouse.objects.all()
                guests = GuestDetails.objects.filter(transaction_id=id)
                return render(request, 'manager/details.html', {'transactions': transactions, 'guesthouse': guesthouse, 'guests': guests, 'form': GuestDetailsForm()})
            else:
                messages.warning(request, 'Email or Password does not match')
                return redirect('login')
    except Exception as e:
        messages.warning(request, str(e))
        return redirect('error')


def add_guest(request, id):
    try:
        if request.method == 'POST':
            user = request.user
            if user.username and user.is_staff is True and user.is_superuser is False:
                form = GuestDetailsForm(request.POST)
                if form.is_valid():
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    phone = form.cleaned_data['phone']
                    email = form.cleaned_data['email']
                    T = Transactions.objects.get(id=id)
                    G = GuestDetails()
                    G.transaction = T
                    G.first_name = first_name
                    G.last_name = last_name
                    G.phone = phone
                    G.email = email
                    G.save()
                return redirect('booking-details', id)
            else:
                messages.warning(request, 'Email or Password does not match')
                return redirect('login')
        else:
            return redirect('manager')
    except Exception as e:
        messages.warning(request, str(e))
        return redirect('error')


def delete_guest(request, t, id):
    try:
        if request.method == 'POST':
            return redirect('manager')
        else:
            user = request.user
            if user.username and user.is_staff is True and user.is_superuser is False:
                guest = GuestDetails.objects.get(id=id)
                if guest is not None:
                    guest.delete()
                return redirect('booking-details', t)
            else:
                messages.warning(request, 'Email or Password does not match')
                return redirect('login')
    except Exception as e:
        messages.warning(request, str(e))
        return redirect('error')