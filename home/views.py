from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.http import FileResponse
from .models import User,Product,PurchaseDetaile
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .fun import Calculate
from django.template.loader import render_to_string
# Create your views here.
types = {
    "1":"kitchen tiles",
    "2":"bedroom tiles",
    "3":"living room tiles",
    "4":"bathroom tiles",
    "5":"elevation",
    "6":"communicational site tiles",
    "7":"washroom pods",
    "8":"washbasin",
    "9":"parking tiles",
    "10":"premium floor",
    "11":"premium wall",
    "12":"premium elevation",
    "13":"vitrified tiles",
    "14":"gvt tiles"
}
tiles_detaile = {
    "1":"Ceramic Store grand range of exquisite kitchens floor tiles are a feast for eyes. The ultimate collection has the ability to transform any plain Jane dimension to an ultra-gorgeous one. The designer tiles are made using state-of-the art technology to ensure that each kitchen floor tile is of high quality. Our tiles are a perfect blend of mind-blowing designs with appealing colours and extraordinary finishes. The large collection is made to cater the individual styles and needs of our customers. Our constant quality checks and diligent workers ensure that we produce the best quality tiles.",
    "2":"Revamp your house with an eye-catching range of bedroom floor tiles by Ceramic Store. Manufactured with the help of advanced digital machinery, the assortment of floor tiles comes in various textures, and dimensions to match the interior of your house. The polished tiles by the brand have a reflective surface that effortlessly brighten up the whole area. The radiance of the floor tiles is durable and easy to keep up. To add that earthy and rustic look of natural wood to your bedroom or living room, choose from our eclectic collection of wooden floor tiles.",
    "3":"Ceramic Store brings an incredible selection of stylish and elegant looking living room wall tiles that gives a classy makeover to your dull room. Available in an elegant range of colours, textures, sizes, and designs, these tiles are manufactured using the modern and latest tile manufacturing technologies. Create unique patterns and eye catch designs with these magnificent tiles. Let there be no limit to your creativity. Choose tiles from the house of Ceramic Store to amp up the look of your living room.",
    "4":"Ceramic Store presents a supreme range of bathroom wall tiles. The all-new assortment of bathroom tiles is an epitome of creativity and advanced technology. Give your bathroom a makeover with our exclusive and classy range of wall tiles. We have categories ranging from ceramic tiles, glazed vitrified tiles & polished vitrified tiles, which comprises a huge variety of bathroom tiling. Wall tiles of these ranges are available in voluminous colours, patterns, sizes to give your space an astonishing look. This eclectic collection comes in glossy as well as matt finish.",
    "5":"A great product is created from the matchless craftsmanship and ingenious technology just as the exterior wall tiles crafted by Ceramic Store. These tiles are made to perfection and are versatile to be used in many different ways. Hence, they provide you complete liberty to unbridle your imaginations, making your own tailored space. With the aesthetic appeal in both shape and design, the exterior wall tiles by Ceramic Store offer high resistance and robust appearance to the outer walls. These tiles create a remarkable imprint of modern and stylish interior, enriching the space exquisitely.",
    "6":"Our range of floor tiles is as huge as ever! It is an amalgamation of industrial proficiency and exquisite designs. Each tile is made with excellence using the most advanced equipment and technology to ensure great quality. These exceptional floor tiles are also best commercial spaces shopping malls, restaurant, fashion store, office reception, hotels etc.",
    "7":"washroom pods",
    "8":"washbasin",
    "9":"parking tiles",
    "10":"premium floor",
    "11":"premium wall",
    "12":"premium elevation",
    "13":"vitrified tiles",
    "14":"gvt tiles"
}

def home(request):
    return render(request,"./MPR/home.html")

def login_page(request):
    if request.method=="POST":
        user=request.POST.get("username")
        password=request.POST.get("password")
        if not User.objects.filter(username=user).exists():
            return render(request,"./MPR/login.html",{"user":True})
        obj=authenticate(username=user,password=password)
        if obj is not None:
            login(request,obj)
            return redirect("home:home")
        return render(request,"./MPR/login.html")
    return render(request,"./MPR/login.html")

def register(request):
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        cpassword = request.POST.get("comfirm_password")
        email = request.POST.get("email")
        user = User.objects.filter(username=username)
        if cpassword!=password:
            return render(request,"./MPR/register.html")
        if user.exists():
            messages.info(request, "USERNAME ALREDY EXISTS !!")
            return render(request,"./MPR/register.html")
        
        user = User(username=username,email=email)
        user.set_password(password)
        user.save()
        return redirect("home:home")
    return render(request,"./MPR/register.html")

def logout_user(request):
    logout(request)
    return redirect("home:home")

def filter(request):
    category_id = request.GET.get('categoryId', None)
    data = Product.objects.filter(catagory_id=category_id)
    info = {"about":tiles_detaile[category_id],"name":types[category_id]}
    return render(request,"./MPR/product1.html",{"tiles":data,"info":info})

def filter_sidebar(request):
    size = request.GET.get('size', None)
    data = Product.objects.filter(size=size)
    return render(request,"./MPR/product1.html",{"tiles":data})

def download(request,filename):
    path=f'media/latest/{filename}'
    response = FileResponse(open(path,"rb"))
    return response

def cart(request):
    product=[]
    cartitem = request.session.get('cart',{})
    if len(cartitem)==0:
        return render(request,"./MPR/cart1.html",{"empty":True})
    else:
        for key in cartitem.keys():
            product.append(Product.objects.get(id=key))
    return render(request,"./MPR/cart1.html",{"items":product})

def deleteitem(request,id):
    cartitem = request.session.get('cart',{})
    del cartitem[str(id)]
    request.session['cart']=cartitem
    return redirect('home:cartpage')
    

def addtocart(request,id):
    cartitem = request.session.get('cart', {})
    if id in cartitem:
        cartitem[id]+=1
    else:
        cartitem[id]=1
    request.session['cart']=cartitem
    return redirect("home:cartpage")

def detaile(request):
    key=request.GET.get("product",None)
    product = Product.objects.get(id=key)
    return render(request,"./MPR/detaile1.html",{"product":product})

def purchase(request):  
    id = request.GET.get("name")
    user = request.user.username
    email=request.user.email
    product = Product.objects.get(id=id)
    product_name = product.name
    if request.method=="POST":
        length = int(request.POST.get("length"))
        breadth = int(request.POST.get("breadth"))
        area=lambda length,breadth:length*breadth
        price = product.price
        bands = request.POST.get("bands")
        light = int(request.POST.get("light"))
        dark = int(request.POST.get("dark"))
        high = int(request.POST.get("Highlighters"))
        address = request.POST.get("address")
        obj = Calculate(length,breadth,price,light,dark,high)
        PurchaseDetaile.objects.create(username=user,name=product_name,length=length,breadth=breadth,area=area(length,breadth),address=address)
        cart_detaile = obj.number_of_box(light,dark,high,price)
        cart_detaile["name"]=product.name
        mail_template = render_to_string("./MPR/email.html",{"items":cart_detaile})
        send_mail(
            'Transection',
            'rhis',
            'mr.goku.0619@gmail.com',
            ['mr.rahul.0619@gmail.com'],
            fail_silently=True,
            html_message=mail_template
        )
        return redirect("home:home")    
    return render(request,"./MPR/buy.html",{"product":product,"username":user})

