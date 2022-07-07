import logging
import queue
import textwrap

from jupyter_client.manager import KernelManager
from rich import print

from ass_executor.utils import remove_ansi_escape

LOGGER = logging.getLogger("ass-executor.kernel")


def decode_traceback(traceback: str) -> str:
    return remove_ansi_escape('\n'.join(traceback))


class MyKernel:

    def __init__(self, name: str = "python3", startup_timeout: int = 60):
        self._kernel = KernelManager(kernel_name=name)
        self._kernel.start_kernel()
        self._client = self._kernel.client()
        self._client.start_channels()
        try:
            self._client.wait_for_ready(timeout=startup_timeout)
        except RuntimeError:
            self._client.stop_channels()
            self._kernel.shutdown_kernel()
            raise

    def is_alive(self) -> bool:
        return self._kernel.is_alive()

    def get_info(self):
        msg_id = self._client.kernel_info()
        reply = self._get_response(msg_id)
        output = self._get_output()
        return output

    def run_snippet(self, snippet: str) -> str:

        msg_id = self._client.execute(snippet)
        LOGGER.debug(f"{msg_id = }")

        reply = self._get_response(msg_id)
        LOGGER.debug(f"{type(reply) = }")
        LOGGER.debug(f"{reply = }")
        LOGGER.debug(f"{reply['content'] = }")

        # if reply["content"]["status"] == "error":
        #     try:
        #         return decode_traceback(reply["content"]["traceback"])
        #     except KeyError:
        #         return "An error occurred, no traceback was provided."

        output = self._get_output()
        # LOGGER.debug(f"{output = }")

        return output.strip()

    def _get_response(self, msg_id: str) -> dict:
        return self._client.get_shell_msg(msg_id)

    def _get_output(self, timeout: float = 1.0) -> str:

        # When the execution state is "idle" it is complete

        io_msg_content = self._client.get_iopub_msg(timeout=timeout)['content']

        if 'execution_state' in io_msg_content and io_msg_content['execution_state'] == 'idle':
            return ""

        while True:
            last_io_msg_content = io_msg_content

            try:
                io_msg_content = self._client.get_iopub_msg(timeout=timeout)['content']
                if 'execution_state' in io_msg_content and io_msg_content['execution_state'] == 'idle':
                    break
            except queue.Empty:
                break

        return self._decode_io_msg_content(last_io_msg_content)

    @staticmethod
    def _decode_io_msg_content(content: dict) -> str:

        if 'data' in content:  # Indicates completed operation
            return content['data']['text/plain']
        elif 'name' in content and content['name'] == "stdout":  # indicates output
            return content['text']
        elif 'traceback' in content:  # Indicates an error
            return decode_traceback(content['traceback'])
        else:
            return ''

    def __del__(self):
        self._client.stop_channels()
        self._kernel.shutdown_kernel()


def do_test_my_kernel(name: str = "python3"):

    kernel = MyKernel(name=name)

    snippets = [
        "a=2",
        textwrap.dedent("""\
            a = 42
            b = 73
            c = a + b
            print(c)        
            """),
        'print(f"{a=}, {b=}, {c=}")',
        '1/0',  # should return a ZeroDivisionError
        'import sys; print(f"{sys.path = }")',
        'import pandas as pd',
        'df = pd.DataFrame(dict(A=[1,2,3], B=["one", "two", "three"]))',
        'df',
        'df.describe()',
        '!pip list -v'
    ]

    for snippet in snippets:
        if out := kernel.run_snippet(snippet):
            print(out)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    # kernel_name = "python3"
    kernel_name = "plato-common-egse"

    do_test_my_kernel(name=kernel_name)
