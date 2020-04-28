from django.db import models
from django.utils.translation import ugettext_lazy as _

class State(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    
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
