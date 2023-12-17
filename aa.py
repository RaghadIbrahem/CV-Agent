import re

import spacy
import en_core_web_sm
from spacy.matcher import Matcher
nlp = en_core_web_sm.load()
matcher = Matcher(nlp.vocab)
def extract_name(resume_text):
    nlp_text = nlp(resume_text)

    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

    matcher.add('NAME', [pattern])

    matches = matcher(nlp_text)

    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text

cvGPA = 'amal'
m = re.sub(r'[/W]', "", cvGPA)
print(m)