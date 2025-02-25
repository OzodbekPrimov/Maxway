import json

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from .services import *
from config.settings import MEDIA_ROOT
from .forms import *
def home_page(request):
    if request.GET:
        product = get_product_by_id(request.GET.get("product_id", 0))
        return JsonResponse(product)

def order_page(request):
    if request.GET:
        user = get_user_by_phone(request.GET.get("phone_number",0))
        return JsonResponse(user)

def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    orders = []
    orders_list = request.COOKIES.get("orders")
    total_price = request.COOKIES.get("total_price",0)
    print(orders_list)
    print(total_price)
    if orders_list:
        for key, val in json.loads(orders_list).items():
            orders.append(
                {
                "product": Product.objects.get(pk=int(key)),
                "count": val
                }
            )
    ctx = {
        'categories': categories,
        'products': products,
        'orders':orders,
        'total_price':total_price,
        'MEDIA_ROOT': MEDIA_ROOT
    }

    response = render(request, 'food/index.html', ctx)
    response.set_cookie("greeting", 'hello')
    return response

def main_order(request):
    model = Customer()
    if request.method == "POST":  # request.POST o‘rniga aniqroq
        try:
            model = Customer.objects.get(phone_number=request.POST.get("phone_number", ""))
        except Customer.DoesNotExist:
            model = Customer()

        form = CustomerForm(request.POST or None, instance=model)
        if form.is_valid():
            customer = form.save()
            formOrder = OrderForm(request.POST or None, instance=Order())
            if formOrder.is_valid():
                order = formOrder.save(customer=customer)
                print("order:", order)

                # Cookie dan orders_list ni olish
                orders_list = request.COOKIES.get("orders")
                if not orders_list:  # Agar cookie bo‘lmasa
                    print("Cookie da orders yo‘q")
                    return redirect("index")  # Yoki boshqa logic

                try:
                    orders_dict = json.loads(orders_list)  # JSON parse qilish
                except (json.JSONDecodeError, TypeError):
                    print("Cookie formati noto‘g‘ri")
                    return redirect("index")  # Xato bo‘lsa redirect

                # Har bir mahsulot uchun
                for key, value in orders_dict.items():
                    product = get_product_by_id(int(key))
                    if product:  # Agar mahsulot topilsa
                        counts = value
                        order_product = OrderProduct(
                            count=counts,
                            price=product['price'],
                            product_id=product['id'],
                            order_id=order.id
                        )
                        order_product.save()
                    else:
                        print(f"Mahsulot ID={key} topilmadi")

                # Cookie ni o‘chirish (ixtiyoriy)
                response = redirect("index")
                response.delete_cookie("orders")
                return response

            else:
                print(formOrder.errors)
        else:
            print(form.errors)

    categories = Category.objects.all()
    products = Product.objects.all()
    orders = []
    orders_list = request.COOKIES.get("orders")
    total_price = request.COOKIES.get("total_price")
    if orders_list:
        for key, val in json.loads(orders_list).items():
            orders.append(
                {
                "product": Product.objects.get(pk=int(key)),
                "count": val
                }
            )
    ctx = {
        'categories': categories,
        'products': products,
        'orders':orders,
        'total_price':total_price,
        'MEDIA_ROOT': MEDIA_ROOT,
    }

    response = render(request, 'food/order.html', ctx)
    response.set_cookie("greeting", 'hello')
    return response

# def send_order(request):
#     return redirect(index)
    # return render(request,'food/order.html')