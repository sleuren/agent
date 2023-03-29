#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import plugins

class Plugin(plugins.BasePlugin):
    __name__ = 'exim'

    def run(self, config):
        '''
        exim mail queue monitoring, needs sudo access!
        '''
        data = {}
        data['queue_size'] = int(os.popen('sudo exim -bpc').read())
        return data

if __name__ == '__main__':
    Plugin().execute()
