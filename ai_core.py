from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from utils.code_generator import CodeGenerator

class AICore:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        # Use GPT-2 as it's a free and capable model for text generation
        self.model_name = "gpt2"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.code_generator = CodeGenerator()

    def process_message(self, message):
        # Retrieve context from memory
        context = self.memory_manager.get_context(message)

        # Prepare input with context
        input_text = f"Context: {context}\nUser: {message}\nAssistant:"
        inputs = self.tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)

        # Generate response
        with torch.no_grad():
            outputs = self.model.generate(
                inputs["input_ids"],
                max_length=200,
                num_beams=4,
                temperature=0.7,
                pad_token_id=self.tokenizer.eos_token_id
            )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract only the assistant's response
        if "Assistant:" in response:
            response = response.split("Assistant:")[-1].strip()

        # Store interaction in memory
        self.memory_manager.store_interaction(message, response)

        return response

    def generate_code(self, prompt):
        # For code generation, use the code_generator which has templates
        return self.code_generator.generate(prompt)