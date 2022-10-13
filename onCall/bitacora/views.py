import csv
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.db.models import Q
from .models import Incidencia, IncideciaHijo, Elemento
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from .forms import IncidenciaForm, ElementoForm, IncidenciaHijoForm
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
# Create your views here.

def bitacora(request):
    return render(request, "bitacora/bitacora.html")


class IncidenciaListView(ListView):
    model = Incidencia
    paginate_by = 6
    template_name = "bitacora/bitacora_list.html"


    """ 
    def get_context_data(self, **kwargs):
        object_list = Incidencia.objects.exclude(estado = "Resuelto")
        context = super(IncidenciaListView, self).get_context_data(object_list=object_list, **kwargs)
        queryset = self.request.GET.get('bucar')

        if queryset:
            object_list = Incidencia.objects.filter(Q(elemento__name__icontains=queryset)).distinct()
            print(object_list)
            context = super(IncidenciaListView, self).get_context_data(object_list=object_list, buscar=True, **kwargs)
        return context
    """


class IncidenciaCreate(CreateView):
    model = Incidencia
    #fields = ['folio']
    success_url = reverse_lazy('bitacora:incidencia_list')
    form_class = IncidenciaForm
    template_name = "bitacora/bitacora_form.html"
    second_form_class = ElementoForm

    def get_context_data(self, **kwargs):
        context = super(IncidenciaCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)

        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)

        return context

    def get_success_url(self):
        return reverse('bitacora:incidencia_create')

    def get_no_success_url(self):
        return render(request, "grtc_incidencia/incidencia_tablero.html", contexto)

    def get_success_url2(self):
        return reverse('bitacora:incidencia_list')

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)

        if form2.is_valid() and form.is_valid():
            form2.save(commit=False)
            form.save()
            return HttpResponseRedirect(self.get_success_url2())

        elif form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url2())


        elif form2.is_valid() and not form.is_valid():
            return HttpResponseRedirect(self.get_no_success_url())

        elif form2.is_valid():
            if form2.cleaned_data.get("name"):
                form2.save()
            else:
                form2.save(commit=False)
            return HttpResponseRedirect(self.get_success_url())







class IncidenciaUpdate(UpdateView):
    model = Incidencia
    #fields = ['remedy','afectacion','bitacora']
    template_name = "bitacora/bitacora_update_form.html"
    success_url = reverse_lazy('bitacora:incidencia_list')
    form_class = IncidenciaForm


#BORRAR LA BITACORA
class IncidenciaDelete(DeleteView):
    model = Incidencia
    form_class = IncidenciaForm
    template_name = "bitacora/bitacora_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy('bitacora:incidencia_list')


class IncidenciaHijoCreate(FormMixin, DetailView):
    model = Incidencia
    form_class = IncidenciaHijoForm
    template_name = "bitacora/incidencia_hijo_form.html"


    def get_success_url(self):
        return reverse('bitacora:incidencia_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(IncidenciaHijoCreate, self).get_context_data(**kwargs)
        context['form'] = IncidenciaHijoForm(initial={'padre': self.object})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form)
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(IncidenciaHijoCreate, self).form_valid(form)


class IncidenciahijoUpdate(UpdateView):
    model = IncideciaHijo
    #fields = ['remedy','afectacion','bitacora']
    template_name = "bitacora/incidenciaHijo_update_form.html"
    success_url = reverse_lazy('bitacora:incidencia_list')
    form_class = IncidenciaHijoForm
    #fields = ['folio','estado','msr','noti','description','nemonico','region','inicio_afectacion','ultima_actualizacion','proxima_actualizacion','calendarizacion', 'elemento']




#BORRAR LA BITACORA
class IncidenciaHijoDelete(DeleteView):
    model = IncideciaHijo
    form_class = IncidenciaHijoForm
    template_name = "bitacora/incidenciaHijo_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy('bitacora:incidencia_list')


class IncidenciaHijoDetailView(DetailView):
    model = IncideciaHijo
    template_name = "bitacora/incidenciaHijo_detail.html"



def export_csv(request):
    queryset = Incidencia.objects.exclude(estado = "Resuelto")

    #contruimos la respuesta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=incidencias_activas.csv'

    #Writer
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    # La cabecera o los nombres de las columnas
    writer.writerow(['Folio', 'Estado', 'MSR', 'NOT', 'Descripción', 'Nemónico', 'Región', 'Elemento', 'Inicio' , 'Duración', 'Última Actualización',	'Próxima Actualización'	,'Calendarización' , 'Tiempo Excedido',
 'Hijos'])

    for obj in queryset:
        elemento= []
        hijo = []
        elementos = Elemento.objects.filter(get_elementos=obj.id)
        hijos = IncideciaHijo.objects.filter(padre_id=obj.id)
        if len(elementos) !=0:
            for x in elementos:
                elemento.append(x.nombre)
        else:
            elemento.append('Sin elementos')

        elemento_str = ", ".join(elemento)

        if len(hijos) != 0:
            for x in hijos:
                estado = f'{x.folio} y el estado es {x.estado}'
                hijo.append(estado)

        else:
            hijo.append('Sin Hijos')
        hijo_str = ", ".join(hijo)
        hijo_str = f'Los folios hijos son: {hijo_str}'

        writer.writerow([obj.folio, obj.estado, obj.msr, obj.noti,obj.description, obj.nemonico,obj.region, elemento_str ,obj.inicio_afectacion, obj.duration,obj.ultima_actualizacion, obj.proxima_actualizacion, obj.calendarizacion,obj.tiempo_excedido, hijo_str ])

    return response




def create_bitacora(request):
    form = IncidenciaForm
    form2 = ElementoForm
    template_name = "bitacora/bitacora_form.html"
    context ={}

    if request.method == "POST":
        form = form(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('bitacora:incidencia_create') + '?ok')


    if request.GET.get('nombre') and request.GET.get('description') and request.GET.get('nemonico'):
        form2 = form2(data = request.GET)
        if form2.is_valid():
            form2.save()
            return redirect(reverse('bitacora:incidencia_create'))

    context = {
        'form': form,
        'form2': form2,
    }

    return render(request, template_name, context)







class IncidenciaCerradasListView(ListView):
    model = Incidencia
    paginate_by = 5
    template_name = "bitacora/bitacora_list_cerradas.html"

    def get_queryset(self):
        object_list = Incidencia.objects.filter(estado = "Resuelto")
        queryset = self.request.GET.get('buscar')
        if queryset:
            print('Pasa por aca')
            object_list = Incidencia.objects.filter(
                #Q(folio__icontains=queryset) |
                #Q(estado__icontains=queryset) |
                #Q(msr__icontains=queryset) |
                #Q(noti__icontains=queryset) |
                #Q(nemonico__cliente__name__icontains=queryset) |
                Q(elemento__name=queryset) |
                Q(tkt__icontains=queryset)
            ).distinct().exclude(estado = "Resuelto")
        return object_list


def export_csv_cerradas(request):
    queryset = Incidencia.objects.filter(estado = "Resuelto")

    #contruimos la respuesta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=incidencias_cerradas.csv'

    #Writer
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    # La cabecera o los nombres de las columnas
    writer.writerow(['Folio', 'Estado', 'MSR', 'NOT', 'Descripción', 'Nemónico', 'Región', 'Elemento', 'Inicio' , 'Duración', 'Última Actualización',	'Próxima Actualización'	,'Calendarización' , 'Tiempo Excedido',
 'Hijos'])

    for obj in queryset:
        elemento= []
        hijo = []
        elementos = Elemento.objects.filter(get_elementos=obj.id)
        hijos = IncideciaHijo.objects.filter(padre_id=obj.id)
        if len(elementos) !=0:
            for x in elementos:
                elemento.append(x.nombre)
        else:
            elemento.append('Sin elementos')

        elemento_str = ", ".join(elemento)

        if len(hijos) != 0:
            for x in hijos:
                hijo.append(x.folio)

        else:
            hijo.append('Sin Hijos')
        hijo_str = ", ".join(hijo)
        hijo_str = f'Los folios hijos son: {hijo_str}'

        writer.writerow([obj.folio, obj.estado, obj.msr, obj.noti,obj.description, obj.nemonico,obj.region, elemento_str ,obj.inicio_afectacion, obj.duration,obj.ultima_actualizacion, obj.proxima_actualizacion, obj.calendarizacion,obj.tiempo_excedido, hijo_str ])

    return response