from django.db import models

class LegalCase(models.Model):
    title = models.CharField(max_length=255,help_text="Official title of the case")
    case_number = models.CharField(max_length=100, unique=True,help_text="Official case number")
    court = models.CharField(max_length=255,help_text="Court where the case is being heard")
    date_of_judgment = models.DateField(null=True, blank=True,help_text="Date when the judgment was delivered")
    parties_involved = models.TextField(help_text="Details of the parties involved in the case")
    summary = models.TextField(blank=True, null=True, help_text="Brief summary of the case")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.case_number})"
    
class CaseSection(models.Model):
    SECTION_CHOICES = (
        ('FACTS', 'Facts'),
        ('ISSUES', 'Issues'),
        ('ARGUMENTS', 'Arguments'),
        ('JUDGMENT', 'Judgment'),
        ('REASONING', 'Reasoning'),
    )

    legal_case = models.ForeignKey(LegalCase, on_delete=models.CASCADE, related_name='sections')
    section_type = models.CharField(max_length=20, choices=SECTION_CHOICES,help_text="Type of the case section")
    content = models.TextField(help_text="Content of the case section")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.legal_case.title}-{self.section_type}"
    

