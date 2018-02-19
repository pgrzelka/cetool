import datetime
from django import forms

now = datetime.datetime.now()


class EcpForm(forms.Form):
    performer = forms.CharField(widget=forms.Textarea, label="Wykonawca")
    month = forms.IntegerField(min_value=1, max_value=12, label="Miesiąc", initial=now.month)
    year = forms.IntegerField(min_value=2017, label="Rok", initial=now.year)
    hours_sum = forms.IntegerField(min_value=0, label="Suma godzin", initial=0)
    hourly_bid = forms.IntegerField(min_value=0, label="Stawka godz", initial=50)
    sum = forms.IntegerField(min_value=0, label="Suma zł", initial=0)

    def __init__(self, *args, **kwargs):
        super(EcpForm, self).__init__(*args, **kwargs)
        counter = 1
        for q in range(1, 32):
            self.fields['day-' + str(counter)] = forms.CharField(label="Dzień {}".format(q), initial=0, required=False)
            self.fields['desc-' + str(counter)] = forms.CharField(label="Opis {}".format(q), initial="", required=False)
            counter += 1
