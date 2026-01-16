from django.db import models
from cases.models import LegalCase

class LegalDocument(models.Model):
    legal_case = models.ForeignKey(LegalCase, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='legal_documents/',help_text="Uploaded legal document file")
    original_filename = models.CharField(max_length=255,help_text="Original name of the uploaded file")
    extracted_text = models.TextField(blank=True, null=True,help_text="Text extracted from the document for analysis")
    is_processed = models.BooleanField(default=False,help_text="Whether text extraction is completed")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_filename} - {self.legal_case.title}"
    
    
