import os
import time
import tiktoken
from openai import OpenAI


class AICaller:
    def __init__(self, model):
        """
        Initializes an instance of the AICaller class.

        Parameters:
            model (str): The name of the model to be used.

        Raises:
            ValueError: If the OPENAI_API_KEY environment variable is not found or if there is an error in getting the encoding.

        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not found.")

        self.model = model
        self.openai_client = OpenAI(api_key=self.api_key)

        # Initialize the encoding for the model
        try:
            self.encoding = tiktoken.get_encoding("cl100k_base")
        except Exception as e:
            raise ValueError(f"Failed to get encoding: {e}")

    def call_model(self, prompt, max_tokens=4096):
        """
        Calls the OpenAI API with streaming enabled to get completions for a given prompt
        and streams the output to the console in real time, while also accumulating the response to return.

        Parameters:
            prompt (str): The prompt to send to the model.
            max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 4096.

        Returns:
            str: The text generated by the model.
        """
        response = self.openai_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            temperature=0,
            max_tokens=max_tokens,
            stream=True,
        )

        full_text = ""
        print("Streaming results from LLM model...")
        try:
            for chunk in response:
                if chunk.choices[0].delta and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(
                        content, end="", flush=True
                    )  # Print each part of the text as it arrives
                    full_text += content  # Accumulate the content in full_text
                    time.sleep(
                        0.01
                    )  # Optional: Delay to simulate more 'natural' response pacing
        except Exception as e:
            print(f"Error during streaming: {e}")
        print("\n")

        return full_text.strip()

    def count_tokens(self, text):
        """
        Counts the number of tokens in the given text using the model's encoding.

        Parameters:
            text (str): The text to encode.

        Returns:
            int: The number of tokens.
        """
        try:
            return len(self.encoding.encode(text))
        except Exception as e:
            raise ValueError(f"Error encoding text: {e}")
