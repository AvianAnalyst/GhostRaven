from GhostRaven.content_builder import ContentBuilder
from GhostRaven.ssp_builder import SSPBuilder


# with open('contents/Universal.yaml') as universal_contents, open('templates/mt_checkbox_templates.yaml') as checkboxes:
#     mt_document_contents = ContentBuilder(checkboxes, universal_contents)
# with open('contents/MTOnly.yaml') as environment_contents:
#     mt_document_contents.add_contents(environment_contents)
#
# mt_builder = SSPBuilder('templates/MTFinalSSP_Template.docx', mt_document_contents.contents)
# mt_builder.build_ssp()
# mt_builder.save('output/mt_output.docx')

with open('contents/Universal.yaml') as universal_contents, open('templates/gcch_checkbox_templates.yaml') as checkboxes:
    gcch_document_contents = ContentBuilder(checkboxes, universal_contents)
with open('contents/GCCHOnly.yaml') as environment_contents:
    gcch_document_contents.add_contents(environment_contents)

gcch_builder = SSPBuilder('templates/GCCHFinalSSP_Template.docx', gcch_document_contents.contents)
gcch_builder.build_ssp()
gcch_builder.save('output/gcch_output.docx')

# with open('contents/universal.yaml') as universal_contents, open('templates/dod_checkbox_templates.yaml') as checkboxes:
#     dod_document_contents = ContentBuilder(checkboxes, universal_contents)
# with open('contents/DoD.yaml') as environment_contents:
#     dod_document_contents.add_contents(environment_contents)
# with open('contents/GCCHOnly.yaml') as environment_contents:
#     dod_document_contents.add_contents(environment_contents)
#
# dod_builder = SSPBuilder('templates/DoDFinalSSP_Template.docx', dod_document_contents.contents)
# dod_builder.build_ssp()
# dod_builder.save('output/dod_output.docx')
