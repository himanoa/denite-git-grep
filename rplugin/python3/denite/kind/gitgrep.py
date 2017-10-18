# # -*- coding: utf-8 -*-
from .base import Base


class Kind(Base):

    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'gitgrep_kind'
        self.default_action = 'open'
        self.vim = vim

    def action_open(self, context):
        self.vim.command('echomsg "{}"'.format(context))
