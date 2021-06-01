import re
import typing
from collections import defaultdict
from logging import warning

import yaml

CHECKED_BOX = '☒'

UNCHECKED_BOX = '☐'


class ContentBuilder:
    """
    Class to interpolate yaml files building a dict of complete contents for a specific environment
    """
    def __init__(self, checkbox_template_file: typing.TextIO, universal_file: typing.TextIO) -> None:
        """
        Takes an opened file to use as the base universal contents across environments
        :param universal_file: opened file-like object pointing to yaml collection of universal content
        """
        self.CHECKBOX_TEMPLATES = yaml.safe_load(checkbox_template_file)
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
        env_contents = {k: v.strip() if type(v) == str else v for k, v in env_contents.items()}
        for k, v in self.contents.items():
            try:
                self.contents[k] = re.sub(r'{{(.+?)}}', lambda match: self._combine_strings(match, env_contents), v)
            except TypeError:
                template = k.split('_')[-1]
                all_true_options = v
                if child_true_options := env_contents.get(k):
                    all_true_options = child_true_options + v
                try:
                    self.build_checkbox_string(all_true_options, self.CHECKBOX_TEMPLATES[template], k)
                except KeyError:
                    raise KeyError(f"tried to access the {template} checkbox template. {env_file=}, and {k=}: {v=}")

    def _combine_strings(self, match, content: dict):
        """
        Helper function to perform interpolation
        :param match: passed in automatically by `re.sub`
        :param content:
        :return:
        """
        key = match.group(0).strip('}{')
        try:
            print(f'replacing {key} with {content[key]=}')
            return content[key]
        except KeyError:
            self.undefined_keys[key] += 1
            # warning(key)
            raise KeyError(f"fix {key=}.")
            return '' # hides mistakes made


    def build_checkbox_string(self, true_options, template, key):
        options = defaultdict(lambda: UNCHECKED_BOX)
        for option in true_options:
            options[option] = CHECKED_BOX

        finished_cell_contents = re.sub(r'{{(.+?)}}', lambda m: self._combine_strings(m, options), template)
        self.contents[key] = finished_cell_contents
