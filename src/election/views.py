from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django_tables2 import RequestConfig
from election.forms import (CreateBoxForm, CreateVoteReportForm, DownloadAllReportsForm, GetBoxForm,
                            GetCityForm, GetDistrictForm,
                            ReadonlyVoteReportForm, VerifyVoteReportForm)
from election.models import Box, City, District, VoteReport
from election.serializers import VoteReportSerializer
from election.tables import (BoxTable, StatisticsTable, VoteReportTable,
                             VoteReportTableWide)


# Template Views
def index(request):
    return render(request, "election/index.html")

def get_city(request):
    if request.method == "POST":
        form = GetCityForm(request.POST)
        if form.is_valid():
            return redirect(get_district, city=form.cleaned_data["city"].slug)
    else:
        form = GetCityForm()
    return render(request, "election/select_city_form.html", {"form": form})

def get_district(request, city):
    if request.method == "POST":
        form = GetDistrictForm(request.POST)
        if form.is_valid():
            return redirect(search_box, city=form.cleaned_data["city"], district=form.cleaned_data["district"].slug)
    else:
        form = GetDistrictForm(initial={"city":city})
        form.fields['district'].queryset = District.objects.filter(city__slug=city)
    return render(request, "election/select_district_form.html", {"form": form, "city":city})

def search_box(request, city, district):
    if request.method == "POST":
        form = GetBoxForm(request.POST)
        if form.is_valid():
            return redirect(get_or_create_box, city=city, district=district, box_number=form.cleaned_data["box_number"])
        else:
            print(form.errors)
    else:
        form = GetBoxForm(initial={"district":district})
    _city = City.objects.get(slug=city)
    _district = District.objects.get(city__slug=city,slug=district)
    return render(request, "election/search_box_form.html", {"form": form, "city": _city, "district": _district})

def get_or_create_box(request, city, district, box_number):
    not_found = False
    if request.method == "POST":
        print(request.POST)
        form = CreateBoxForm(request.POST)
        if form.is_valid():
            box = form.save()
            return redirect(get_or_create_box, form.instance.district.city.slug, form.instance.district.slug, form.instance.number)
        else:
            return render(request, "election/422.html", {"form": form})
    try: 
        box = Box.objects.get(district__city__slug=city, district__slug=district, number=box_number)
    except ObjectDoesNotExist:
        box = Box(district=District.objects.get(city__slug=city,slug=district), number=box_number)
        not_found = True
    box_form = CreateBoxForm(instance=box)
    vote_report_form = CreateVoteReportForm(instance=VoteReport(box=box,source_ip=get_client_ip(request)))

    return render(
        request, 
        "election/box.html", 
        {
            "not_found":not_found, 
            "box_form":box_form, 
            "vote_report_table": VoteReportTable(box.reports.all()) if box.id else None, # type: ignore
            "n_vote_report": box.reports.all().count() if box.id else 0, # type: ignore
            "vote_report_form": vote_report_form,
            "box":box
        }
    )

def create_vote_report(request):
    if request.method == "POST":
        form = CreateVoteReportForm(request.POST, request.FILES)
        if form.is_valid():
            vote_report = form.save()
            return redirect(
                get_or_create_box, 
                city=vote_report.box.district.city.slug, 
                district=vote_report.box.district.slug, 
                box_number=vote_report.box.number,
            )
        else:
            return render(request, "election/422.html", {"form": form})

    return render(request, "election/404.html")
    
def get_all_boxes(request, city, district):
    _district = District.objects.get(city__slug=city,slug=district)
    table = BoxTable(Box.objects.filter(district=_district).order_by('number'), empty_text="Bu ilçeye ait bir sandık bulunamadı. Lütfen önceki sayfaya dönüp sandık numarası girerek yeni bir sandık yaratın.") # type: ignore
    return render(
        request, 
        "election/boxes.html", 
        {
            "district":_district, 
            "box_table": table,
        }
    )

def get_all_reports(request, city, district):
    _district = District.objects.get(city__slug=city,slug=district)
    table = VoteReportTableWide(VoteReport.objects.filter(box__district=_district).order_by('date'), empty_text="Bu ilçeye ait bir tutanak bulunamadı.") # type: ignore
    return render(
        request, 
        "election/reports.html", 
        {
            "district":_district, 
            "report_table": table,
        }
    )

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_vote_report(request, pk):
    report = VoteReport.objects.get(pk=pk)
    vote_report_form = ReadonlyVoteReportForm(instance=report)
    verify_vote_report_form = VerifyVoteReportForm(initial={"report":report.pk,"source_ip":get_client_ip(request)})
    return render(
        request, 
        "election/vote_report.html", 
        {
            "report": report,
            "vote_report_form": vote_report_form,
            "verify_vote_report_form": verify_vote_report_form,
        }
    )

def verify_vote_report(request):
    if request.method == "POST":
        form = VerifyVoteReportForm(request.POST)
        print(form.instance.__dict__)
        if form.is_valid():
            print("form is valid")
            form.save()
            return redirect(get_or_create_box, form.instance.report.box.district.city.slug, form.instance.report.box.district.slug, form.instance.report.box.number)
        else:
            return render(request, "election/422.html", {"form": form})

    return render(request, "election/404.html")

def get_sss(request):
    return render(request, "election/sss.html")

def get_stats(request):
    table = StatisticsTable(City.objects.all()) # type: ignore
    form = DownloadAllReportsForm()
    RequestConfig(request, paginate={"per_page": 100}).configure(table)
    return render(request, "election/stats.html", {"table":table, "form":form})

def get_all_reports_json(request):
    if request.method == "POST":
        form = DownloadAllReportsForm(request.POST)
        if form.is_valid():
            return JsonResponse(
                VoteReportSerializer(VoteReport.objects.all(), many=True).data,
                safe=False,
                json_dumps_params={'ensure_ascii': False},
                headers={'Content-Disposition':'attachment'}
            )
        else:
            return render(request, "election/422.html", {"form": form})
    return HttpResponse(status=405)