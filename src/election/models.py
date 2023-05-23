import uuid
from django.db import models
from django.utils.text import slugify 
from django.core.exceptions import ValidationError

# Validators

def validate_file_extension(value):
    if value.file.content_type not in [
        'application/pdf', 
        'image/png', 
        'image/jpeg',
        'image/jpg',
    ]:
        raise ValidationError(u'Invalid file format', code="invalid")

def validate_file_size(value):
    if value.file.size > 2621440:
        raise ValidationError(u'File too big', code="invalid")

# Models

class City(models.Model):
    id = models.IntegerField(unique=True)
    slug = models.SlugField(max_length=40, primary_key=True)
    name = models.CharField(max_length=40, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(City, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.id} - {self.name}"

class District(models.Model):
    slug = models.SlugField(max_length=40)
    name = models.CharField(max_length=40)
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="districts")
    n_box = models.IntegerField()
    n_voter = models.IntegerField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(District, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name}"

class Box(models.Model):
    number = models.IntegerField()
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name="boxes")

    def get_absolute_url(self):
        return f"/sandik/{self.district.city.slug}/{self.district.slug}/{self.number}/"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["number","district"],
                name='box_number_district_unique_constraint',),
        ]

class VoteReport(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid1, editable=False)
    box = models.ForeignKey(Box, on_delete=models.PROTECT, related_name="reports")
    version = models.IntegerField(default=1)
    n_valid = models.IntegerField() 
    n_invalid = models.IntegerField()
    n_kk = models.IntegerField()
    n_rte = models.IntegerField()
    file = models.FileField(upload_to='reports', validators=[validate_file_extension, validate_file_size])
    date = models.DateTimeField(auto_now_add=True)
    source_ip = models.GenericIPAddressField()

    def city_slug(self):
        return self.box.district.city.slug # type: ignore

    def district_slug(self):
        return self.box.district.slug # type: ignore

    def box_number(self):
        return self.box.number # type: ignore
    
    def n_verify(self):
        return self.verifications.filter(result=True).count() # type: ignore

    def n_reject(self):
        return self.verifications.filter(result=False).count() # type: ignore

    def save(self, *args, **kwargs):
        assert self.n_invalid+self.n_valid == self.n_kk+self.n_rte, "Toplam oy sayilari birbirini tutmuyor."
        self.version = VoteReport.objects.filter(box=self.box).count()+1
        super(VoteReport, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/tutanak/{self.pk}/"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["version","box"],
                name='version_box_unique_constraint',),
        ]


class VoteReportVerification(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid1, editable=False)
    report = models.ForeignKey(VoteReport, on_delete=models.PROTECT, related_name="verifications")
    source_ip = models.GenericIPAddressField()
    result = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["report","source_ip"],
                name='report_source_ip_unique_constraint',),
        ]

        