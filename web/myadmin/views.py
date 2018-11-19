from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.core.urlresolvers import reverse
from . import models
import time,os
from web.settings import BASE_DIR
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request,'myadmin/index.html')
#添加页面
def useradd(request):
    if request.method=='GET':
        # 返回页面
        return render(request,'myadmin/user/add.html')
    elif request.method=='POST':
        try:
            data = request.POST.dict()
            # print(data)
            data.pop('csrfmiddlewaretoken')
            # print(data)
            data['password']=make_password(data['password'], None, 'pbkdf2_sha256')
            # print(data['password'])
            myfile = request.FILES.get("pic_url")
            # print(myfile) 
            # 判断图片有没有提交
            if myfile:
                pic=upload(myfile)
                print(pic)
                data['pic_url']=pic
            else:
                data['pic_url']='/static/pics/default.jpg'
            #存数据
            # print(data)
            ob = models.Users(**data)
            # print(ob)
            ob.save()
            return HttpResponse('<script>alert(“添加成功”;loction.herf="'+reverse('mydamin_user_list')+'")</script>')
        except:
            return HttpResponse('<script>alert(“添加失败”;loction.herf="")</script>')
#查看所有信息
def userlist(request):
    data=models.Users.objects.all().exclude(status=3)
    # print(data)
    keywords = request.GET.get('keywords')
    print(keywords)
    types=request.GET.get('types')
     # 判断有没有条件查询
    if types:
        # 判断有没有搜索类型
        if types == 'all':
            # sql
            # select * from users where username like %keywords% or email like %keywords%
            # models.Users.objects.filter(username__contains('123'),email__contains('123'))
            # data = models.Users.objects.filter(username__contains('123'))
            # data.filter(,email__contains('123'))
            data = data.filter(Q(username__contains=keywords)|Q(phone__contains=keywords))
        elif types == 'sex':
            key={'男':'1','女':'0'}
            data = data.filter(sex__contains=key[keywords])
        else:
            # data = models.Users.objects.filter(usersname__contains=keywords)

            t = {types+'__contains':keywords}
            data = data.filter(**t)

     # 数据分页
    # 实例化分页类 第一个参数所有的数据集合 每页要显示的条数
    p = Paginator(data,20)
    # 统计所有的数据
    # sum_data=p.count
    # 获取可以分多少页 
    page_num=p.num_pages
    # 分页的范围 range(1,)
    pagenums = p.page_range
    
    # 接受页码
    pg = int(request.GET.get('p',1))
    # 判断当前页码不能小于1
    if pg<1:
        pg=1
    if pg>page_num:
        pg=page_num
    # 获取第几页的数据
    pagedata = p.page(pg)
    # 限制边界 如果当前页码小于或=3 只区前五条数据
    # 
    if pg <= 3:
        pag_list=pagenums[:5]
    elif pg+2> page_num:
         pag_list=pagenums[-5:]
    else:
        pag_list=pagenums[pg-3:pg+2]
    print(pag_list)
    return render(request,'myadmin/user/list.html',{'info':pagedata,'pagenums':pag_list,'pg':pg})
#删除数据
def userdel(request,id):
    ob=models.Users.objects.get(id=id)
    ob.status=3
    ob.save()

    # return HttpResponse('<script>alert("删除成功");location.href="'+reverse('myadmin_user_list')+'"</script>')
    return HttpResponse('<script>alert("删除成功");location.href="'+reverse('mydamin_user_list')+'"</script>')
#修改数据
def useredit(request,id):
    ob=models.Users.objects.get(id=id)
    if request.method=='GET':
        return render(request,'myadmin/user/edit.html',{'info':ob})
    elif request.method=='POST':
        ob.username=request.POST.get('username')
        #判断有没有提交密码 
        if request:
            ob.password=make_password(request.POST.get('password'), None, 'pbkdf2_sha256')
        ob.phone=request.POST.get('phone')
        ob.sex=request.POST.get('sex')
        ob.email=request.POST.get('email')
        # print(ob.pic_url)
        #判断有没有提交图片 如果提交了就把文件删除
        if request.FILES.get('pic_url'):
            # 删除原来的图片 /home/py15//static/pics/图片
            # 判是否用的默认头像如用的是默认头像 不做删除

            if ob.pic_url!='/static/pics/default.jpg':
                #如果上传图片，且原来也没有图片就设置为默认值图片
                try:
                    os.remove(BASE_DIR+ob.pic_url)
                except:
                    ob.pic_url='/static/pics/default.jpg'  
            # 讲提交上来的新图片写入到本地 并将地址入库
            myfile = request.FILES.get('pic_url')
            ob.pic_url=upload(myfile)
            
            ob.save()
        return HttpResponse(HttpResponse('<script>alert("修改成功");location.href="'+reverse('mydamin_user_list')+'"</script> '))

#图片上传
def upload(myfile):
    #执行图片的上传
    filename = str(time.time())+"."+myfile.name.split('.').pop()
    destination = open("./static/pics/"+filename,"wb+")
    for chunk in myfile.chunks():      # 分块写入文件  
        destination.write(chunk)  
    destination.close()
    # /static/picsn/图片
    return '/static/pics/'+filename