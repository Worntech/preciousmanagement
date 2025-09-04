from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

from .views import change_password
from .views import (
    CustomerListView, CustomerDetailView,
    CustomerCreateView, CustomerUpdateView, CustomerDeleteView
)

from django.views.generic import RedirectView

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
    path("allasset/", views.allasset, name="allasset"),
    # path("assethistory/<str:category_name>/", views.assethistory, name="assethistory"),
    path("assethistory/<str:category>/", views.assethistory, name="assethistory"),
    path("remove_asset/",views.remove_asset,name = "remove_asset"),
    # path("add_product/",views.add_product,name = "add_product"),
    path("addmaterial/",views.addmaterial,name = "addmaterial"),
    
    path("productin/",views.productin,name = "productin"),
    path("productout/",views.productout,name = "productout"),
    
    path("moneyin/",views.moneyin,name = "moneyin"),
    path("moneyout/",views.moneyout,name = "moneyout"),
    path("paysalary/",views.paysalary,name = "paysalary"),
    path("payedsalary/",views.payedsalary,name = "payedsalary"),
    path("addproduct/",views.addproduct,name = "addproduct"),
    path("moneyrequest/",views.moneyrequest,name = "moneyrequest"),
    # path("assethistory/",views.assethistory,name = "assethistory"),
    path("removed_asset/",views.removed_asset,name = "removed_asset"),
    # path("allasset/",views.allasset,name = "allasset"),
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
    path("products/", views.product_list, name="product_list"),
    path("stockremoved/",views.stockremoved,name = "stockremoved"),
    path("allstock/",views.allstock,name = "allstock"),
    
    # FOR VIEWING THE INFORMATION
    path("viewfarmer/<str:id>/",views.viewfarmer,name = "viewfarmer"),
    path("viewstaff/<str:id>/",views.viewstaff,name = "viewstaff"),
    path('viewmoneyrequest/<str:pk>/', views.viewmoneyrequest.as_view(), name = "viewmoneyrequest"),
    # path('viewproductbuy/<str:pk>/', views.viewproductbuy.as_view(), name = "viewproductbuy"),
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
    
# Utafutaji wa mkulima kuanza manunuzi
    path("purchase/search/", views.start_purchase, name="purchase_search"),

    # Ongeza bidhaa/manunuzi mapya kwa mkulima fulani
    path("purchase/select/<int:farmer_id>/", views.add_purchase, name="add_purchase"),

    # Maelezo ya manunuzi moja
    path("purchase/detail/<int:purchase_id>/", views.purchase_detail, name="purchase_detail"),

    # Historia ya manunuzi ya mkulima mmoja
    path("purchase/farmer/<int:farmer_id>/", views.farmer_purchases, name="farmer_purchases"),

    # Risiti printable
    path("purchase/print/<int:purchase_id>/", views.print_purchase, name="print_purchase"),
    

    # Kubadilisha status ya manunuzi kuwa 'paid'
    path("purchase/<int:purchase_id>/paid/", views.mark_purchase_paid, name="mark_purchase_paid"),

    # Kughairi manunuzi
    path("purchase/<int:purchase_id>/cancel/", views.cancel_purchase, name="cancel_purchase"),

    # Overall reports
    path("reports/purchases/", views.purchase_report_overall, name="purchase_report_overall_default"),
    path("reports/purchases/<str:period>/", views.purchase_report_overall, name="purchase_report_overall"),

    # Farmer reports (DEFAULT: month)
    path("reports/purchases/farmer/<int:farmer_id>/",
         views.purchase_report_farmer, {"period": "month"},
         name="purchase_report_farmer_default"),
    path("reports/purchases/farmer/<int:farmer_id>/<str:period>/",
         views.purchase_report_farmer, name="purchase_report_farmer"),

    # Export CSV (weka majina 2 tofauti ili kuepuka clash)
    path("reports/purchases/export/<str:scope>/<str:period>/",
         views.purchase_report_export_csv, name="purchase_report_export_csv"),
    path("reports/purchases/export/<str:scope>/<int:farmer_id>/<str:period>/",
         views.purchase_report_export_csv, name="purchase_report_export_csv_farmer"),

    # LEGACY redirects (hakikisha ZINAELEKEA kwenye MAJINA MAPYA hapo juu)
    path("purchase/report/",
         RedirectView.as_view(pattern_name="purchase_report_overall_default", permanent=False)),
    path("purchase/report/<str:period>/",
         RedirectView.as_view(pattern_name="purchase_report_overall", permanent=False)),
    path("purchase/<int:farmer_id>/report/",
         RedirectView.as_view(pattern_name="purchase_report_farmer_default", permanent=False)),
    path("purchase/<int:farmer_id>/report/<str:period>/",
         RedirectView.as_view(pattern_name="purchase_report_farmer", permanent=False)),

    # Farmer search (JINA SAHIHI)
    path("purchase/farmer/search/", views.purchase_farmer_search, name="purchase_farmer_search"),
    
    
    path("customers/", CustomerListView.as_view(), name="customer_list"),
    path("customers/create/", CustomerCreateView.as_view(), name="customer_create"),
    path("customers/<int:pk>/", CustomerDetailView.as_view(), name="customer_detail"),
    path("customers/<int:pk>/edit/", CustomerUpdateView.as_view(), name="customer_update"),
    path("customers/<int:pk>/delete/", CustomerDeleteView.as_view(), name="customer_delete"),
    
    # Products
    path("products/", views.product_list, name="product_list"),
    path("products/create/", views.product_create, name="product_create"),
    path("products/<int:pk>/edit/", views.product_update, name="product_update"),
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),

    # Additions
    path("additions/", views.addition_list, name="addition_list"),
    path("additions/create/", views.addition_create, name="addition_create"),
    path("additions/<int:pk>/<str:status>/", views.addition_mark, name="addition_mark"),
    path("additions/<int:pk>/delete/", views.addition_delete, name="addition_delete"),
    
    ##################################################
    # Orders
    path("orders/", views.order_list, name="order_list"),
    path("orders/<int:pk>/", views.order_detail, name="order_detail"),
    path("orders/<int:pk>/mark-paid/", views.order_mark_paid, name="order_mark_paid"),
    path("orders/<int:pk>/cancel-paid/", views.order_cancel_paid, name="order_cancel_paid"),

    # Customers + create order (smart routing)
    path("customers/search/", views.customer_search, name="customer_search"),
    path("customers/<int:customer_id>/orders/", views.customer_orders, name="customer_orders"),
    path("customers/<int:customer_id>/orders/create/", views.order_create_for_customer, name="order_create_for_customer"),

    # Documents
    path("orders/<int:pk>/invoice/", views.order_invoice, name="order_invoice"),                 # Billing Invoice
    path("orders/<int:pk>/proforma/", views.order_proforma, name="order_proforma"),             # Proforma Invoice
    path("orders/<int:pk>/purchase-order/", views.order_purchase_order, name="order_purchase_order"),
    path("orders/<int:pk>/delivery-note/", views.order_delivery_note, name="order_delivery_note"),
    path("orders/<int:pk>/goods-received/", views.order_goods_received_note, name="order_grn"),
    
    
    # Sales Reports
    path("reports/sales/", views.sales_report_overall, name="sales_report_overall_default"),
    path("reports/sales/<str:period>/", views.sales_report_overall, name="sales_report_overall"),

    # Per-customer Sales Reports (default: month)
    path("reports/sales/customer/search/", views.sales_customer_search, name="sales_customer_search"),
    path("reports/sales/customer/<int:customer_id>/", views.sales_report_customer, name="sales_report_customer_default"),
    path("reports/sales/customer/<int:customer_id>/<str:period>/", views.sales_report_customer, name="sales_report_customer"),

    # CSV export
    path("reports/sales/export/<str:scope>/<str:period>/", views.sales_report_export_csv, name="sales_report_export_csv"),
    path("reports/sales/export/<str:scope>/<int:customer_id>/<str:period>/", views.sales_report_export_csv, name="sales_report_export_csv_customer"),
    
    
    
    
    
    
    
    # Materials
    path("materials/", views.material_list, name="material_list"),
    path("materials/new/", views.material_create, name="material_create"),
    path("materials/<int:pk>/edit/", views.material_update, name="material_update"),
    path("materials/<int:pk>/toggle/", views.material_toggle, name="material_toggle"),
    path("materials/seed-defaults/", views.material_seed_defaults, name="material_seed_defaults"),

    # Receipts (Add stock)
    path("materials/receipts/", views.receipt_list, name="receipt_list"),
    path("materials/receipts/new/", views.receipt_create, name="receipt_create"),
    path("materials/receipts/<int:pk>/approve/", views.receipt_approve, name="receipt_approve"),
    path("materials/receipts/<int:pk>/reject/", views.receipt_reject, name="receipt_reject"),

    # Requisitions (Use stock)
    path("materials/requisitions/", views.requisition_list, name="requisition_list"),
    path("materials/requisitions/new/", views.requisition_create, name="requisition_create"),
    path("materials/requisitions/<int:pk>/approve/", views.requisition_approve, name="requisition_approve"),
    path("materials/requisitions/<int:pk>/reject/", views.requisition_reject, name="requisition_reject"),
    
    
    
    
    # Parties
    path("loans/parties/", views.party_list, name="party_list"),
    path("loans/parties/new/", views.party_create, name="party_create"),
    path("loans/parties/<int:pk>/edit/", views.party_update, name="party_update"),

    # Loans
    path("loans/", views.loan_list, name="loan_list"),
    path("loans/new/", views.loan_create, name="loan_create"),

    # Repayments
    path("repayments/", views.repayment_list, name="repayment_list"),
    path("repayments/new/", views.repayment_create, name="repayment_create"),
]