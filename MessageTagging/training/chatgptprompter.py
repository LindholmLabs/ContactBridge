import os
import openai

from MessageTagging.training.promptgenerator import PromptGenerator

openai.api_key = os.getenv("OPENAI_API_KEY")

print(os.getenv("OPENAI_API_KEY"))


class Prompter():
  def __init__(self, context=""):
    self.context = context
    self.messages = [{"role": "system", "content": self.context}]

  def prompt(self, prompt):
    user_message = {"role": "user", "content": prompt}
    messages = [
      self.messages[0],  # System message
      user_message  # User message
    ]
    return self.contact_chatgpt(messages)

  def contact_chatgpt(self, messages):
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )
    return completion['choices'][0]['message']['content']

  def set_context(self, context):
    self.context = context
    self.messages[0] = {"role": "system", "content": self.context}




if __name__ == "__main__":
  prompter = Prompter()
  prompt_generator = PromptGenerator('companies.csv', 'names.csv')

  prompter.set_context("Generate distinct, very short responses for a contact form, as an employer contacting a potential employee initially. Invent all names, avoid placeholders. No special formatting or line breaks. No subject line. Only provide the prompt.")
  generated_prompt = prompt_generator.generate_prompt()
  print(f"generated prompt: {generated_prompt}")
  print(prompter.prompt(generated_prompt))
