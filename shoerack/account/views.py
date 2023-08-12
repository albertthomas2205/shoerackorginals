from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from adminside.forms import UserdetailsForm  #

from user.models import Userdetails,CustomUser
from cart.models import Order
    



# Create your views here.
def profilehome(request):
    return render(request,'profile/profilehome.html')


def viewaddress(request):
    # Retrieve the logged-in user's details
    addresses = Userdetails.objects.filter(userr=request.user)
    print('haiiii')
    print(addresses)

    # Pass the user_details object to the HTML template
    return render(request, 'profile/viewadddress.html', {'addresses': addresses})

def addaddress(request):
    if request.method == 'POST':
        form = UserdetailsForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.userr = request.user  # Assuming you have a CustomUser model and using request.user for the logged-in user
            address.save()
            return redirect('viewaddress')  # Replace 'address_list' with the URL name of the page displaying the list of addresses
    else:
        form = UserdetailsForm()
    
    return render(request, 'profile/addaddress.html', {'form': form})

from django.http import JsonResponse

def delete_address(request):
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        try:
            address = Userdetails.objects.get(pk=address_id)
            address.delete()
            return JsonResponse({'success': True})
        except Userdetails.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Address not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


def editaddress(request, userdetails_id):
    userdetails = get_object_or_404(Userdetails, id=userdetails_id)

    if request.method == 'POST':
        form = UserdetailsForm(request.POST, instance=userdetails)
        if form.is_valid():
            form.save()
            return redirect('viewaddress')  # Replace with the URL name for success
    else:
        form = UserdetailsForm(instance=userdetails)

    context = {'form': form}
    return render(request, 'profile/editaddress.html', context)

def userorders(request):
    cust = get_object_or_404(CustomUser, id=request.user.id)
    orders=Order.objects.filter(user=cust)
    
    context={'orders':orders,'cust':cust}
    return render(request,'profile/orders.html',context)

def Usercancel(request,id):
    edit=get_object_or_404(Order,id=id)
    edit.status='C'
    edit.save()
    return redirect('userorders')
    

