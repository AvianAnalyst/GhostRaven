# todo: write library to generate checkbox xml
# todo: write argparse to run from commandline with flags
import re
from collections import defaultdict
from logging import warn, warning
from typing import Tuple

import docx
import yaml


class SSPBuilder:
    def __init__(self, env = None):
        while not env:
            env = input('What environment?')

        with open('contents/universal.yaml') as f:
            self.universal_contents = yaml.full_load(f)
        with open('contents/' + env + '.yaml') as f:
            self.env_contents = yaml.full_load(f)

        self.contents = {
            content_name: re.sub(r'{{(.*?)}}', lambda match: self._replace_text(match, self.env_contents), content_text)
            for content_name, content_text in self.universal_contents.items()
        }
        self.contents['ac_1_status'] = self.contents['ac_1_status'].split(', ')

        self.template = docx.Document('template.docx')

        self.undefined_keys = defaultdict(lambda: 0)

    def _replace_text(self, match, content):
        try:
            return content[match.group(0).strip('{}')]
        except KeyError:
            self.undefined_keys[match.group(0).strip('{}')] += 1
            return '' # hides mistakes made

    def build_ssp(self):
        for table in self.template.tables:
            for row in table.rows:
                for cell in row.cells:
                    cell.text = re.sub(r'{{(.+?)}}', lambda match: self._replace_text(match, self.contents), cell.text)

    def save(self, output_name = 'output/working_output.docx'):
        self.template.save(output_name)
        if self.undefined_keys:
            with open('output/error_log.txt', 'w') as f:
                log = 'The following keys were referenced in the template, or yaml file, but were not defined in any yaml file:\n'
                log += '\n'.join([str(key).strip('()') for key in zip(self.undefined_keys.keys(), self.undefined_keys.values())])
                f.write(log)
            warning("There were some keys referenced that weren't defined. Please view output/error_log.txt for more information.")



gcc_builder = SSPBuilder('gcc')
dod_builder = SSPBuilder('dod')

gcc_builder.build_ssp()
dod_builder.build_ssp()

print(gcc_builder.contents)
print(dod_builder.contents)

gcc_builder.save('output/gcc_output.docx')
dod_builder.save('output/dod_output.docx')
