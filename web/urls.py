from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

from .views import change_password


from .views import (
    CustomPasswordResetView, CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView
)

urlpatterns = [
    path('signup', views.signup, name = "signup"),
    path('registervendors', views.registervendors, name = "registervendors"),
    path('signin', views.signin, name = "signin"),
	path('logout/', views.logout, name="logout"),
    path('change-password/', change_password, name='change_password'),
    
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='web/registration/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='web/registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='web/registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='web/registration/password_reset_complete.html'), name='password_reset_complete'),
 
    path("",views.home,name = "home"),
    path("aboutus",views.aboutus,name = "aboutus"),
    path("base",views.base,name = "base"),
    path("contactus",views.contactus,name = "contactus"),
    path("contactpost/",views.contactpost,name = "contactpost"),
    path("contactlist/",views.contactlist,name = "contactlist"),
    path("viewcontact/<int:id>/",views.viewcontact,name = "viewcontact"),
    path('deletecontact/<int:id>/', views.deletecontact, name = "deletecontact"),
    path("dashboard/",views.dashboard,name = "dashboard"),
    path("services/",views.services,name = "services"),
    path("shop/",views.shop,name = "shop"),
    
    path("add_farmers/",views.add_farmers,name = "add_farmers"),
    path("allstaff/",views.allstaff,name = "allstaff"),
    path("allvendors/",views.allvendors,name = "allvendors"),
    path("allfarmers/",views.allfarmers,name = "allfarmers"),
    path("add_asset/",views.add_asset,name = "add_asset"),
    path("add_product/",views.add_product,name = "add_product"),
    path("addmaterial/",views.addmaterial,name = "addmaterial"),
    
    path("productin/",views.productin,name = "productin"),
    path("productout/",views.productout,name = "productout"),
    
    path("moneyin/",views.moneyin,name = "moneyin"),
    path("moneyout/",views.moneyout,name = "moneyout"),
    path("paysalary/",views.paysalary,name = "paysalary"),
    path("payedsalary/",views.payedsalary,name = "payedsalary"),
    path("addproduct/",views.addproduct,name = "addproduct"),
    path("moneyrequest/",views.moneyrequest,name = "moneyrequest"),
    path("assethistory/",views.assethistory,name = "assethistory"),
    path("allasset/",views.allasset,name = "allasset"),
    path("moneyinlist/",views.moneyinlist,name = "moneyinlist"),
    path("moneyoutlist/",views.moneyoutlist,name = "moneyoutlist"),
    path("comb_honey/",views.comb_honey,name = "comb_honey"),
    path("honey/",views.honey,name = "honey"),
    path("wax/",views.wax,name = "wax"),
    path("requestedmoney/",views.requestedmoney,name = "requestedmoney"),
    path("acceptedmoney/",views.acceptedmoney,name = "acceptedmoney"),
    path("completedmoney/",views.completedmoney,name = "completedmoney"),
    path("declinedmoney/",views.declinedmoney,name = "declinedmoney"),
    path("myrequest/",views.myrequest,name = "myrequest"),
    path("allproduct/",views.allproduct,name = "allproduct"),
    path("allmaterial/",views.allmaterial,name = "allmaterial"),
    path("stockadded/",views.stockadded,name = "stockadded"),
    path("stockremoved/",views.stockremoved,name = "stockremoved"),
    path("allstock/",views.allstock,name = "allstock"),
    
    # FOR VIEWING THE INFORMATION
    path("viewfarmer/<str:id>/",views.viewfarmer,name = "viewfarmer"),
    path("viewstaff/<str:id>/",views.viewstaff,name = "viewstaff"),
    path('viewmoneyrequest/<str:pk>/', views.viewmoneyrequest.as_view(), name = "viewmoneyrequest"),
    path('viewproductbuy/<str:pk>/', views.viewproductbuy.as_view(), name = "viewproductbuy"),
    path("viewmoneyin/<str:id>/",views.viewmoneyin,name = "viewmoneyin"),
    path("viewmoneyout/<str:id>/",views.viewmoneyout,name = "viewmoneyout"),
    
    # FOR UPDATING INFORMATIONS
    path('updatefarmer/<int:pk>/', views.updatefarmer, name = "updatefarmer"),
    path('updatestaff/<int:pk>/', views.updatestaff, name = "updatestaff"),
    path('updateasset/<int:pk>/', views.updateasset, name = "updateasset"),
    path('updateallasset/<int:pk>/', views.updateallasset, name = "updateallasset"),
    path('updatemoneyrequested/<int:pk>/', views.updatemoneyrequested, name = "updatemoneyrequested"),
    path('updateproductbuy/<int:pk>/', views.updateproductbuy, name = "updateproductbuy"),
    path('updatepayedsalary/<int:pk>/', views.updatepayedsalary, name = "updatepayedsalary"),
    path('updateallproduct/<int:pk>/', views.updateallproduct, name = "updateallproduct"),
    path('updateallmaterial/<int:pk>/', views.updateallmaterial, name = "updateallmaterial"),
    path('updateproductin/<int:pk>/', views.updateproductin, name = "updateproductin"),
    path('updateproductout/<int:pk>/', views.updateproductout, name = "updateproductout"),
    path('updateallstock/<int:pk>/', views.updateallstock, name = "updateallstock"),
    
    path('updatemoneyin/<int:pk>/', views.updatemoneyin, name = "updatemoneyin"),
    path('updatemoneyout/<int:pk>/', views.updatemoneyout, name = "updatemoneyout"),
    
    # FOR DELETING INFORMATIONS
    path('deletefarmer/<int:pk>/', views.deletefarmer, name = "deletefarmer"),
    path('deletestaff/<int:pk>/', views.deletestaff, name = "deletestaff"),
    path('deleteasset/<int:pk>/', views.deleteasset, name = "deleteasset"),
    path('deleteallasset/<int:pk>/', views.deleteallasset, name = "deleteallasset"),
    path('deletemoneyrequest/<int:pk>/', views.deletemoneyrequest, name = "deletemoneyrequest"),
    path('deleteproductbuyw/<int:pk>/', views.deleteproductbuyw, name = "deleteproductbuyw"),
    path('deleteproductbuyc/<int:pk>/', views.deleteproductbuyc, name = "deleteproductbuyc"),
    path('deleteproductbuyh/<int:pk>/', views.deleteproductbuyh, name = "deleteproductbuyh"),
    path('deletepayedsalary/<int:pk>/', views.deletepayedsalary, name = "deletepayedsalary"),
    path('deleteallproduct/<int:pk>/', views.deleteallproduct, name = "deleteallproduct"),
    path('deleteallmaterial/<int:pk>/', views.deleteallmaterial, name = "deleteallmaterial"),
    path('deleteproductin/<int:pk>/', views.deleteproductin, name = "deleteproductin"),
    path('deleteproductout/<int:pk>/', views.deleteproductout, name = "deleteproductout"),
    path('deleteallstack/<int:pk>/', views.deleteallstack, name = "deleteallstack"),
    path('deleteqrcode/<int:pk>/', views.deleteqrcode, name = "deleteqrcode"),
    
    path('deletemoneyin/<int:pk>/', views.deletemoneyin, name = "deletemoneyin"),
    path('deletemoneyout/<int:pk>/', views.deletemoneyout, name = "deletemoneyout"),
    
    # for status
    path("moneyrequest_status/<int:id>/<str:status>/",views.moneyrequest_status,name = "moneyrequest_status"),
    path("moneyrequest_statusa/<int:id>/<str:status>/",views.moneyrequest_statusa,name = "moneyrequest_statusa"),
    path("moneyrequest_statusc/<int:id>/<str:status>/",views.moneyrequest_statusc,name = "moneyrequest_statusc"),
    path("moneyrequest_statusd/<int:id>/<str:status>/",views.moneyrequest_statusd,name = "moneyrequest_statusd"),
    
    # status for product and rawmaterials from the farmer
    path("farmerproduct_statusc/<int:id>/<str:status>/",views.farmerproduct_statusc,name = "farmerproduct_statusc"),
    path("farmerproduct_statush/<int:id>/<str:status>/",views.farmerproduct_statush,name = "farmerproduct_statush"),
    path("farmerproduct_statusw/<int:id>/<str:status>/",views.farmerproduct_statusw,name = "farmerproduct_statusw"),
    path("farmerproduct_statusg/<int:id>/<str:status>/",views.farmerproduct_statusg,name = "farmerproduct_statusg"),
    path("addproduct_status/<int:id>/<str:status>/",views.addproduct_status,name = "addproduct_status"),
    path("addmaterial_status/<int:id>/<str:status>/",views.addmaterial_status,name = "addmaterial_status"),
    
    path('request-qrcode/', views.request_qr_code, name='request_qr_code'),
    path('view-qrcodes/', views.view_qr_codes, name='view_qr_codes'),

]