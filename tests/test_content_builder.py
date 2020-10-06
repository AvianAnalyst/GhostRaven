# TODO: add support for checking new lines characters?
# TODO: fix tests to test what they're supposed to, no more no less, includes test specific input files

from content_builder import ContentBuilder


# test 1 combines parent and child strings:
def test_combines_universal_and_env_specific_strings():
    expected = 'this is universal. this is environment specific'

    with open('/mnt/c/Users/v-kybyrd/PycharmProjects/SSP_proof_of_concept/tests/parent.yaml', 'r') as f:
        content = ContentBuilder(f)

    with open('/mnt/c/Users/v-kybyrd/PycharmProjects/SSP_proof_of_concept/tests/child.yaml', 'r') as f:
        content.add_contents(f)

    assert content.contents['basic_string_replacement'] == expected


# test 2 combines parent and child strings with addendum:
def test_combines_universal_and_env_specific_strings_with_addendum():
    expected = 'this is universal. this is environment specific\n' \
               'here is an addendum paragraph'

    with open('parent.yaml', 'r') as f:
        content = ContentBuilder(f)

    with open('addendum.yaml', 'r') as f:
        content.add_contents(f)

    with open('child.yaml', 'r') as f:
        content.add_contents(f)

    assert content.contents['basic_string_replacement'] == expected

# test 3 combines lists:
def test_fills_implementation_status_string_correctly():
    expected = 'Implementation Status (check all that apply):\n' \
                      '☒ Implemented\n' \
                      '☐ Partially implemented\n' \
                      '☐ Planned\n' \
                      '☐ Alternative implementation\n' \
                      '☐ Not applicable'
    with open('parent.yaml', 'r') as f:
        contents = ContentBuilder(f)

    with open('child.yaml', 'r') as f:
        contents.add_contents(f)

    assert contents.contents['implemented_status_string'] == expected

def test_fills_multiple_selection_implementation_status_strings_correctly():
    expected = 'Implementation Status (check all that apply):\n' \
               '☒ Implemented\n' \
               '☐ Partially implemented\n' \
               '☐ Planned\n' \
               '☒ Alternative implementation\n' \
               '☐ Not applicable'
    with open('parent.yaml', 'r') as f:
        contents = ContentBuilder(f)

    with open('child.yaml', 'r') as f:
        contents.add_contents(f)

    assert contents.contents['implemented_alt_status_string'] == expected

