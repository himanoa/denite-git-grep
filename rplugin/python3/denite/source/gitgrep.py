# -*- coding: utf-8 -*-

from .base import Base
import subprocess
import re


def run_command(command, cwd, encode='utf8'):
    process = subprocess.run(command,
                             cwd=cwd,
                             stdout=subprocess.PIPE)

    return process.stdout.decode(encode).split('\n')


class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)
        self.vim = vim
        self.name = 'git-grep'
        self.kind = 'file'

    def on_init(self, context):
        pass

    def on_close(self, context):
        pass

    def gather_candidates(self, context):
        # command: git --no-pager grep -n --no-color
        args = [x for x in ['git',
                            '--no-pager',
                            'grep',
                            '-n',
                            '--no-color',
                            ' '.join(context['args'][1::]),
                            '--',
                            context['args'][0]] if len(x) != 0]
        return [self.__candidate(x) for x in run_command(args, self.vim.eval('getcwd()')) if self.__candidate(x) is not None]

    def __candidate(self, line):
        try:
            regex = re.compile("\:\d+\:")
            path = regex.split(line)[0]
            body = ''.join(line.split(':')[2::])
            row = regex.search(line)[0].strip(':')

            return {
                'word': line,
                "abbr": '{0}:{1}: {2}'.format(
                    path,
                    row,
                    body
                ),
                'action__path': path,
                'action__line': int(row),
                'action__col': 0,
                'action__text': body
            }
        except TypeError:
            return None
