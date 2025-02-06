from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .models import QRCode

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
        fields = ['first_name', 'middle_name', 'last_name', 'gender', 'village', 'ward', 'district', 'region', 'mobile_number', 'nin_number', 'postal_code', 'total_beehives', 'ttb_beehives', 'top_bar_beehives', 'tch_beehives', 'ktbh_beehives', 'local_beehives', 'colonized_beehives', 'uncolonized_beehives', 'farmer_background']
        
class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['asset_name', 'quantity']
        
class AllAssetForm(forms.ModelForm):
    class Meta:
        model = AllAsset
        fields = '__all__'
        
class ProductBuyForm(forms.ModelForm):
    class Meta:
        model = ProductBuy
        fields = ['seller_name', 'product_name', 'barcode', 'weight']
        
class CommentProductBuyForm(forms.ModelForm):
    content = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={

            'rows': '4',
            'id': 'content',
            'placeholder' : 'Write Your Comment Here',
        }))
    class Meta:
        model = CommentProductBuy
        fields = ('content',)

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
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['used_rawmaterial', 'honey', 'wax', 'comment']
        
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
        
class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['wax', 'comb_honey', 'honey', 'comment']
        
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
