from ipykernel.kernelbase import Kernel
from pexpect import replwrap, EOF

import re

__version__ = '0.1'

version_pat = re.compile(r'version (\d+(\.\d+)+)')


class NgnkKernel(Kernel):
    implementation = 'ngnk_kernel'
    implementation_version = __version__
    cmd = '/usr/bin/rlwrap ./k/k-libc ./k/repl.k'
    prompt = 'ngnk> '
    silent = False

    @property
    def language_version(self):
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
        change_prompt = "PS1('{0}'); PS2('{1}')"
        self.ngnkwrapper = replwrap.REPLWrapper(self.cmd, self.prompt,
                                                change_prompt)

    def process_output(self, output):
        if not self.silent:
            # Send standard output
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

        try:
            exitcode = int(self.ngnkwrapper.run_command('echo $?').rstrip())
        except Exception:
            exitcode = 1

        if exitcode:
            error_content = {
                'ename': '',
                'evalue': str(exitcode),
                'traceback': []
            }
            self.send_response(self.iopub_socket, 'error', error_content)

            error_content['execution_count'] = self.execution_count
            error_content['status'] = 'error'
            return error_content
        else:
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
