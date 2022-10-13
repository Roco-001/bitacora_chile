from django.db import models
from datetime import datetime, timedelta
from django.utils import  timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError


# Create your models here.
ESTADO = (
        ('En Curso', 'En Curso'),
        ('Observación', 'Observación'),
        ('Resuelto', 'Resuelto'),
        ('Pendiente', 'Pendiente')
    )

MSR = (
        ('AM', 'AM'),
        ('BAF', 'BAF'),
        ('CL/EX', 'CL/EX'),
        ('CS', 'CS'),
        ('CX', 'CX'),
        ('DX', 'DX'),
        ('TX', 'TX')
    )

NOT = (
        ('MCO', 'MCO'),
        ('SUBTEL', 'SUBTEL'),
        ('DS60-SUBTEL', 'DS60-SUBTEL'),
        ('CLTS_VIP', 'CLTS_VIP'),

    )

REGION = (
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('IV', 'IV'),
        ('V', 'V'),
        ('VI', 'VI'),
        ('VII', 'VII'),
        ('VIII', 'VIII'),
        ('IX', 'IX'),
        ('X', 'X'),
        ('XI', 'XI'),
        ('XII', 'XII'),
        ('XIII', 'XIII'),
        ('XIV', 'XIV'),
        ('XV', 'XV'),
        ('XVI', 'XVI'),

    )
hoy = datetime.now().strftime("%d%m%Y")
now = timezone.now


class Elemento(models.Model):
    nombre = models.CharField(max_length=250, verbose_name="Elemento", blank=True, null=True)
    description =models.TextField(verbose_name="Descripción", blank=True, null=True)
    nemonico = models.CharField(max_length=250, verbose_name="Nemónico", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        unique_together = ('nombre',)
        verbose_name = "Elemento"
        verbose_name_plural = "Elementos"
        # Ordena de mas nuevo a mas antiguo
        ordering = ["-created"]

    def __str__(self):
        return self.nombre



class Incidencia(models.Model):
    folio = models.CharField(max_length=250, verbose_name="Folio", blank=True, null=True )
    estado = models.CharField(choices=ESTADO, max_length=45, verbose_name="Estado", blank=True, null=True,
                               default='En Curso')
    msr = models.CharField(choices=MSR, max_length=45, verbose_name="MSR", blank=True, null=True)
    noti = models.CharField(choices=NOT, max_length=45, verbose_name="NOT", blank=True, null=True)
    description = RichTextUploadingField(verbose_name='Descripción', blank=True, null=True)
    nemonico = models.CharField(max_length=250, verbose_name="Nemónico", blank=True, null=True)
    region = models.CharField(choices=REGION, max_length=45, verbose_name="Región", blank=True, null=True)
    elemento = models.ManyToManyField(Elemento, related_name="get_elementos", verbose_name="Elemento", blank=True)

    inicio_afectacion = models.DateTimeField(verbose_name="Inicio de Afectación", default=now)
    duration = models.DurationField(verbose_name="Duración", default=timedelta())
    ultima_actualizacion = models.DateTimeField(verbose_name="Última Actualización", blank=True, null=True)
    proxima_actualizacion = models.DateTimeField(verbose_name="Próxima Actualización", blank=True, null=True)
    calendarizacion = models.DateTimeField(verbose_name="Calendarización", blank=True, null=True)

    tiempo_excedido = models.DurationField(verbose_name="Tiempo Excedido", default=timedelta())
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")


    #def get_absolute_url(self):
    #    return reverse('blog:post_detail',
    #                   args=[self.id,])

    class Meta:
        unique_together = ('folio',)
        verbose_name = "Incidencia"
        verbose_name_plural = "Incidencias"
        # Ordena de mas nuevo a mas antiguo
        ordering = ["-created"]

    def __str__(self):
        return self.folio

    def save(self, *args, **kwargs):
        ahora =  timezone.now()

        self.duration = ahora - self.inicio_afectacion
        if self.proxima_actualizacion:
            self.tiempo_excedido = ahora - self.proxima_actualizacion

        else:
            self.proxima_actualizacion = self.inicio_afectacion + timedelta(hours=1, minutes=45)



        if self.ultima_actualizacion:
            self.proxima_actualizacion = self.ultima_actualizacion + timedelta(hours=1, minutes=45)

        if self.calendarizacion:
            self.proxima_actualizacion = self.calendarizacion - timedelta(minutes=15)


        super().save(*args, **kwargs)

class IncideciaHijo(models.Model):
    folio = models.CharField(max_length=250, verbose_name="Folio", blank=True, null=True)
    estado = models.CharField(choices=ESTADO, max_length=45, verbose_name="Estado", blank=True, null=True,
                               default='En Curso')
    padre = models.ForeignKey(Incidencia, on_delete=models.CASCADE, related_name="get_incidencia_padres",
                                   blank=True, null=True)
    msr = models.CharField(choices=MSR, max_length=45, verbose_name="MSR", blank=True, null=True)
    description =RichTextUploadingField(verbose_name='Descripción', blank=True, null=True)
    nemonico = models.CharField(max_length=250, verbose_name="Nemónico", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")


    #def get_absolute_url(self):
    #    return reverse('blog:post_detail',
    #                   args=[self.id,])

    class Meta:
        unique_together = ('folio',)
        verbose_name = "Incidencia Hijo"
        verbose_name_plural = "Incidencias Hijos"
        # Ordena de mas nuevo a mas antiguo
        ordering = ["-created"]

    def __str__(self):
        return self.folio