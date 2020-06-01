from django import forms


class OrderForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.widget.attrs.update({'class': 'checkout-group__input form-control'})
    
    PAYMENT_TYPE = [
        ('bank', 'Банковской картой онлайн'),
        ('bill', 'Оплата по счету'),
        ('receipt', 'Оплата при получении'),
    ]
    fullname = forms.CharField(max_length=150, min_length=7)
    email = forms.EmailField(max_length=265)
    phone = forms.CharField(max_length=20)
    postcode = forms.CharField(max_length=10, required=False)
    region = forms.CharField(max_length=50, required=False)
    area = forms.CharField(max_length=50, required=False)
    city = forms.CharField(max_length=50, required=False)
    street = forms.CharField(max_length=50, required=False)
    house = forms.CharField(max_length=10, required=False)
    building = forms.CharField(max_length=20, required=False)
    apartment = forms.CharField(max_length=10, required=False)
    comment = forms.CharField(required=False, widget=forms.Textarea())
    payment_type = forms.ChoiceField(label='Тип оплаты', choices=PAYMENT_TYPE, widget=forms.Select())
    entity_name = forms.CharField(max_length=60, required=False)
    entity_inn = forms.CharField(max_length=13, required=False)
    entity_kpp = forms.CharField(max_length=20, required=False)
