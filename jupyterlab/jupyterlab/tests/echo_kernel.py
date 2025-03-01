# -*- coding: utf-8 -*-
import logging

from ipykernel.kernelapp import IPKernelApp
from ipykernel.kernelbase import Kernel


class EchoKernel(Kernel):
    implementation = 'Echo'
    implementation_version = '1.0'
    language = 'echo'
    language_version = '0.1'
    language_info = {
        'name': 'echo',
        'mimetype': 'text/plain',
        'file_extension': '.txt',
    }
    banner = "Echo kernel - as useful as a parrot"

    def do_execute(self, code, silent, store_history=True,
            user_expressions=None, allow_stdin=False):
        if not silent:
            stream_content = {'name': 'stdout', 'text': code}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {}}


class EchoKernelApp(IPKernelApp):
    kernel_class = EchoKernel


if __name__ == '__main__':
    logging.disable(logging.ERROR)
    EchoKernelApp.launch_instance()
