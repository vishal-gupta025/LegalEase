from django.contrib import admin
from documents.services.document_processor import LegalDocumentProcessor
from .models import LegalDocument


@admin.register(LegalDocument)
class LegalDocumentAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'legal_case', 'is_processed', 'uploaded_at')
    search_fields = ('original_filename', )
    list_filter = ('is_processed',)
    actions = ['process_selected_documents']

    def process_selected_documents(self, request, queryset):
        for document in queryset:
            if not document.is_processed:
                LegalDocumentProcessor.process_document(document)
        
        self.message_user(request, "Selected documents have been processed.")

    process_selected_documents.short_description = "Process selected legal documents"