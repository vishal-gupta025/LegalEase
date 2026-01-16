from cases.models import CaseSection
from documents.services.text_extractor import TextExtractorService
from documents.services.section_parser import LegalSectionParser


class LegalDocumentProcessor:

    @staticmethod
    def process_document(legal_document):

        extracted_text = TextExtractorService.extract_text(legal_document.file.path)
        legal_document.extracted_text = extracted_text
        legal_document.save()

        parsed_sections = LegalSectionParser.parse_sections(extracted_text)

        for section_type, content in parsed_sections.items():
            if content.strip():
                CaseSection.objects.create(
                    legal_case=legal_document.legal_case,
                    section_type=section_type,
                    content=content
                )
        legal_document.is_processed = True
        legal_document.save()

