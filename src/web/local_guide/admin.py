from django.contrib import admin
from .models import LocalGuide, Language, Certification, LocalGuideLanguage, LocalGuideCertification

admin.site.register(LocalGuide)
admin.site.register(Language)
admin.site.register(Certification)
admin.site.register(LocalGuideLanguage)
admin.site.register(LocalGuideCertification)