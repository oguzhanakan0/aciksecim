import django_tables2 as tables
from django_tables2.utils import A
from election.models import City, VoteReport, Box
import locale
locale.setlocale(locale.LC_ALL, '')

class VoteReportTable(tables.Table):
    version = tables.LinkColumn(verbose_name= 'Tutanak Versiyonu', args=[A('pk')])
    n_verify = tables.Column(accessor=A('n_verify'),verbose_name="Onay Sayısı")
    n_reject = tables.Column(accessor=A('n_reject'), verbose_name="Ret Sayısı")

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
        verbose_name="Sandık", 
        args=[A('city_slug'),A('district_slug'),A('box_number')])
    version = tables.LinkColumn(verbose_name= 'Versiyon')
    n_valid = tables.Column(verbose_name= 'Geçerli')
    n_invalid = tables.Column(verbose_name= 'Geçersiz')
    n_kk = tables.Column(verbose_name= 'K.K.')
    n_rte = tables.Column(verbose_name= 'R.T.E.')
    n_verify = tables.Column(accessor=A('n_verify'),verbose_name="Onay")
    n_reject = tables.Column(accessor=A('n_reject'), verbose_name="Ret")

    class Meta:
        model = VoteReport
        orderable = False
        fields = ("date","box_number","version","n_valid","n_invalid","n_kk","n_rte","n_verify","n_reject")
        template_name = 'django_tables2/bootstrap5.html'

class BoxTable(tables.Table):
    number = tables.LinkColumn(verbose_name= 'Sandık Numarası')

    class Meta:
        model = Box
        orderable = False
        fields = ("number", )

class StatisticsTable(tables.Table):
    id = tables.Column(verbose_name= 'İl Kodu')
    name = tables.LinkColumn("get-district", args=[A('slug')], verbose_name="Şehir")
    n_box = tables.Column(verbose_name= 'Resmi Sandık Sayısı')
    n_voter = tables.Column(verbose_name= 'Resmi Seçmen Sayısı')
    n_boxes = tables.Column(verbose_name="Girilen Sandık Sayısı",orderable=False)
    n_report = tables.Column(verbose_name="Girilen Tutanak Sayısı",orderable=False)
    n_report_verification = tables.Column(verbose_name="Tutanak Kontrol Sayısı",orderable=False)

    def render_n_box(self, value):
        return f'{value:n}'
    
    def render_n_voter(self, value):
        return f'{value:n}'

    class Meta:
        model = City
        orderable = True
        fields = ("id", "name", "n_box", "n_voter" )
