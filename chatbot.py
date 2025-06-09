import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_chatgpt_response(prompt):
    """
    Get a response from ChatGPT for the given prompt
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("Welcome to ChatGPT Bot! (Type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        # Check if user wants to quit
        if user_input.lower() == 'quit':
            print("\nGoodbye!")
            break
        
        # Get response from ChatGPT
        response = get_chatgpt_response(user_input)
        print("\nChatGPT:", response)

if __name__ == "__main__":
    main() 