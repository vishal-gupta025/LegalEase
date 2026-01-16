from django.contrib import admin
from .models import LegalCase, CaseSection

@admin.register(LegalCase)
class LegalCaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'case_number', 'court', 'date_of_judgment', 'created_at')
    search_fields = ('title', 'case_number', 'court')
   

@admin.register(CaseSection)
class CaseSectionAdmin(admin.ModelAdmin):
    list_display = ('legal_case', 'section_type', 'created_at')
    list_filter = ('section_type',)
