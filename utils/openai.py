import openai
import random
import time


class OpenAIKey:
    def __init__(self, keys_file_path):
        self.keys = self.get_openai_keys(keys_file_path)
        random.seed(int(time.time()))
        openai.api_key = random.choice(self.keys)

    def get_openai_keys(self, keys_file_path):
        raw_key_list = []
        with open(keys_file_path,"r") as f:
            for line in f.readlines():
                key = line.split("----")[2].strip()
                raw_key_list.append(key)
        return raw_key_list
    
    def switch_key(self):
        if len(self.keys) == 0:
            return None
        elif len(self.keys) == 1:
            print("No other keys available, waiting for 5s")
            time.sleep(5)
            openai.api_key = self.keys[0]
            return openai.api_key
        else:
            key = random.choice(self.keys)
            while key == openai.api_key:
                key = random.choice(self.keys)
            openai.api_key = key
            return key

    def remove_key(self):
        self.keys.remove(openai.api_key)

    def process_error(self, e):
        if "RateLimitError" in repr(e) or "APIConnectionError" in repr(e) or "AuthenticationError" in repr(e):
            if "per min" in repr(e):
                print(f"Rate limit reached for key {self.current_key}")
            elif "current quota" in repr(e):
                self.remove_key()
                print(e)
                print(f"Remove key {self.current_key}")
                
            self.switch_key()
            if self.current_key is None:
                print("All the keys are expired!")
                exit(0)
        else:
            print(f"Unknown error: {e}")


def create_response(model, prompt_input, max_tokens=256, temperature=0.0, stop=None):
    if stop is None:
        response = openai.Completion.create(
            model=model,
            prompt=prompt_input,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
    else:
        response = openai.Completion.create(
            model=model,
            prompt=prompt_input,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["{}:".format(stop)]
        )
    return response["choices"][0]["text"]


def create_response_chat(model="gpt-3.5-turbo", prompt_input=None, max_tokens=256, temperature=0.0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=prompt_input,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response["choices"][0]["message"]["content"]

def get_model_response(model: str, user_input: str) -> str:
    response = create_response_chat(
        model=model,
        prompt_input=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
        max_tokens=32,
        temperature=0
    )
    return response