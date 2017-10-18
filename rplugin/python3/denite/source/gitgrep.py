# -*- coding: utf-8 -*-

from .base import Base
import subprocess


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
        self.kind = 'gitgrep_kind'

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
        return [{'word': word} for word in run_command(args, self.vim.eval('getcwd()'))]
