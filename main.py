from dotenv import load_dotenv

from brochurizer import Brochurizer
from helpers.url_helper import URLHelper
from webpage import Webpage

load_dotenv()

def prompt_for_url():
    while True:
        url = input("Enter the URL of the page to brochurize: ").strip().lower()
        url = URLHelper.normalize_url(url)
        if not URLHelper.is_url_valid(url):
            continue
        if not URLHelper.is_url_reachable(url):
            continue
        print(f"ℹ️ Selected URL: {url}")
        return url


def prompt_for_platform():
    while True:
        platform = input("Enter the platform name: (Default: ollama. Supported: ollama, openai) ").strip().lower()
        if not platform:
            platform = 'ollama'
        if platform not in ['ollama', 'openai']:
            print("❌ Invalid platform. Please enter a valid platform name.")
            continue
        print(f"ℹ️ Selected platform: {platform}")
        return platform


def prompt_for_model(platform: str):
    while True:
        if platform == 'openai':
            model = input("Enter the model name (Default: gpt-4o-mini): ").strip().lower()
            if not model:
                model = 'gpt-4o-mini'
        elif platform == 'ollama':
            model = input("Enter the model name (Default: llama3.2): ").strip().lower()
            if not model:
                model = 'llama3.2'
        else:
            print(f"❌ Unsupported platform {platform}. Please select a valid platform.")
            continue
        print(f"ℹ️ Selected model: {model}")
        return model

def prompt_for_export():
    export = input("Do you want to export the brochure as a markdown file? (Y/n): ").strip().lower() or 'y'
    return export == 'y'

def main():
    while True:
        try:
            url = prompt_for_url()
            platform = prompt_for_platform()
            model = prompt_for_model(platform)
            export = prompt_for_export()
            webpage = Webpage(url)
            brochurizer = Brochurizer(platform=platform, model=model, webpage=webpage)
            brochurizer.create_brochure(export=export)
            break
        except (ValueError, OSError) as e:
            print(f"❌ Brochure creation failed: {e}")
            retry = input("Do you want to retry? (Y/n): ").strip().lower() or 'y'
            if retry != 'y':
                break
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            break
        except Exception as e:
            raise Exception(f"❌ An unexpected error occurred: {e}") from e
            break


if __name__ == '__main__':
    main()
