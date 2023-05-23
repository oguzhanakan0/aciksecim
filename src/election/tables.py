import django_tables2 as tables
from django_tables2.utils import A
from election.models import VoteReport, Box

class VoteReportTable(tables.Table):
    version = tables.LinkColumn(verbose_name= 'Tutanak Versiyonu', args=[A('pk')])
    n_verify = tables.Column(accessor=A('n_verify'),verbose_name="Onaylanma Sayisi")
    n_reject = tables.Column(accessor=A('n_reject'), verbose_name="Reddedilme Sayisi")

    class Meta:
        model = VoteReport
        orderable = False
        fields = ("version", "n_verify", "n_reject")
        template_name = 'django_tables2/bootstrap5.html'

class VoteReportTableWide(tables.Table):
    date = tables.Column(verbose_name= 'Tarih')
    box_number = tables.LinkColumn(
        "get-or-create-box",
        accessor=A('box_number'),
        verbose_name="Sandik Numarasi", 
        args=[A('city_slug'),A('district_slug'),A('box_number')])
    version = tables.LinkColumn(verbose_name= 'Tutanak Versiyonu')
    n_valid = tables.Column(verbose_name= 'Gecerli')
    n_invalid = tables.Column(verbose_name= 'Gecersiz')
    n_kk = tables.Column(verbose_name= 'K.K.')
    n_rte = tables.Column(verbose_name= 'R.T.E.')
    n_verify = tables.Column(accessor=A('n_verify'),verbose_name="Onaylanma Sayisi")
    n_reject = tables.Column(accessor=A('n_reject'), verbose_name="Reddedilme Sayisi")

    class Meta:
        model = VoteReport
        orderable = False
        fields = ("date","box_number","version","n_valid","n_invalid","n_kk","n_rte","n_verify","n_reject")
        template_name = 'django_tables2/bootstrap5.html'

class BoxTable(tables.Table):
    number = tables.LinkColumn(verbose_name= 'Sandik Numarasi')

    class Meta:
        model = Box
        orderable = False
        fields = ("number", )
