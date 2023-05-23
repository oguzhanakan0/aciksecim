from django import forms
from election.models import Box, City, District, VoteReport, VoteReportVerification
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

class GetCityForm(forms.Form):
    city = forms.ModelChoiceField(
        City.objects.all(), 
        label="Şehir", 
        help_text="Yurt dışı için listenin en sonuna kaydırınız.", 
        required=True
    )

class GetDistrictForm(forms.Form):
    city = forms.CharField(widget=forms.widgets.HiddenInput)
    district = forms.ModelChoiceField(District.objects.all(), label="Ilce", required=True)

class GetBoxForm(forms.Form):
    district = forms.CharField(widget=forms.widgets.HiddenInput)
    box_number = forms.IntegerField(required=True, label="Sandık Numarası")

class CreateBoxForm(forms.ModelForm):
    number = forms.IntegerField(required=True, label="Sandık Numarası", widget=forms.NumberInput(attrs={'placeholder': 12345}))
    captcha = CaptchaField(error_messages={"invalid":"CAPTCHA kodunu hatalı girdiniz."}, help_text="Kodu yenilemek için kod görseline tıklayın.")
    
    class Meta:
        model = Box
        fields = "__all__"
        widgets = {'district': forms.HiddenInput()}

class CreateVoteReportForm(forms.ModelForm):
    n_valid = forms.IntegerField(label="Geçerli Oy Sayısı", widget=forms.NumberInput(attrs={'placeholder': 123}))
    n_invalid = forms.IntegerField(label="Geçersiz Oy Sayısı", widget=forms.NumberInput(attrs={'placeholder': 123}))
    n_kk = forms.IntegerField(label="Kemal Kılıçdaroğlu Oy Sayısı", widget=forms.NumberInput(attrs={'placeholder': 123}))
    n_rte = forms.IntegerField(label="Tayyip Erdoğan Oy Sayısı", widget=forms.NumberInput(attrs={'placeholder': 123}))
    file = forms.FileField(
        label="Tutanak dosyası", 
        help_text="Kabul edilen dosya uzantıları: PNG, JPG, JPEG, PDF",
    )
    captcha = CaptchaField(error_messages={"invalid":"CAPTCHA kodunu hatalı girdiniz."}, help_text="Kodu yenilemek için kod görseline tıklayın.")

    def clean(self):
        cleaned_data = super().clean()
        n1 = cleaned_data["n_kk"]+cleaned_data["n_rte"]
        n2 = cleaned_data["n_valid"]+cleaned_data["n_invalid"]

        if n1!=n2:
            raise ValidationError("Girilen oy sayıları toplamı birbirine eşit değil. Lütfen kontrol edin.", code="oy-sayilari-esit-degil")
                
    class Meta:
        model = VoteReport
        fields = ["box","n_valid","n_invalid","n_kk","n_rte","file","source_ip"]
        widgets = {'box': forms.HiddenInput(), 'source_ip': forms.HiddenInput()}

class ReadonlyCityForm(forms.ModelForm): 
    name = forms.CharField(max_length=40, disabled=True, label="Il") 
    
    class Meta:
        model = City
        fields = ["name"]

class ReadonlyDistrictForm(forms.ModelForm): 
    name = forms.CharField(max_length=40, disabled=True, label="Ilce") 
    
    class Meta:
        model = District
        fields = ["name"]

class ReadonlyBoxForm(forms.ModelForm): 
    number = forms.IntegerField(disabled=True, label="Sandık Numarası") 
    
    class Meta:
        model = District
        fields = ["number"]

class ReadonlyVoteReportForm(forms.ModelForm): 
    version = forms.IntegerField(disabled=True, label="Versiyon") 
    n_valid = forms.IntegerField(disabled=True, label="Geçerli Oy")
    n_invalid = forms.IntegerField(disabled=True, label="Geçersiz Oy")
    n_kk = forms.IntegerField(disabled=True, label="K.K.")
    n_rte = forms.IntegerField(disabled=True, label="R.T.E.")
    
    class Meta:
        model = VoteReport
        fields = ["version","n_valid","n_invalid","n_kk","n_rte"]

class VerifyVoteReportForm(forms.ModelForm): 
    result = forms.ChoiceField(
        label="Tutanak ve veriler eşleşiyor mu?",
        widget=forms.RadioSelect, 
        choices=[(True, "Evet"), (False, "Hayır")]
    )
    comment = forms.CharField(
        label="Eşleşmiyorsa sebebini belirtiniz",
        min_length=0,
        max_length=180, 
        required=False,
        widget=forms.Textarea(attrs={'rows':4, 'cols':15, "placeholder":"Örnek: Sayılar eşleşmiyor, tutanak okunmuyor vs."})
    )
    captcha = CaptchaField(error_messages={"invalid":"CAPTCHA kodunu hatalı girdiniz."}, help_text="Kodu yenilemek için kod görseline tıklayın.")

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data["source_ip"] == cleaned_data["report"].source_ip:
            raise ValidationError(u'Tutanağı yükleyen kişi ile kontrol eden kişi aynı olamaz.', code="invalid")

    class Meta:
        model = VoteReportVerification
        fields = ["report","result","comment","source_ip"]
        widgets = {
            'report': forms.HiddenInput(), 
            "source_ip": forms.HiddenInput(),
        }

class DownloadAllReportsForm(forms.Form): 
    captcha = CaptchaField(error_messages={"invalid":"CAPTCHA kodunu hatalı girdiniz."}, help_text="Kodu yenilemek için kod görseline tıklayın.")
    