from ipykernel.kernelbase import Kernel
from pexpect import replwrap, EOF

import re

__version__ = '0.1'

version_pat = re.compile(r'version (\d+(\.\d+)+)')


class IREPLWrapper(replwrap.REPLWrapper):
    """A subclass of REPLWrapper that gives incremental output
    specifically for bash_kernel.

    The parameters are the same as for REPLWrapper, except for one
    extra parameter:

    :param line_output_callback: a callback method to receive each batch
      of incremental output. It takes one string parameter.
    """
    def __init__(self,
                 cmd_or_spawn,
                 orig_prompt,
                 prompt_change,
                 extra_init_cmd=None,
                 line_output_callback=None):
        self.line_output_callback = line_output_callback
        replwrap.REPLWrapper.__init__(self,
                                      cmd_or_spawn,
                                      orig_prompt,
                                      prompt_change,
                                      extra_init_cmd=extra_init_cmd)

    def _expect_prompt(self, timeout=-1):
        if timeout == None:
            # "None" means we are executing code from a Jupyter cell by way of the run_command
            # in the do_execute() code below, so do incremental output.
            while True:
                pos = self.child.expect_exact(
                    [self.prompt, self.continuation_prompt, u'\r\n'],
                    timeout=None)
                if pos == 2:
                    # End of line received
                    self.line_output_callback(self.child.before + '\n')
                else:
                    if len(self.child.before) != 0:
                        # prompt received, but partial line precedes it
                        self.line_output_callback(self.child.before)
                    break
        else:
            # Otherwise, use existing non-incremental code
            pos = replwrap.REPLWrapper._expect_prompt(self, timeout=timeout)

        # Prompt received, so return normally
        return pos


class NgnkKernel(Kernel):
    implementation = 'ngnk_kernel'
    implementation_version = __version__
    cmd = '/home/jovyan/k/k-libc /home/jovyan/k/repl.k'
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
            self.prompt,
            None,
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
