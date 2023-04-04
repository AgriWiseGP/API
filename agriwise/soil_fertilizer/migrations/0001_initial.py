# Generated by Django 4.0.8 on 2023-03-14 13:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SoilAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Pratio', models.DecimalField(decimal_places=2, max_digits=7)),
                ('Kratio', models.DecimalField(decimal_places=2, max_digits=7)),
                ('Nratio', models.DecimalField(decimal_places=2, max_digits=7)),
                ('PH', models.DecimalField(decimal_places=2, max_digits=7)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherConditions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.DecimalField(decimal_places=2, max_digits=7)),
                ('humidity', models.DecimalField(decimal_places=2, max_digits=7)),
                ('rainfall', models.DecimalField(decimal_places=2, max_digits=7)),
            ],
        ),
        migrations.CreateModel(
            name='SoilFertilizer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crop_name', models.CharField(choices=[('rice', 'rice'), ('Coconut', 'Coconut')], max_length=100)),
                ('soil_name', models.CharField(choices=[('Clayey', 'Clayey'), ('alluvial', 'alluvial'), ('clay loam', 'clay loam'), ('coastal', 'coastal'), ('laterite', 'laterite'), ('sandy', 'sandy'), ('silty clay', 'silty clay')], max_length=100)),
                ('target', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('soil_analysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='soil_fertilizer.soilanalysis')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('weather_conditions', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='soil_fertilizer.weatherconditions')),
            ],
        ),
    ]