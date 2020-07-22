# TODO: factor out yaml interpreter class
# TODO: write tests
# TODO: convert yaml to lists
# todo: write argparse to run from commandline with flags
import re
import docx
import yaml
from collections import defaultdict
from logging import warning

CHECKED_BOX = '☒'
UNCHECKED_BOX = '☐'
STATUS_TEMPLATE = 'Implementation Status (check all that apply):\n' \
                  '{{implemented}} Implemented\n' \
                  '{{partial}} Partially implemented\n' \
                  '{{planned}} Planned\n' \
                  '{{alt}} Alternative implementation\n' \
                  '{{na}} Not applicable'
UNINHERITABLE_STATUS_TEMPLATE = 'Control Origination(check all that apply):\n' \
                                     '{{corp}} Service Provider Corporate\n' \
                                     '{{sys}} Service Provider System Specific\n' \
                                     '{{hybrid}} Service Provider Hybrid (Corporate and System Specific)'
INHERITABLE_STATUS_TEMPLATE = f'{UNINHERITABLE_STATUS_TEMPLATE}\n' \
                                   f'{{cust_configured}} Configured by Customer (Customer System Specific)\n' \
                                   f'{{cust_provided}} Provided by Customer (Customer System Specific)\n' \
                                   f'{{shared}} Shared (Service Provider and Customer Responsibility)\n' \
                                   f'{{inherited}} from pre-existing FedRAMP Authorization for {{auth}}, {{date}}'


class SSPBuilder:

    def __init__(self, env = None):
        while not env:
            env = input('What environment?\n')

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
        key = match.group(0).strip('{}')
        try:
            if 'status!' in key:
                key = key[7:]
                return self.build_status_string(self.contents[key], SSPBuilder.status_template)
            elif 'origination!' in key:
                key = key[12:]
                if '+!' in key:
                    key = key[2:]
                    return self.build_status_string(self.contents[key], SSPBuilder.inheritable_origination_template)
                else:
                    return self.build_status_string(self.contents[key], SSPBuilder.uninheritable_origination_template)

            else:
                return content[key]

        except KeyError:
            self.undefined_keys[key] += 1
            warning(key)
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

    def build_status_string(self, true_options, template):
        options = defaultdict(lambda: SSPBuilder.unchecked_box)
        for option in true_options:
            options[option] = SSPBuilder.checked_box

        finished_cell_contents = re.sub(r'{{(.+?)}}', lambda m: self._replace_text(m, options), template)
        return finished_cell_contents




gcc_builder = SSPBuilder('gcc')
dod_builder = SSPBuilder('dod')

gcc_builder.build_ssp()
dod_builder.build_ssp()

gcc_builder.save('output/gcc_output.docx')
dod_builder.save('output/dod_output.docx')
