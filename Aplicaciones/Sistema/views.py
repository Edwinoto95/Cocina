from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.forms import modelformset_factory
from .models import (
    Receta, Ingrediente, LugarOrigen, RecetaIngrediente, PasoPreparacion
)
from .forms import (
    RecetaForm, IngredienteForm, LugarOrigenForm,
    RecetaIngredienteForm, PasoPreparacionForm
)

def inicio(request):
    ultimas_recetas = Receta.objects.all().order_by('-fecha_creacion')[:5]
    lugares_origen = LugarOrigen.objects.all()
    return render(request, 'inicio.html', {
        'ultimas_recetas': ultimas_recetas,
        'lugares_origen': lugares_origen
    })

def lista_recetas(request):
    recetas = Receta.objects.all()
    lugares_origen = LugarOrigen.objects.all()

    dificultad = request.GET.get('dificultad')
    origen = request.GET.get('origen')

    if dificultad:
        recetas = recetas.filter(dificultad=dificultad)
    if origen:
        recetas = recetas.filter(lugar_origen_id=origen)

    return render(request, 'recetas.html', {
        'recetas': recetas,
        'lugares_origen': lugares_origen
    })

def detalle_receta(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    return render(request, 'detalle_receta.html', {'receta': receta})

def crear_receta(request):
    IngredienteFormSet = modelformset_factory(
        RecetaIngrediente,
        form=RecetaIngredienteForm,
        extra=1,
        can_delete=True
    )
    PasoFormSet = modelformset_factory(
        PasoPreparacion,
        form=PasoPreparacionForm,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        form = RecetaForm(request.POST, request.FILES)
        formset_ingredientes = IngredienteFormSet(request.POST, prefix='ingredientes')
        formset_pasos = PasoFormSet(request.POST, request.FILES, prefix='pasos')

        if form.is_valid() and formset_ingredientes.is_valid() and formset_pasos.is_valid():
            receta = form.save()

            for form_ingrediente in formset_ingredientes:
                if form_ingrediente.cleaned_data and not form_ingrediente.cleaned_data.get('DELETE'):
                    ingrediente = form_ingrediente.save(commit=False)
                    ingrediente.receta = receta
                    ingrediente.save()

            for form_paso in formset_pasos:
                if form_paso.cleaned_data and not form_paso.cleaned_data.get('DELETE'):
                    paso = form_paso.save(commit=False)
                    paso.receta = receta
                    paso.save()

            messages.success(request, 'Receta creada exitosamente.')
            return redirect('Sistema:detalle_receta', pk=receta.pk)

    else:
        form = RecetaForm()
        formset_ingredientes = IngredienteFormSet(queryset=RecetaIngrediente.objects.none(), prefix='ingredientes')
        formset_pasos = PasoFormSet(queryset=PasoPreparacion.objects.none(), prefix='pasos')

    return render(request, 'form_receta.html', {
        'form': form,
        'formset_ingredientes': formset_ingredientes,
        'formset_pasos': formset_pasos
    })

def editar_receta(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    IngredienteFormSet = modelformset_factory(
        RecetaIngrediente,
        form=RecetaIngredienteForm,
        extra=1,
        can_delete=True
    )
    PasoFormSet = modelformset_factory(
        PasoPreparacion,
        form=PasoPreparacionForm,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        form = RecetaForm(request.POST, request.FILES, instance=receta)
        formset_ingredientes = IngredienteFormSet(
            request.POST,
            prefix='ingredientes',
            queryset=RecetaIngrediente.objects.filter(receta=receta)
        )
        formset_pasos = PasoFormSet(
            request.POST,
            request.FILES,
            prefix='pasos',
            queryset=PasoPreparacion.objects.filter(receta=receta)
        )

        if form.is_valid() and formset_ingredientes.is_valid() and formset_pasos.is_valid():
            receta = form.save()

            for form_ingrediente in formset_ingredientes:
                if form_ingrediente.cleaned_data:
                    if form_ingrediente.cleaned_data.get('DELETE') and form_ingrediente.instance.pk:
                        form_ingrediente.instance.delete()
                    else:
                        ingrediente = form_ingrediente.save(commit=False)
                        ingrediente.receta = receta
                        ingrediente.save()

            for form_paso in formset_pasos:
                if form_paso.cleaned_data:
                    if form_paso.cleaned_data.get('DELETE') and form_paso.instance.pk:
                        form_paso.instance.delete()
                    else:
                        paso = form_paso.save(commit=False)
                        paso.receta = receta
                        paso.save()

            messages.success(request, 'Receta actualizada exitosamente.')
            return redirect('Sistema:detalle_receta', pk=receta.pk)

    else:
        form = RecetaForm(instance=receta)
        formset_ingredientes = IngredienteFormSet(
            queryset=RecetaIngrediente.objects.filter(receta=receta),
            prefix='ingredientes'
        )
        formset_pasos = PasoFormSet(
            queryset=PasoPreparacion.objects.filter(receta=receta),
            prefix='pasos'
        )

    return render(request, 'form_receta.html', {
        'form': form,
        'formset_ingredientes': formset_ingredientes,
        'formset_pasos': formset_pasos,
        'receta': receta
    })

def eliminar_receta(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    receta.delete()
    messages.success(request, 'Receta eliminada exitosamente.')
    return redirect('Sistema:recetas')

# Views para Ingredientes
def lista_ingredientes(request):
    ingredientes = Ingrediente.objects.all()
    return render(request, 'ingredientes.html', {'ingredientes': ingredientes})

def crear_ingrediente(request):
    if request.method == 'POST':
        form = IngredienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingrediente creado exitosamente.')
            return redirect('Sistema:ingredientes')
    else:
        form = IngredienteForm()
    return render(request, 'form_ingrediente.html', {'form': form})

def editar_ingrediente(request, pk):
    ingrediente = get_object_or_404(Ingrediente, pk=pk)
    if request.method == 'POST':
        form = IngredienteForm(request.POST, instance=ingrediente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingrediente actualizado exitosamente.')
            return redirect('Sistema:ingredientes')
    else:
        form = IngredienteForm(instance=ingrediente)
    return render(request, 'form_ingrediente.html', {
        'form': form,
        'ingrediente': ingrediente
    })

def eliminar_ingrediente(request, pk):
    ingrediente = get_object_or_404(Ingrediente, pk=pk)
    ingrediente.delete()
    messages.success(request, 'Ingrediente eliminado exitosamente.')
    return redirect('Sistema:ingredientes')

# Views para Lugares de Origen
def lista_lugares(request):
    lugares = LugarOrigen.objects.all()
    return render(request, 'lugares.html', {'lugares': lugares})

def crear_lugar(request):
    if request.method == 'POST':
        form = LugarOrigenForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lugar de origen creado exitosamente.')
            return redirect('Sistema:lugares')
    else:
        form = LugarOrigenForm()
    return render(request, 'form_lugar.html', {'form': form})

def editar_lugar(request, pk):
    lugar = get_object_or_404(LugarOrigen, pk=pk)
    if request.method == 'POST':
        form = LugarOrigenForm(request.POST, instance=lugar)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lugar de origen actualizado exitosamente.')
            return redirect('Sistema:lugares')
    else:
        form = LugarOrigenForm(instance=lugar)
    return render(request, 'form_lugar.html', {
        'form': form,
        'lugar': lugar
    })

def eliminar_lugar(request, pk):
    lugar = get_object_or_404(LugarOrigen, pk=pk)
    lugar.delete()
    messages.success(request, 'Lugar de origen eliminado exitosamente.')
    return redirect('Sistema:lugares')

def recetas_por_dificultad(request, dificultad):
    recetas = Receta.objects.filter(dificultad=dificultad)
    return render(request, 'recetas.html', {
        'recetas': recetas,
        'dificultad_seleccionada': dificultad
    })

def recetas_por_origen(request, origen_id):
    lugar = get_object_or_404(LugarOrigen, pk=origen_id)
    recetas = Receta.objects.filter(lugar_origen=lugar)
    return render(request, 'recetas.html', {
        'recetas': recetas,
        'lugar_seleccionado': lugar
    })
