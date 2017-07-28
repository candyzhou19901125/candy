from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from sign.models import Event, Guest
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404


# Create your views here.
def index(request):
    return render(request, 'index.html')


def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', ' ')
        password = request.POST.get('password', ' ')
        if username == "" or password == "":
            return render(request, 'index.html', {'error': 'username or  password null!'})
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            # 将session信息记录到浏览器
            request.session['user'] = username
            response = HttpResponseRedirect('/event_manage/')
            # 添加浏览器cookie
            # response.set_cookie('user', username, 3600)
            return response
        else:
            return render(request, 'index.html', {'error': 'username or  password error!'})


@login_required
def event_manage(request):
    print(request.method)
    # username = request.COOKIES.get('user')
    event_list = Event.objects.all()
    username = request.session.get('user')
    print(username)
    return render(request, 'event_manage.html', {'user': username, 'events': event_list})


# 发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('user')
    search_name = request.GET.get('name')
    print(search_name)
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, 'event_manage.html', {'user': username, 'events': event_list})


# 嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 2)  # 划分每页显示两条数据
    page = request.GET.get('page')        # 通过GET请求得到当前要显示的第几页数据
    try:
        contacts = paginator.page(page)   # 获取第page页的数据
    except PageNotAnInteger:
        # 如果page不是整数，取第一页数据
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果page不在范围，取最后一页面
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts})


# 发布会名称搜索
@login_required
def search_phone(request):
    username = request.session.get('user')
    search_phone = request.GET.get('phone')
    guest_list = Guest.objects.filter(phone__contains=search_phone)
    paginator = Paginator(guest_list, 2)  # 划分每页显示两条数据
    page = request.GET.get('page')  # 通过GET请求得到当前要显示的第几页数据
    try:
        contacts = paginator.page(page)  # 获取第page页的数据
    except PageNotAnInteger:
        # 如果page不是整数，取第一页数据
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果page不在范围，取最后一页面
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts})


# 签到页面
@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    return render(request, 'sign_index.html', {'event': event})


# 签到动作
@login_required
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone', '')
    print(phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'phone error.'})
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'event id or phone error.'})
    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request,'sign_index.html',{'event':event, 'hint': 'user has sign in.'})
    else:
        Guest.objects.filter(phone=phone, event_id =eid).update(sign='1')
        return render(request, 'sign_index.html',{'event':event,  'hint': 'sign in success!', 'guest': result})


# 退出登录
@login_required
def logout(request):
    auth.logout(request)  # 退出登录
    response = HttpResponseRedirect('/index/')
    return response











