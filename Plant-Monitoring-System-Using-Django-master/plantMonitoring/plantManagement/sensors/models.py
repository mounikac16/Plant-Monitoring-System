from __future__ import unicode_literals
from django.db import models

class plantID(models.Model):
	pid = models.IntegerField(primary_key=True)
	read_time = models.DateTimeField(auto_now = True)
	plantName = models.CharField(max_length = 25, null=True)
	latitude = models.FloatField(default = 13.5548)
	longitude = models.FloatField(default = 80.027)

	def __str__(self):
		display = 'Pid ' + str(self.pid) + 'Name ' + str(self.plantName) + ' Lat ' + str(self.latitude) + ' Long ' + str(self.longitude) + '\n'
		return display

class plant(models.Model):
	pid = models.ForeignKey(plantID, on_delete = models.CASCADE)
	soilMoisture = models.FloatField(null=True)
	read_time = models.DateTimeField(auto_now = True)

	def __str__(self):
		display = 'Plantid' + str(self.pid) + 'Soil moisture ' + str(self.soilMoisture) + '%\n'
		return display

class weatherStation(models.Model):
	read_time = models.DateTimeField(auto_now = True)
	temperature = models.FloatField(default=0)
	humidity = models.FloatField(default=0)
	overHeadTank = models.FloatField(default=0)
	rainGauge = models.FloatField(null=True)

	def __str__(self):
		display = 'Temperature ' + str(self.temperature) + 'C ' + 'Humidity' + str(self.humidity) + '% ' + 'Level of overhead tanks water: ' + str(self.overHeadTank) + 'cm ' + 'Level of rain gauge water: ' + str(self.rainGauge) + 'cm\n'
		return display
