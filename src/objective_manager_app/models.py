from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from datetime import datetime
from django.contrib.auth.models import User

class CodeKategorie(models.Model):
    titel = models.CharField(max_length=100)
    beschreibung = models.CharField(max_length=200)

    def __str__(self):
        return self.kategorie


class Organisation(models.Model):
    departement = models.CharField(max_length=200)
    dienststelle = models.CharField(max_length=200)
    bereich = models.CharField(max_length=200)
    departement_kuerzel = models.CharField(max_length=200)
    dienststelle_kuerzel = models.CharField(max_length=200)
    bereich_kuerzel = models.CharField(max_length=200)
    
    def __str__(self):
        return self.bereich if self.bereich else self.dienststelle

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    vorname = models.CharField(verbose_name= 'Vorname', max_length=200)
    nachname = models.CharField(verbose_name= 'Nachname', max_length=200)
    email = models.EmailField(verbose_name= 'Email', max_length=200, null=True, blank=True)
    telefon = models.CharField(verbose_name= 'Telefon', max_length=200, null=True, blank=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    erstellt_am = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vorname} {self.nachname}"


class NeuBestehendManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(kategorie_id=2)


class RolleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(kategorie_id=3)
    

class Code(models.Model):
    kategorie = models.ForeignKey(CodeKategorie, on_delete=models.CASCADE)
    kuerzel = models.CharField(max_length=10)
    titel = models.CharField(max_length=10)
    beschreibung = models.CharField(max_length=200)

    def __str__(self):
        return self.titel


class ThemaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(typ_id=1)


class HandlungsfeldManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(typ_id=2, vorgaenger__typ_id=1)


class ZielManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(typ_id=3, vorgaenger__typ_id=2)

class MassnahmeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(typ_id=4, vorgaenger__typ_id=3)


class BusinessObject(models.Model):
    typ = models.ForeignKey(Code, on_delete=models.CASCADE)
    vorgaenger = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    kuerzel = models.CharField(max_length=10)
    titel = models.CharField(max_length=200, verbose_name="Titel")
    beschreibung = models.TextField(verbose_name="Beschreibung")
    erstellt_am = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    erstellt_von = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Erstellt von")
    aufwand_personen_tage_plan = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Aufwand Personentage", default=0)
    aufwand_tsd_chf_plan = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Aufwand tsd CHF", default=0)
    jahr_start = models.IntegerField(verbose_name="Jahr Start", default=datetime.now().year)
    jahr_ende = models.IntegerField(verbose_name="Jahr Ende", default=datetime.now().year)
    anmerkung_initialisierung = models.TextField(verbose_name="Pol. Vorstoss", null=True, blank=True)
    messbarkeit = models.CharField(max_length=200, verbose_name="Messbarkeit")  
    bestehende_massnahme = models.CharField(max_length=200, verbose_name="Bestehende Massnahme")
    kontakt_verantwortlich = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="Kontakt verantwortlich")

    objects = models.Manager()
    themen = ThemaManager()
    handlungsfelder = HandlungsfeldManager()
    ziele = ZielManager()
    massnahmen = MassnahmeManager()

    def __str__(self):
        return self.titel


class MassnahmeOrganisation(models.Model):
    massnahme = models.ForeignKey(BusinessObject, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)

    def __str__(self):
        return self.massnahme.titel


class Rolle(BusinessObject):
    objects = RolleManager()

    class Meta:
        proxy = True


class NeuBestehend(BusinessObject):
    objects = NeuBestehendManager()

    class Meta:
        proxy = True




class Handlungsfeld(BusinessObject):
    objects = HandlungsfeldManager()

    class Meta:
        proxy = True


class Ziel(BusinessObject):
    objects = ZielManager()

    class Meta:
        proxy = True


class Massnahme(BusinessObject):
    objects = MassnahmeManager()

    class Meta:
        proxy = True


class Thema(models.Model):
    titel = models.CharField(max_length=200)
    beschreibung = models.TextField()
    kontakt = models.CharField(max_length=200)
    jahr_start = models.IntegerField(verbose_name="Jahr Start", default = datetime.now().year +1)    
    jahr_ende = models.IntegerField(verbose_name="Jahr Ende", default = datetime.now().year + 5)    

    def __str__(self):
        return self.titel


class PlanRecord(models.Model):
    objekt = models.ForeignKey(BusinessObject, on_delete=models.CASCADE,verbose_name="Massnahme")
    #organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, verbose_name="Organisation")
    jahr = models.IntegerField(verbose_name="Jahr", default=datetime.now().year)
    monat = models.IntegerField()
    soll_wert_erreicht_pzt = models.IntegerField(verbose_name="Zielerreichungsgrad (Soll, %)")
    ist_wert_erreicht_pzt = models.IntegerField(verbose_name="Zielerreichungsgrad (Ist, %)")
    aufwand_personen_tage_plan = models.IntegerField(verbose_name='Aufwand Personentage (Soll)')
    aufwand_tsd_chf_plan = models.IntegerField(verbose_name='Aufwand tsd CHF (Soll)')
    aufwand_personen_tage_ist = models.IntegerField(default=0, verbose_name='Aufwand Personentage (Ist)')
    aufwand_tsd_chf_ist = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Aufwand tsd CHF (Ist)')
    beschreibung = models.TextField(verbose_name="Beschreibung",null=True, blank=True)
    
    erstellt_am = models.DateTimeField(auto_now_add=True,verbose_name='Erstellt am')
    erstellt_von = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='Erstellt von')

    def __str__(self):
        return f"{self.objekt.titel} {self.jahr}"

def person_delete(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == "POST":
        person.delete()
        return redirect('personen_list')