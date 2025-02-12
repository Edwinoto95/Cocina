from django.db import models

class LugarOrigen(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Lugares de Origen"

class Ingrediente(models.Model):
    UNIDADES_MEDIDA = [
        ('g', 'Gramos'),
        ('kg', 'Kilogramos'),
        ('ml', 'Mililitros'),
        ('l', 'Litros'),
        ('unidad', 'Unidad'),
        ('cdta', 'Cucharadita'),
        ('cda', 'Cucharada'),
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    unidad_medida = models.CharField(max_length=10, choices=UNIDADES_MEDIDA)
    
    def __str__(self):
        return self.nombre

class Receta(models.Model):
    DIFICULTAD_CHOICES = [
        ('facil', 'Fácil'),
        ('medio', 'Medio'),
        ('dificil', 'Difícil')
    ]
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tiempo_preparacion = models.IntegerField(help_text="Tiempo en minutos")
    dificultad = models.CharField(max_length=10, choices=DIFICULTAD_CHOICES)
    lugar_origen = models.ForeignKey(LugarOrigen, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='recetas/', blank=True, null=True)
    
    def __str__(self):
        return self.nombre

class RecetaIngrediente(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='ingredientes')
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    notas = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.cantidad} {self.ingrediente.unidad_medida} de {self.ingrediente.nombre}"

class PasoPreparacion(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='pasos')
    numero_paso = models.IntegerField()
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='pasos/', blank=True, null=True)
    
    class Meta:
        ordering = ['numero_paso']
    
    def __str__(self):
        return f"Paso {self.numero_paso} de {self.receta.nombre}"