import requests
import json
import yaml

# Load configuration from YAML file
def load_config():
    with open('ollama_config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config

# Helper functions  

def llm_chat(messages):
    try:
        config = load_config()
        
        
         # Input validation for messages
        if not isinstance(messages, list):
            raise ValueError("Messages must be a list")

        for message in messages:
            if not isinstance(message, dict):
                raise ValueError("Each message must be a dictionary")
        
        data = {
            'model': config['llm']["chat_model"], 
            'messages': messages,   
            'temperature': config['llm']['temperature'],
            'stream': False
        }
        llm_chat_url = config['llm']["url"] + config['llm']["chat_endpoint"]
        
     
        json_data = json.dumps(data)
        headers = config['llm']["headers"]
        
        # Add a reasonable timeout
        response = requests.post(llm_chat_url, data=json_data, headers=headers, timeout=10)

        if response.status_code == 200:
            # Check content type
            if 'application/json' in response.headers.get('Content-Type', ''):
                response_json = response.json()
                actual_response = response_json.get("message", "No message in response")
                return actual_response
            else:
                return "Invalid response format"
        else:
            return f"Request failed with status code {response.status_code}"

    except requests.RequestException as e:
        return f"Network error occurred: {str(e)}"
    except ValueError as ve:
        return f"Configuration error: {str(ve)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


def llm_instruct(prompt, system="you are a helpful assistant"):
    try:
        config = load_config()

        # Input validation
        if not isinstance(prompt, str):
            raise ValueError("Prompt must be a string")
        if not isinstance(system, str):
            raise ValueError("System description must be a string")

        data = {
            'model': config['llm']["instruct_model"], 
            'prompt': prompt,
            'system': system,   
            'temperature': config['llm']['temperature'],
            'stream': False
        }
        llm_instruct_url = config['llm']["url"] + config['llm']["instruct_endpoint"]
        
  
        json_data = json.dumps(data)
        headers = config['llm']["headers"]
        
        # Add a reasonable timeout
        response = requests.post(llm_instruct_url, data=json_data, headers=headers, timeout=10)

        if response.status_code == 200:
            # Check content type
            if 'application/json' in response.headers.get('Content-Type', ''):
                response_json = response.json()
                actual_response = response_json.get("response", "No response in JSON")
                return actual_response
            else:
                return "Invalid response format"
        else:
            return f"Request failed with status code {response.status_code}"

    except requests.RequestException as e:
        return f"Network error occurred: {str(e)}"
    except ValueError as ve:
        return f"Configuration error: {str(ve)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

# Sample usage of llm_instruct 
if __name__ == "__main__":
    print("Running sample usage of ollama_helpers.py")
    prompt="what is the meaning of life?"
    system="talk like a pirate"
    response=llm_instruct(prompt,system=system)
    print(response)

    # Sample usage of llm_chat
    messages= [
            {"role": "system", "content": "talk like a surfer dude."},
            {"role": "user", "content": "What is the meaning of life."},
    ##        {"role": "assistant", "content": "possible responses in the context?"},
    ##        {"role": "user", "content": "more stuff"},
    ]
    #print(json.dumps(messages,indent=4))

    response=llm_chat(messages)

    print(response)

