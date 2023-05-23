from django import forms
from election.models import Box, City, District, VoteReport, VoteReportVerification
from django.core.exceptions import ValidationError

class GetCityForm(forms.Form):
    city = forms.ModelChoiceField(City.objects.all(), label="Il", required=True)

class GetDistrictForm(forms.Form):
    city = forms.CharField(widget=forms.widgets.HiddenInput)
    district = forms.ModelChoiceField(District.objects.all(), label="Ilce", required=True)

class GetBoxForm(forms.Form):
    district = forms.CharField(widget=forms.widgets.HiddenInput)
    box_number = forms.IntegerField(required=True, label="Sandık Numarası", help_text="Sandık numarası 5 haneli rakamlardan oluşur.")

class CreateBoxForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = "__all__"

class CreateVoteReportForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        n1 = cleaned_data["n_kk"]+cleaned_data["n_rte"]
        n2 = cleaned_data["n_valid"]+cleaned_data["n_invalid"]

        if n1!=n2:
            raise ValidationError("Girilen oy sayilari toplami birbirine esit degil. Lutfen kontrol edin.", code="oy-sayilari-esit-degil")
                
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
    number = forms.IntegerField(disabled=True, label="Sandik Numarasi") 
    
    class Meta:
        model = District
        fields = ["number"]

class ReadonlyVoteReportForm(forms.ModelForm): 
    version = forms.IntegerField(disabled=True, label="Tutanak Versiyonu") 
    n_valid = forms.IntegerField(disabled=True, label="Gecerli Oy Sayisi")
    n_invalid = forms.IntegerField(disabled=True, label="Gecersiz Oy Sayisi")
    n_kk = forms.IntegerField(disabled=True, label="Kemal Kilicdaroglu")
    n_rte = forms.IntegerField(disabled=True, label="Tayyip Erdogan")
    
    class Meta:
        model = VoteReport
        fields = ["version","n_valid","n_invalid","n_kk","n_rte"]

class VerifyVoteReportForm(forms.ModelForm): 
    result = forms.ChoiceField(
        label="Tutanak ve veriler eslesiyor mu?",
        widget=forms.RadioSelect, 
        choices=[(True, "Evet"), (False, "Hayir")]
    )
    comment = forms.CharField(
        label="Eslesmiyorsa sebebini belirtiniz",
        min_length=0,
        max_length=180, 
        required=False,
        widget=forms.Textarea
    )

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data["source_ip"] == cleaned_data["report"].source_ip:
            raise ValidationError(u'Report creator and verifier cannot be the same.', code="invalid")

    class Meta:
        model = VoteReportVerification
        fields = ["report","result","comment","source_ip"]
        widgets = {'report': forms.HiddenInput(), "source_ip": forms.HiddenInput()}
