import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model


class State(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    abbreviation = models.CharField(_("Abbreviation"), max_length=50)
    country = models.CharField(_("Country"), max_length=50)
    # TODO possibly replace Postgres field with relation field
    default_counties = ArrayField(models.CharField(_("County Name"), max_length=80), size=8,
                                  help_text=_("Default Counties"))
    shelter_date = models.DateField(_("Shelter Date"))
    shelter_release_start_date = models.DateField(
        _("Shelter Release Start Date"))
    shelter_release_end_date = models.DateField(_("Shelter Release End Date"))
    social_distancing = models.BooleanField(
        _("Social Distancing"), default=True)
    social_distancing_end_date = models.DateField(
        _("Social Distancing End Date"))
    quarantine_percent = models.PositiveSmallIntegerField(
        _("Percentage Quarantined"), default=0)
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
    state = models.ForeignKey("State", verbose_name=_(
        "State"), on_delete=models.CASCADE)
    hospital_bed_capacity = models.IntegerField(
        _("Hospital Bed Capacity"), blank=True, null=True)
    icu_bed_capacity = models.IntegerField(
        _("ICU Bed Capacity"), blank=True, null=True)
    ventilator_capacity = models.IntegerField(
        _("Ventilator Capacity"), blank=True, null=True)

    class Meta:
        verbose_name = _("County")
        verbose_name_plural = _("Counties")

    def __str__(self):
        return '{} ({})'.format(self.name, self.state)

    def get_absolute_url(self):
        return reverse("County_detail", kwargs={"pk": self.pk})


class SimulationRun(models.Model):
    user = models.ForeignKey(get_user_model(), verbose_name=_(
        "User"), on_delete=models.CASCADE)
    model_input = JSONField(null=True, blank=True, unique=True  )
    model_output = JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(
        _("Timestamp"), auto_now=False, auto_now_add=True)
    webhook_token = models.UUIDField(
        _("Webhook Token"), default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name = _("Simulation Run")
        verbose_name_plural = _("Simulation Runs")

    def __str__(self):
        return "{} - {}".format(self.user, self.timestamp)

    def get_absolute_url(self):
        return reverse("SimulationRun_detail", kwargs={"pk": self.pk})
