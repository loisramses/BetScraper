import re

selection_standardization = {
    'more': 'Mais de ',
    'less': 'Menos de '
}

general_standardization = {
    'to_delete': re.compile(r'\b(fc|sk|club|ac|csc|csm|cs|fk|cp|cd|s\.c\.|sc|sl|sad|sfc|cf|afc| : oaf|as|ssv|sv|1\.|spvgg|tsv|lb|fcv|kv|kvc|ksv|rfc|kas|ksc|pfc|pofc|nk|hnk|gnk|hk|hc|bm)\s'),
    'float': re.compile(r'([0-9]*[.])?[0-9]+')
}
