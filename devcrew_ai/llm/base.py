from abc import ABC, abstractmethod

class BaseLLM(ABC):
    @abstractmethod
    def generate(self, prompt: str, system_instruction: str = "") -> str:
        """
        Generate text response from the model.
        
        Args:
            prompt: The user query or prompt.
            system_instruction: Instruction that guides model behavior.
            
        Returns:
            The generated string response.
        """
        pass
