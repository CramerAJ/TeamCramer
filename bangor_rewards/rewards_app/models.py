from __future__ import unicode_literals
import math

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum

# Create your models here.
class Charity(models.Model):
	name = models.CharField(max_length=64)
	points = models.IntegerField(default=0)
	description = models.CharField(max_length=360, blank=True, null=True)
	image_url = models.URLField(default="http://google.com")
	website = models.URLField(default="http://google.com")
	latitude = models.FloatField(default=0)
	longitude = models.FloatField(default=0)
	facebook_url = models.URLField(default="")
	twitter_url = models.URLField(default="")

	def pay(self, amt):
		self.points += amt

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "charities"

class Profile(models.Model):
	name = models.CharField(max_length=64)
	current_points = models.IntegerField(default=0)
	total_points = models.IntegerField(default=0)
	image_url = models.URLField(default="http://simpleicon.com/wp-content/uploads/account.png")
	cover_image_url = models.URLField(default="http://blog.entheosweb.com/wp-content/uploads/2012/03/fbs23_byentheosweb.jpg")
	friends = models.ManyToManyField("self",blank=True)
	achievements = models.ManyToManyField("Achievement",blank=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE) # connected to admin user

	def __str__(self):
		return self.name

	@receiver(post_save, sender=User)
	def update_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)
		instance.profile.save()

	def spent(self):
		return self.total_points - self.current_points

	def get_level(self):
		spent = self.total_points - self.current_points
		return int((math.sqrt(spent))/10)

	def get_title(self):
		titleList = ["Benevolent Beginner", "Altruistic Apprentice", "Chief of Charity", "Kingpin of Kindness", "Sovereign of Selflessness", "Potentate of Philanthropy", "Overlord of Offering", "Grandmaster of Giving", "Magnanimous Mogul" ]
		level = self.get_level()
		if level < len(titleList):
			return titleList[level]
		else:
			return titleList[len(titleList-1)]

	def pay(self, amt):
		self.current_points -= amt

	def get_top_three_charities(self):
		usersDonations = Activity.objects.filter(profile__in=[self]).filter(act__in='Donation')
		topThreePointTotals = (usersDonations.values('charity').annotate(s = Sum('points')).order_by('-s'))[:3]             
		topThreeCharities = []
		for x in topThreePointTotals:
			charityID = x['charity']
			topThreeCharities.append(Charity.objects.get(id=charityID))
		return topThreeCharities
        
class Achievement(models.Model):
	name = models.CharField(max_length=64)
	description = models.CharField(max_length=360)

	def __str__(self):
		return self.name


class Activity(models.Model):
	act_types = [
		('D', 'Donation'),
		('E', 'Earning')
	]
	profile = models.ForeignKey("Profile", on_delete=models.CASCADE, null=True)
	charity = models.ForeignKey("Charity", on_delete=models.CASCADE, blank=True, null=True)
	act = models.CharField(max_length=20, choices=act_types)
	points = models.IntegerField(default=0)
	timestamp = models.DateField(auto_now=True)



	def __str__(self):
		if self.charity:
			return "Donated " + str(self.points) + " points to " + self.charity.name
		else:
			return "Earned " + str(self.points) + " points"
