import select
import subprocess

from usecases.ports.qa_engine import QaEngine


class LlamaQaEngine(QaEngine):
    def __init__(self):
        self.llama = subprocess.Popen(["ollama", "run", "llama2"],
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      universal_newlines=True,
                                      bufsize=0
                                      )

    def get_response(self) -> str:
        response = ""
        [self.llama.stdout.readline() for _ in range(2)]
        ready = True
        line = ""
        while ready and line is not None:
            line = self.llama.stdout.readline()
            response += line
            ready, _, _ = select.select([self.llama.stdout], [], [], 3)
        return response


    def send_message(self, message: str) -> None:
        self.llama.stdin.write(message.replace("\n", "") + "\n")

    def close(self):
        self.llama.stdin.close()