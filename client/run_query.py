import time
from openai import OpenAI

# --- Configuration ---

# This is the model you pulled in the setup step.
MODEL_NAME = "qwen3:4b"

# This is the URL of the Ollama service defined in docker-compose.yml
# The service name 'ollama' acts as the hostname inside the Docker network.
OLLAMA_BASE_URL = "http://ollama:11434/v1"

# --- End of Configuration ---

def query_llm(client, prompt):
    """
    Sends the user's prompt to the LLM and prints the response.
    """
    try:
        start_time = time.time()
        
        print("\nThinking...")

        # Send the chat completion request
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        end_time = time.time()
        
        # Extract and print the response
        response_content = response.choices[0].message.content
        print("\n--- LLM Response ---")
        print(response_content)
        print("--------------------")
        print(f"Response generated in {end_time - start_time:.2f} seconds.\n")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please ensure the 'ollama' service is running and you have")
        print(f"pulled the model by running: docker-compose exec ollama ollama pull {MODEL_NAME}\n")

def main():
    """
    Main function to run the interactive chat loop.
    """
    print(f"Connecting to Ollama at {OLLAMA_BASE_URL}...")
    
    # Initialize the OpenAI client to connect to Ollama
    # The API key is required by the library but not used by Ollama.
    try:
        client = OpenAI(
            base_url=OLLAMA_BASE_URL,
            api_key='ollama',
        )
        # Quick check to see if the server is responsive
        client.models.list()
        print(f"Connection successful. Ready to chat with '{MODEL_NAME}'.")
        print("Type 'exit' or 'quit' to end the session.")
    except Exception as e:
        print(f"Failed to connect to Ollama: {e}")
        print("Please ensure the 'ollama' service is running.")
        return

    while True:
        try:
            prompt = input("You: ")
            if prompt.lower() in ['exit', 'quit']:
                print("Exiting chat. Goodbye!")
                break
            
            if not prompt.strip():
                continue
                
            query_llm(client, prompt)

        except EOFError:
            print("\nExiting chat. Goodbye!")
            break
        except KeyboardInterrupt:
            print("\nExiting chat. Goodbye!")
            break

if __name__ == "__main__":
    main()

