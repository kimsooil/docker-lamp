from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _


class State(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    abbreviation = models.CharField(_("Abbreviation"), max_length=50)
    country = models.CharField(_("Country"), max_length=50)
    # TODO possibly replace Postgres field with relation field
    default_counties = ArrayField(models.CharField(_("County Name"), max_length=80), size=16,
                                  help_text=_("Default Counties"))
    shelter_date = models.DateField(_("Shelter Date"))
    shelter_release_start_date = models.DateField(_("Shelter Release Start Date"))
    shelter_release_end_date = models.DateField(_("Shelter Release End Date"))
    social_distancing = models.BooleanField(_("Social Distancing"), default=False)
    social_distancing_end_date = models.DateField(_("Social Distancing End Date"))
    quarantine_percent = models.PositiveSmallIntegerField(_("Percentage Quarantined"), default=0)
    quarantine_start_date = models.DateField(_("Quarantine Start Date"))

    class Meta:
        verbose_name = _("State")
        verbose_name_plural = _("States")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("State_detail", kwargs={"pk": self.pk})


# Create your models here.
class County(models.Model):
    name = models.CharField(_("County Name"), max_length=80)
    state = models.ForeignKey("State", verbose_name=_("State"), on_delete=models.CASCADE)
    hospital_bed_capacity = models.IntegerField(_("Hospital Bed Capacity"), blank=True, null=True)
    icu_bed_capacity = models.IntegerField(_("ICU Bed Capacity"), blank=True, null=True)
    ventilator_capacity = models.IntegerField(_("Ventilator Capacity"), blank=True, null=True)

    class Meta:
        verbose_name = _("County")
        verbose_name_plural = _("Counties")

    def __str__(self):
        return '{} ({})'.format(self.name, self.state)

    def get_absolute_url(self):
        return reverse("County_detail", kwargs={"pk": self.pk})
