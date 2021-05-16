from django.contrib import admin

from cars.models import Brand, Model_auth, Car, ExtraTableForPrice

admin.site.register(Brand)
admin.site.register(Model_auth)
admin.site.register(Car)
admin.site.register(ExtraTableForPrice)
