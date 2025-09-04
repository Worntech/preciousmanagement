from django.forms import ModelForm
from django import forms
from .models import *

from django.contrib.auth.forms import UserCreationForm
from .models import QRCode
from .models import Farmer

from django.forms import inlineformset_factory
from .models import Purchase, PurchaseItem

from django.forms import modelformset_factory, inlineformset_factory
from .models import SalesOrder, SalesOrderItem

class MyUserForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['email', 'username']

class StaffForm(ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'middle_name', 'last_name', 'gender', 'village', 'ward', 'district', 'region', 'designation', 'mobile_number', 'nin_number', 'postal_code', 'email', 'username', 'profile_picture']

class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['first_name', 'middle_name', 'last_name', 'gender', 'village', 'ward', 'district', 'region', 'mobile_number', 'nin_number', 'postal_code', 'total_beehives', 'ttb_beehives', 'tch_beehives', 'ktbh_beehives', 'local_beehives', 'colonized_beehives', 'uncolonized_beehives', 'mwanzo', 'malengo', 'muhamasishaji', 'kiasi_mwisho', 'kufanikisha_nin', 'kusaidia_mazingira', 'familia_mtazamo']

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            'asset_name',
            'category',
            'assigned_to',
            'location',
            'purchase_date',
            'purchase_cost',
            'current_value',
            'depreciation_rate',
            'expected_life_years',
            'status',
            'condition',
            'warranty_expiry',
            'last_service_date',
            'next_service_due',
            'assigned_to',
        ]

        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'warranty_expiry': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'last_service_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'next_service_due': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'asset_name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'purchase_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_value': forms.NumberInput(attrs={'class': 'form-control'}),
            'depreciation_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'expected_life_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            # 'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_purchase_cost(self):
        cost = self.cleaned_data.get('purchase_cost')
        if cost is not None and cost < 0:
            raise forms.ValidationError("Purchase cost cannot be negative.")
        return cost

    def clean_current_value(self):
        value = self.cleaned_data.get('current_value')
        if value is not None and value < 0:
            raise forms.ValidationError("Current value cannot be negative.")
        return value
        
class AllAssetForm(forms.ModelForm):
    class Meta:
        model = AllAsset
        fields = '__all__'

class FarmerSearchForm(forms.Form):
    query = forms.CharField(label="Tafuta Farmer", max_length=100)
    

# PurchaseItemFormSet = inlineformset_factory(
#     parent_model=Purchase,
#     model=PurchaseItem,
#     fields=("barcode_data", "product_name", "quantity", "unit_price"),
#     extra=0,
#     can_delete=True,
#     # fk_name="purchase",  # UNAHITAJI HII tu kama FK si 'purchase'
# )

class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ("barcode_data", "product_name", "quantity", "unit_price")
        widgets = {
            "barcode_data": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter barcode (optional)",
                "autocomplete": "off",
            }),
            "product_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Product name",
                "autocomplete": "off",
            }),
            "quantity": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "1",
                "min": "0",
                "placeholder": "Qty",
            }),
            "unit_price": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "min": "0",
                "placeholder": "Price",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 🔒 Force kuwa TextInput (ikizidi kubadilishwa mahali pengine)
        self.fields["barcode_data"].required = False
        self.fields["barcode_data"].widget = forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter barcode (optional)",
            "autocomplete": "off",
        })


PurchaseItemFormSet = inlineformset_factory(
    parent_model=Purchase,
    model=PurchaseItem,
    form=PurchaseItemForm,
    fields=("barcode_data", "product_name", "quantity", "unit_price"),
    extra=0,          # rows mpya utaongeza kwa JS
    can_delete=True,
    # fk_name="purchase",
)

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ("code", "created_at", "updated_at")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Jina la mteja/ kampuni"}),
            "company_name": forms.TextInput(attrs={"class": "form-control"}),
            "contact_person": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "alt_phone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "alt_email": forms.EmailInput(attrs={"class": "form-control"}),
            "address_line1": forms.TextInput(attrs={"class": "form-control"}),
            "address_line2": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "region": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control"}),
            "tin": forms.TextInput(attrs={"class": "form-control"}),
            "vat_number": forms.TextInput(attrs={"class": "form-control"}),
            "payment_terms": forms.Select(attrs={"class": "form-select"}),
            "credit_limit": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Maelezo ya ziada"}),
        }
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "unit", "stock", "unit_price", "is_active"]
        widgets = {
            "name": forms.Select(attrs={"class": "form-select"}),  # Chaguo la bidhaa ulizotaja
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "unit": forms.Select(attrs={"class": "form-select"}),
            "stock": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "unit_price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": 0}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ProductAdditionForm(forms.ModelForm):
    class Meta:
        model = ProductAdditionHistory
        fields = ["product", "quantity", "note"]
        widgets = {
            "product": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "note": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }
        

class SalesOrderForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        fields = ("customer", "notes")
        widgets = {
            "customer": forms.Select(attrs={"class": "form-select"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Notes (optional)"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # mara nyingi kwenye "create-for-customer" tunam-fix customer
        if "customer" in self.fields:
            self.fields["customer"].widget.attrs["readonly"] = True
            self.fields["customer"].disabled = True  # huzuia kubadilishwa client-side


class SalesOrderItemForm(forms.ModelForm):
    class Meta:
        model = SalesOrderItem
        fields = ("product", "quantity", "unit_price")
        widgets = {
            "product": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "min": "1", "step": "1", "placeholder": "Qty"}),
            "unit_price": forms.NumberInput(attrs={"class": "form-control", "min": "0", "step": "0.01", "placeholder": "Price"}),
        }

# CREATE PAGE: tumia ModelFormSet (bila instance) — order bado haija-save
SalesOrderItemCreateFormSet = modelformset_factory(
    SalesOrderItem,
    form=SalesOrderItemForm,
    fields=("product", "quantity", "unit_price"),
    extra=1,
    can_delete=True,   # kufuta rows kabla ya submit (JS pia inashughulikia)
)

# EDIT PAGE: tumia InlineFormSet (na instance=order) — kufuta/update/add kwenye DB
SalesOrderItemInlineFormSet = inlineformset_factory(
    SalesOrder,
    SalesOrderItem,
    form=SalesOrderItemForm,
    fields=("product", "quantity", "unit_price"),
    extra=0,
    can_delete=True,
    fk_name="order",
)

      
class ProductSellForm(forms.ModelForm):
    class Meta:
        model = ProductSell
        fields = ['seller_name', 'product_name', 'barcode', 'amount', 'weight']
        
class CommentProductSellForm(forms.ModelForm):
    content = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={

            'rows': '4',
            'id': 'content',
            'placeholder' : 'Write Your Comment Here',
        }))
    class Meta:
        model = CommentProductSell
        fields = ('content',)
        
class MasterAmountForm(forms.ModelForm):
    class Meta:
        model = MasterAmount
        fields = ['amount']
        
class VendorAmountForm(forms.ModelForm):
    class Meta:
        model = VendorAmount
        fields = ['amount']
        
class MoneyRequestForm(forms.ModelForm):
    class Meta:
        model = MoneyRequest
        fields = ['amount', 'purpose']
        
class CommentMoneyRequestForm(forms.ModelForm):
    content = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={

            'rows': '4',
            'id': 'content',
            'placeholder' : 'Write Your Comment Here',
        }))
    class Meta:
        model = CommentMoneyRequest
        fields = ('content',)
        
class MoneyinForm(forms.ModelForm):
    class Meta:
        model = Moneyin
        fields = ['amount', 'money_source', 'money_processor']

class MoneyoutForm(forms.ModelForm):
    class Meta:
        model = Moneyout
        fields = ['amount', 'purpose', 'money_user']
              
class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ['amount', 'payed_Name', 'paymentperiod']
        
        
class CommentProductForm(forms.ModelForm):
    content = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={

            'rows': '4',
            'id': 'content',
            'placeholder' : 'Write Your Comment Here',
        }))
    class Meta:
        model = CommentProduct
        fields = ('content',)
        
class CommentMaterialForm(forms.ModelForm):
    content = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={

            'rows': '4',
            'id': 'content',
            'placeholder' : 'Write Your Comment Here',
        }))
    class Meta:
        model = CommentMaterial
        fields = ('content',)


class ProductinForm(forms.ModelForm):
    class Meta:
        model = Productin
        fields = ['honey', 'wax']
        
class ProductoutForm(forms.ModelForm):
    class Meta:
        model = Productout
        fields = ['wax', 'honey']
        
              
class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class QRCodeForm(forms.ModelForm):
    class Meta:
        model = QRCode
        fields = ['qr_code_name', 'image']



################## for materials ##################
class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ["name", "unit", "stock", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control", "placeholder":"Material name"}),
            "unit": forms.Select(attrs={"class":"form-select"}),
            "stock": forms.NumberInput(attrs={"class":"form-control", "min":0}),
            "is_active": forms.CheckboxInput(attrs={"class":"form-check-input"}),
        }

class MaterialReceiptForm(forms.ModelForm):
    class Meta:
        model = MaterialReceipt
        fields = ["material", "quantity", "status", "note"]
        widgets = {
            "material": forms.Select(attrs={"class":"form-select"}),
            "quantity": forms.NumberInput(attrs={"class":"form-control", "min":1}),
            "status": forms.Select(attrs={"class":"form-select"}),
            "note": forms.Textarea(attrs={"class":"form-control", "rows":3, "placeholder":"Optional note"}),
        }

class MaterialRequisitionForm(forms.ModelForm):
    class Meta:
        model = MaterialRequisition
        fields = ["material", "quantity", "status", "note"]
        widgets = {
            "material": forms.Select(attrs={"class":"form-select"}),
            "quantity": forms.NumberInput(attrs={"class":"form-control", "min":1}),
            "status": forms.Select(attrs={"class":"form-select"}),
            "note": forms.Textarea(attrs={"class":"form-control", "rows":3, "placeholder":"Reason / usage"}),
        }
        
        
        
        
        
        
        
        
class PartyForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = ["name", "email", "phone", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control", "placeholder":"Party name"}),
            "email": forms.EmailInput(attrs={"class":"form-control"}),
            "phone": forms.TextInput(attrs={"class":"form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class":"form-check-input"}),
        }

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ["party", "type", "amount", "note"]
        widgets = {
            "party": forms.Select(attrs={"class":"form-select"}),
            "type": forms.Select(attrs={"class":"form-select"}),
            "amount": forms.NumberInput(attrs={"class":"form-control", "min":"0", "step":"0.01"}),
            "note": forms.Textarea(attrs={"class":"form-control", "rows":3}),
        }

class RepaymentForm(forms.ModelForm):
    class Meta:
        model = Repayment
        fields = ["party", "type", "amount", "note"]
        widgets = {
            "party": forms.Select(attrs={"class":"form-select"}),
            "type": forms.Select(attrs={"class":"form-select"}),
            "amount": forms.NumberInput(attrs={"class":"form-control", "min":"0", "step":"0.01"}),
            "note": forms.Textarea(attrs={"class":"form-control", "rows":3}),
        }