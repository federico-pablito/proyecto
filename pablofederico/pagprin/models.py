from django.db import models


class maestroequipos(models.Model):
    id = models.CharField(max_length=50),
    tipo = models.CharField(max_length=50),
    interno = models.CharField(max_length=50),
    patente = models.CharField(max_length=50),
    chasis = models.CharField(max_length=50),
    motor = models.CharField(max_length=50),
    año = models.IntegerField(),
    ubicacion = models.CharField(max_length=50),
    up = models.IntegerField(),
    seguro = models.CharField(max_length=50),
    numero_de_poliza = models.IntegerField(),
   
    
    class Meta: 
        db_table = 'maestroequipos'
        managed = True
        verbose_name = 'ModelName'
        verbose_name_plural = 'ModelNames'
        
        
    
    
    
    
    
    

    
   
    