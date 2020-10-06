from content_builder import ContentBuilder
from ssp_builder import SSPBuilder


with open('universal.yaml') as f:
    document_contents = ContentBuilder(f)

""" 
If there were a 'dod' on top of gcch, it would be added here. The yaml would look like: 
some_key: "{{dod_key}} And the dod add on here"
"""

with open('gcch.yaml') as f:
    document_contents.add_contents(f)


dod_ssp = SSPBuilder(document_contents.contents)

dod_ssp.build_ssp()

dod_ssp.save()
