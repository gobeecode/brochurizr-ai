import os


class CredentialHelper:

    @staticmethod
    def validate_openai_api_key():
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment file. Make sure it is configured correctly")
        elif api_key[:8] != "sk-proj-":
            raise ValueError("Invalid OPENAI_API_KEY format.")
        else:
            print("API key is found.")