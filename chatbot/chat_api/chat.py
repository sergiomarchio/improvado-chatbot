from .gpt4free import usesless

base_url_file = 'chatbot/chat_api/base_url.txt'
urls_file = 'chatbot/chat_api/urls.txt'
initial_prompt_file = 'chatbot/chat_api/initial_prompt.txt'


class Chatbot:

    def __init__(self, temperature: float = 0.5, timeout: int = 60):
        self.temperature = temperature
        self.timeout = timeout

        with open(base_url_file, 'r') as f:
            base_url = f.readline()

        # Load url list
        with open(urls_file, 'r') as f:
            url_list = [f'{base_url}{entry}' for entry in f.readlines()]
            urls = ''.join(url_list)

        with open(initial_prompt_file, 'r') as f:
            context = f.read().replace('{urls}', urls)

        # First request with initial instructions
        print("Setting up chatbot behavior...")
        req = usesless.Completion.create(prompt=context, temperature=0.5)

        self.message_id = req["id"]

        print(f"Initial answer {self.message_id}: {req['text']}")

    def send_message(self, message: str) -> str:
        req = usesless.Completion.create(prompt=message,
                                         parentMessageId=self.message_id,
                                         temperature=self.temperature,
                                         timeout=self.timeout)

        answer = req['text']
        self.message_id = req["id"]

        print(f"User: {message}")
        print(f"Answer {self.message_id}: {answer}")

        return answer
