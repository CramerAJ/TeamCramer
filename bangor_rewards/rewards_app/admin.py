from django.contrib import admin
from rewards_app.models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.

from .models import Charity
from .models import Profile
from .models import Achievement
from .models import Activity

# documentation on profile/admin user hookup: https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model
# Define an inline admin descriptor for Profile model which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
	model = Profile
	can_delete = False
	filter_horizontal = ('friends',)
# Define a new User admin
class UserAdmin(BaseUserAdmin):
	inlines = (ProfileInline, )
	def get_inline_instances(self, request, obj=None):
		if not obj:
			return list()
		return super(UserAdmin, self).get_inline_instances(request, obj)
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

#add other models to admin page
admin.site.register(Charity)
admin.site.register(Profile) # may not be necessary with useradmin
admin.site.register(Achievement)
admin.site.register(Activity)

