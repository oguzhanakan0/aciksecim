from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import CreateAPIView
from election.forms import GetCityForm, CreateBoxForm, ReadonlyBoxForm, ReadonlyCityForm, ReadonlyDistrictForm, ReadonlyVoteReportForm, CreateVoteReportForm, GetBoxForm, GetDistrictForm, VerifyVoteReportForm
from election.models import Box, District, VoteReport, VoteReportVerification
from election.serializers import BoxSerializer
from election.tables import VoteReportTable, BoxTable, VoteReportTableWide
from django_tables2 import RequestConfig

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

    return render(request, "election/search_box_form.html", {"form": form, "city": city, "district": district})

def get_or_create_box(request, city, district, box_number):
    not_found = False
    if request.method == "POST":
        form = CreateBoxForm(request.POST)
        if form.is_valid():
            box = form.save()
            return redirect(get_or_create_box, form.instance.district.city.slug, form.instance.district.slug, form.instance.number)
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
    table = BoxTable(Box.objects.filter(district__city__slug=city, district__slug=district).order_by('number')) # type: ignore
    return render(
        request, 
        "election/boxes.html", 
        {
            "city":city, 
            "district":district, 
            "box_table": table,
        }
    )

def get_all_reports(request, city, district):
    table = VoteReportTableWide(VoteReport.objects.filter(box__district__city__slug=city, box__district__slug=district).order_by('date')) # type: ignore
    return render(
        request, 
        "election/reports.html", 
        {
            "city":city, 
            "district":district, 
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
    city_form = ReadonlyCityForm(instance=report.box.district.city)
    district_form = ReadonlyDistrictForm(instance=report.box.district)
    box_form = ReadonlyBoxForm(instance=report.box)
    verify_vote_report_form = VerifyVoteReportForm(initial={"report":report.pk,"source_ip":get_client_ip(request)})
    return render(
        request, 
        "election/vote_report.html", 
        {
            "vote_report_form": vote_report_form,
            "city_form": city_form,
            "district_form": district_form,
            "box_form": box_form,
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
        

# API Views

def BoxCreateAPIView(CreateAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer