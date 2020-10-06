import re
import typing
from collections import defaultdict
from logging import warning

import yaml

CHECKED_BOX = '☒'

UNCHECKED_BOX = '☐'

IMPLEMENTATION_STATUS_TEMPLATE = 'Implementation Status (check all that apply):\n' \
                  '{{implemented}} Implemented\n' \
                  '{{partial}} Partially implemented\n' \
                  '{{planned}} Planned\n' \
                  '{{alt}} Alternative implementation\n' \
                  '{{na}} Not applicable'

UNINHERITABLE_ORIGINATION_TEMPLATE = 'Control Origination(check all that apply):\n' \
                                '{{corp}} Service Provider Corporate\n' \
                                '{{sys}} Service Provider System Specific\n' \
                                '{{hybrid}} Service Provider Hybrid (Corporate and System Specific)'

INHERITABLE_ORIGINATION_TEMPLATE = f'{UNINHERITABLE_ORIGINATION_TEMPLATE}\n' \
                              f'{{cust_configured}} Configured by Customer (Customer System Specific)\n' \
                              f'{{cust_provided}} Provided by Customer (Customer System Specific)\n' \
                              f'{{shared}} Shared (Service Provider and Customer Responsibility)\n' \
                              f'{{inherited}} from pre-existing FedRAMP Authorization for {{auth}}, {{date}}'

CHECKBOX_TEMPLATES = {
    'implementation': IMPLEMENTATION_STATUS_TEMPLATE,
    'uninheritable_origination': UNINHERITABLE_ORIGINATION_TEMPLATE,
    'inheritable_origination': INHERITABLE_ORIGINATION_TEMPLATE,
}


class ContentBuilder:
    """
    Class to interpolate yaml files building a dict of complete contents for a specific environment
    """
    def __init__(self, universal_file: typing.TextIO) -> None:
        """
        Takes an opened file to use as the base universal contents across environments
        :param universal_file: opened file-like object pointing to yaml collection of universal content
        """
        self.contents = yaml.safe_load(universal_file)
        self.undefined_keys = defaultdict(lambda: 0)

    def add_contents(self, env_file: typing.TextIO) -> None:
        """
        Takes an opened file to fill out the universal contents. Order of contents being brought in should be:
        1) universal contents (supplied in constructor)
        2) addendum contents (if necessary)
        3) environment specific contents
        :param env_file: opened file-like object pointing to yaml collection of environment specific contents
        """
        env_contents = yaml.safe_load(env_file)
        for k, v in self.contents.items():
            try:
                self.contents[k] = re.sub(r'{{(.+?)}}', lambda match: self._combine_strings(match, env_contents), v)
            except TypeError:
                # TODO: use dict as switch statement after parsing key prefix from template to find what checkbox template to use
                template = v[0]
                # template = 'implementation'
                self.build_checkbox_string(env_contents[v[1]], CHECKBOX_TEMPLATES[template], k)

    def _combine_strings(self, match, content: dict):
        """
        Helper function to perform interpolation
        :param match: passed in automatically by `re.sub`
        :param content:
        :return:
        """
        key = match.group(0).strip('}{')
        print(f'replacing {key} with {content[key]=}')
        try:
            return content[key]
        except KeyError:
            self.undefined_keys[key] += 1
            warning(key)
            return '' # hides mistakes made


    def build_checkbox_string(self, true_options, template, key):
        options = defaultdict(lambda: UNCHECKED_BOX)
        for option in true_options:
            options[option] = CHECKED_BOX

        finished_cell_contents = re.sub(r'{{(.+?)}}', lambda m: self._combine_strings(m, options), template)
        self.contents[key] = finished_cell_contents


# if __main__ == "__main__":
#     with open('tests/parent.yaml') as f:
#         test = ContentBuilder(f)
#
#     with open('tests/child.yaml') as f:
#         test.add_contents(f)