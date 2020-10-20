from content_builder import ContentBuilder
from ssp_builder import SSPBuilder


with open('contents/universal.yaml') as f:
    mt_document_contents = ContentBuilder(f)
with open('contents/mt.yaml') as f:
    mt_document_contents.add_contents(f)


with open('contents/universal.yaml') as f:
    gcch_document_contents = ContentBuilder(f)
with open('contents/gcch.yaml') as f:
    gcch_document_contents.add_contents(f)


with open('contents/universal.yaml') as f:
    dod_document_contents = ContentBuilder(f)
with open('contents/addendum.yaml') as f:
    dod_document_contents.add_contents(f)
with open('contents/gcch.yaml') as f:
    dod_document_contents.add_contents(f)

mt_builder = SSPBuilder('mt', mt_document_contents.contents)
gcch_builder = SSPBuilder('gcch', gcch_document_contents.contents)
dod_builder = SSPBuilder('dod', dod_document_contents.contents)


mt_builder.build_ssp()
gcch_builder.build_ssp()
dod_builder.build_ssp()

mt_builder.save('output/mt_output.docx')
gcch_builder.save('output/gcch_output.docx')
dod_builder.save('output/dod_output.docx')
