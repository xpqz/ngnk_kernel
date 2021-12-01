"""
Derived from bash_kernel (https://github.com/takluyver/bash_kernel)
"""

from ipykernel.kernelbase import Kernel
import os
from pexpect import replwrap, EOF

import re

__version__ = '0.1'

version_pat = re.compile(r'version (\d+(\.\d+)+)')
NGNKDIR = os.environ['NGNKDIR']


class IREPLWrapper(replwrap.REPLWrapper):
    # As parent, but with incremental output
    def __init__(self,
                 cmd_or_spawn,
                 orig_prompt,
                 prompt_change,
                 new_prompt,
                 extra_init_cmd=None,
                 line_output_callback=None):
        self.line_output_callback = line_output_callback
        replwrap.REPLWrapper.__init__(self,
                                      cmd_or_spawn,
                                      orig_prompt,
                                      prompt_change,
                                      new_prompt,
                                      extra_init_cmd=extra_init_cmd)

    def _expect_prompt(self, timeout=-1):
        if timeout is None:
            while True:
                pos = self.child.expect_exact(
                    [self.prompt, self.continuation_prompt, u'\r\n'],
                    timeout=None)
                if pos == 2:
                    self.line_output_callback(self.child.before + '\n')
                else:
                    if len(self.child.before) != 0:
                        self.line_output_callback(self.child.before)
                    break
        else:
            pos = replwrap.REPLWrapper._expect_prompt(self, timeout=timeout)
        return pos


class NgnkKernel(Kernel):
    implementation = 'ngnk_kernel'
    implementation_version = __version__
    cmd = f'{NGNKDIR}/k {NGNKDIR}/repl.k'
    prompt = u'ngnk> '

    @property
    def language_version(self):
        # TODO
        m = version_pat.search(self.banner)
        return m.group(1)

    _banner = ''

    @property
    def banner(self):
        return self._banner

    language_info = {
        'name': 'ngnk',
        'mimetype': 'text/ngnk',
        'file_extension': '.k'
    }

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self._start_ngnk()

    def _start_ngnk(self):
        self.ngnkwrapper = IREPLWrapper(
            self.cmd,
            ' ',  # Prompt defaults to single space
            'repl.prompt:"ngnk> "',  # Command to change prompt
            self.prompt,  # New prompt after change
            line_output_callback=self.process_output)

    def process_output(self, output):
        stream_content = {'name': 'stdout', 'text': output}
        self.send_response(self.iopub_socket, 'stream', stream_content)

    def do_execute(self,
                   code,
                   silent,
                   store_history=True,
                   user_expressions=None,
                   allow_stdin=False):
        self.silent = silent
        if not code.strip():
            return {
                'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {}
            }

        interrupted = False
        try:
            self.ngnkwrapper.run_command(code.rstrip(), timeout=None)
        except KeyboardInterrupt:
            self.ngnkwrapper.child.sendintr()
            interrupted = True
            self.ngnkwrapper._expect_prompt()
            output = self.ngnkwrapper.child.before
            self.process_output(output)
        except EOF:
            output = self.ngnkwrapper.child.before + 'Restarting ngn/k'
            self._start_ngnk()
            self.process_output(output)

        if interrupted:
            return {'status': 'abort', 'execution_count': self.execution_count}

        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {}
        }

    def do_complete(self, code, cursor_pos):
        return {
            'matches': [],
            'cursor_start': 0,
            'cursor_end': cursor_pos,
            'metadata': dict(),
            'status': 'ok'
        }
