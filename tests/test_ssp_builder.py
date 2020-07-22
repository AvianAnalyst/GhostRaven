import pytest


# TODO: add support for checking new lines characters?
# test 1 combines strings:
def test_combines_universal_and_env_specific_strings():
    universal = 'universal: "this is universal.{{env_specific}}"'
    env = 'env_specific: " this is environment specific"'
    correct = {
        'universal': "this is universal. this is environment specific"
    }


# test 2 combines lists:
def test_combines_universal_and_env_list_strings():
    universal = 'universal:\n' \
                '   - "universal 1"\n' \
                '   - "universal 2"'
    env = 'env:\n' \
          '   - "env 1"'
    correct = {
        'universal': ['universal 1', 'universal 2', 'env 1']
    }
    pass


# test 3 writing to document provides correct strings
def test_after_writing_strings_are_correct():
    pass


# test 4 writing to document provides correct check boxes for status
def test_after_writing_status_checkboxes_are_correct():
    pass

# test 5 writing to document provides  correct check box for -1 (uninheritable) controls
def test_after_writing_uninheritable_origination_checkboxes_are_correct():
    pass

# test 6 writing to document provides correct check boxes for inheritable controls
def test_after_writing_inheritable_origination_checkboxes_are_correct():
    pass
