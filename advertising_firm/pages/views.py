from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateformat import DateFormat

from .models import *
def main(request):
    context = {}
    if request.user.is_authenticated:
        user = request.user

        try:
            employee = Employee.objects.get(user=user).Role
        except:
            employee = ""
        context = {'user': user, 'employee': employee}

    return render(request, 'main.html', context=context)

def logout_func(request):
    logout(request)
    return redirect('main_page')


def sav_form(request):
    if request.method == 'POST':
        name_text = request.POST.get('name')
        last_name_text = request.POST.get('last_name')
        num_phone = request.POST.get('num_phone')
        email = request.POST.get('email')
        comment_text = request.POST.get('comment')


        review = Review(
            FullName=f"{name_text} {last_name_text}",
            number_phone=num_phone,
            email=email,
            Comment=comment_text
        )
        review.save()
    return redirect('main_page')



def auth(request):
    if request.method == 'POST':
        login_text = request.POST.get('login')
        password_text = request.POST.get('password')

        user = authenticate(username=login_text, password=password_text)

        if user is not None:
            login(request, user)
            messages.success(request, 'Авторизация прошла успешно!')

            if Employee.objects.filter(user=user).exists():
                return redirect('worker_view')
            else:
                return redirect('main_page')
        else:
            messages.error(request, 'Ошибка авторизации, неправильно введен пароль или логин')
            return redirect('auth')
    else:
        return render(request, 'auth.html')

    return redirect('main_page')



def sign_in(request):
    if request.method == 'POST':
        login_text = request.POST.get('login')
        email_text = request.POST.get('email')
        password_text = request.POST.get('password')
        name_text = request.POST.get('name')
        adress_text = request.POST.get('adress')

        try:
            # Создаем пользователя
            user = User.objects.create_user(username=login_text, email=email_text, password=password_text)

            # Создаем уровень с дефолтными значениями или выбираем существующий
            level, created = Level.objects.get_or_create(LevelName='Без уровня', defaults={'Discount': 0})

            # Создаем профиль
            profile = Profile(
                user=user,
                FullName=name_text,
                Address=adress_text,
                LevelID=level
            )
            profile.save()

            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('auth')

        except:
            messages.error(request, 'Ошибка регистрации. Пользователь с таким логином уже существует.')


        return redirect('sign_in')

    else:
        return render(request, 'sign_in.html')

@login_required
def create_appl(request):
    user = request.user
    if request.method == 'POST':
        profile = Profile.objects.get(user=user)
        level = profile.LevelID
        service_sel_id = request.POST.get('serviceSelect')
        price = request.POST.get('price').replace('от ', '').replace(' Руб', '')
        textfault = request.POST.get('textfault')

        # Найти выбранную услугу
        selected_service = Service.objects.get(ServiceID=service_sel_id)

        # Создать заказ
        order = Order(
            UserID=profile,
            Description=textfault,
            Status='В обработке',  # Установить начальный статус
            TotalAmount=(float(price) * (1 - float(profile.LevelID.Discount) / 100))
        )
        order.save()
        disc = profile.LevelID.Discount
        # Создать детали заказа
        order_detail = OrderDetail(
            OrderID=order,
            ServiceID=selected_service,
            Price=float(price),
            Discount= disc
        )
        order_detail.save()

        messages.success(request, 'Заявка успешно создана!')

        if level.Discount == 0:
            level.Discount = 5
            level.LevelName = 'Первый уровень'
        elif level.Discount == 5:
            level.Discount = 10
            level.LevelName = 'Второй уровень'
        elif level.Discount == 10:
            level.Discount = 15
            level.LevelName = 'Третий уровень'
        elif level.Discount == 15:
            level.Discount = 20
            level.LevelName = 'Четвертый уровень'
        elif level.Discount == 20:
            level.Discount = 0
            level.LevelName = 'Без уровня'
        level.save()

        return redirect('main_page')

    if Employee.objects.filter(user=user).exists():
        return redirect('main_page')
    else:
        services = Service.objects.all().values('ServiceID', 'ServiceName', 'Description', 'Price')
        profile = Profile.objects.get(user=user)

        return render(request, 'create_appl.html', {'services': list(services), 'user': user, 'profile': profile})


@login_required
def worker_view(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        ord_det = get_object_or_404(OrderDetail, OrderDetailID=id)
        order = ord_det.OrderID
        if order.Status == 'В обработке':
            order.Status = 'Принята'
        elif order.Status == 'Принята':
            order.Status = 'В разработке'
        elif order.Status == 'В разработке':
            order.Status = 'Выполнен'
        order.save()
        return redirect('worker_view')


    user = request.user
    try:
        employee = Employee.objects.get(user=user)
        orders = employee.orderd_work.all()

        orders_mas = []
        for order in orders:
            orders_list = {
                'order_id': order.OrderDetailID,
                'order_name': order.ServiceID.ServiceName,
                'user': f"{employee.FullName} {employee.Role}",
                'description': order.OrderID.Description,
                'order_date': DateFormat(order.OrderID.OrderDate).format('Y-m-d H:i:s'),
                'status': order.OrderID.Status
            }
            orders_mas.append(orders_list)
    except Employee.DoesNotExist:
        orders = None

    return render(request, 'worker.html', {'orders': orders_mas, 'employee': employee})