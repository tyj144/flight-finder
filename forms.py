from django import forms
from django.forms.extras.widgets import SelectDateWidget
import datetime

class IndexForm(forms.Form):
	start_loc = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Airport (ex. BOS, SEA)'}))
	start_date = forms.DateField(label='Depart date', initial=datetime.date.today(), widget=SelectDateWidget)
	end_date = forms.DateField(label='Return date', initial=datetime.date.today() + datetime.timedelta(days=7), widget=SelectDateWidget)