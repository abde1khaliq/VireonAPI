import argparse
from analyzer.ai import ModerationService

def moderate_in_cli(user_input=None):
    moderation = ModerationService()

    if user_input:
        result = moderation.moderate(content=user_input, content_type='text')
        print("📝 Text moderation result:")
        print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run moderation on text or image.")
    parser.add_argument("--text", type=str, help="Text input to moderate")

    args = parser.parse_args()
    moderate_in_cli(user_input=args.text)