import re
from typing import Dict

class LegalSectionParser:

    SECTION_PATTERNS = {
        'FACTS': [
            r'facts of the case',
            r'background of the case',
            r'breif facts'
        ],
        'ISSUEs': [
            r'issues for consideration',
            r'points for determination',
            r'issues involved'
        ],
        'ARGUMENTS': [
            r'arguments',
            r'contentions',
            r'submissions'
        ],
        'JUDGMENT': [
            r'judgment',
            r'final decision',
            r'order'
        ],
        'REASONING': [
            r'reasoning',
            r'analysis',
            r'discussion'
        ],
    }

    @classmethod
    def parse_sections(cls, text: str)-> Dict[str, str]:
        sections = {
            'FACTS': '',
            'ISSUES': '',
            'ARGUMENTS': '',
            'JUDGMENT': '',
            'REASONING': ''
        }

        lower_text = text.lower()

        indices = {} 

        for section, patterns in cls.SECTION_PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, lower_text)
                if match:
                    indices[section] = match.start()
                    break

        sorted_sections = sorted(indices.items(), key=lambda x: x[1])

        for i, (section, start_idx) in enumerate(sorted_sections):
            end_idx = None
            if i + 1 < len(sorted_sections):
                end_idx = sorted_sections[i + 1][1]

            section_text = text[start_idx:end_idx].strip()
            sections[section] = section_text

        return sections