# **************************************************************************** #
# Project: https://github.com/k61n/gitlabci-cppformat 
# License: GNU LGPL Version 2.1 (see LICENSE)
# Copyright (C) by the authors:
#     2023 Konstantin Kholostov <kholostov*gmail.com>
# Description: check if clang-tidy warns on the latest pushed changes
# **************************************************************************** #

import os
import subprocess

from clang_format import get_latest_changes


file = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(file))


def parse_clangtidy_output(filename):
    cmd = f'clang-tidy -p {os.path.join(project_root, "build")} {filename}'
    output = subprocess.check_output(cmd, shell=True, text=True)
    errors = []
    for line in output.split('\n'):
        if line:
            if line.startswith('/') and 'warning:' in line:
                errors.append({})
                errors[-1]['line'] = line.split(':')[1]
                errors[-1]['warning'] = line
                errors[-1]['note'] = ''
                errors[-1]['fix'] = ''
            elif line.startswith('/') and 'note:' in line:
                errors.append({})
                errors[-1]['line'] = line.split(':')[1]
                errors[-1]['warning'] = ''
                errors[-1]['note'] = line
                errors[-1]['fix'] = ''
            else:
                errors[-1]['fix'] += line + '\n'
    return errors


class ClangTidyDB:
    def __init__(self):
        self._errors = {}

    def add_filename(self, filename):
        self._errors[filename] = parse_clangtidy_output(filename)

    def check_filename(self, filename, lines_numbers):
        output = []
        for entry in self[filename]:
            if int(entry['line']) in lines_numbers:
                output.append(entry)
        return output

    def __iter__(self):
        return iter(self._errors.items())

    def __getitem__(self, filename):
        return self._errors[filename]


if __name__ == '__main__':
    # exit if there are no cpp or h files
    latest_changes = get_latest_changes()
    if not latest_changes:
        exit(0)

    # dict clang-tidy warnings for the filenames
    warnings = ClangTidyDB()
    for filename in latest_changes.keys():
        print(f'\nClang-tidy on {os.path.join(project_root, filename)}')
        warnings.add_filename(os.path.join(project_root, filename))

    # check for clang-tidy warnings in new lines in filenames
    print('\n\nClang-tidy has detected several warnings. '
          'Please fix these warnings for the pipeline to succeed.\n\n')
    status = 0
    for filename in latest_changes.keys():
        entries = warnings.check_filename(os.path.join(project_root, filename),
                                          latest_changes[filename])
        if entries:
            status = 1
            for entry in entries:
                if entry["warning"]:
                    print(f'Line {entry["line"]}')
                    print(f'{entry["warning"]}')
                    print(f'Fix:\n{entry["fix"]}')
                # if entry["note"]:
                #     print(f'{entry["note"]}')
                #     print(f'{entry["fix"]}')

    exit(status)
