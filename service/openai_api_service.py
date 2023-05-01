import os
import openai

# This code defines a custom service class called OpenAICore that provides a 
# static method called send_chat_request() for sending a user's text prompt to 
# the OpenAI API and returning the resulting text response. The method first 
# reads prompt text from three separate files called element.prompt, group.prompt, 
# and metadata.prompt. It then checks whether the user's prompt contains the keywords "group" or 
# "metadata" and selects the appropriate prompt text accordingly. Finally, it sends 
# the combined prompt text and user's prompt to the OpenAI API using the 
# ChatCompletion.create() method and returns the resulting text response as a 
# dictionary with "error" and "response" keys.

# The code relies on the openai module to access the OpenAI API and the os module to 
# access the OpenAI API key stored in an environment variable.  
# The send_chat_request() method takes a single parameter called promptUser, which is the 
# user's text input prompt. It then constructs a combined prompt text by concatenating the 
# appropriate base prompt text with the user's prompt and sends it to the OpenAI API using 
# the ChatCompletion.create() method. The resulting text response is then returned as a 
# dictionary with "error" and "response" keys. If an exception occurs during the API request, 
# the method returns an error message as the value of the "error" key.


openai.api_key = os.environ["OPENAI_API_KEY"]


class OpenAICore:

    @staticmethod
    def send_chat_request(promptUser):
        # Read prompt ext from file
        element_prompt = " "
        group_prompt = " "
        MODEL = "gpt-3.5-turbo"
        with open('prompt/element.prompt', 'r') as f:
            element_prompt = f.read()
        with open('prompt/group.prompt', 'r') as f:
            group_prompt = f.read()
        with open('prompt/metadata.prompt', 'r') as f:
            metadata_prompt = f.read()
        try:
            if 'group' in promptUser.lower():
                promptBase = group_prompt
                print('')
                print('********** Sending GROUP prompt **********')
                print('')
            elif 'metadata' in promptUser.lower():
                promptBase = metadata_prompt
                print('')
                print('********** Sending METADATA prompt **********')
                print('')
            else:
                promptBase = element_prompt
                print('')
                print('********** Sending ELEMENT prompt **********')
                print('')
            prompt = promptBase + ' ```' + promptUser.strip() + ' ```'
            print(prompt)
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
            )
            api_response = {
                "error": None, "response": response['choices'][0]['message']['content']}
            print('')
            print('Response: ', api_response)
            print('')
            return api_response
        except Exception as e:
            print('')
            print(f"Error while API request: {e}")
            return {"error": str(e), "response": None}
