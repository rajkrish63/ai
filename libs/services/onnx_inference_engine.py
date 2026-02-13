import os
import json
import numpy as np
from typing import List, Dict, Optional, Generator, Callable

class ONNXInferenceEngine:
    """
    ONNX Runtime-based inference engine for text generation.
    Supports streaming, temperature, top-k, and top-p sampling.
    """
    
    def __init__(self, model_path: str):
        """
        Initialize the inference engine.
        
        Args:
            model_path: Path to directory containing model files
        """
        self.model_path = model_path
        self.session = None
        self.tokenizer = None
        self.config = None
        self.is_loaded = False
    
    def load(self) -> bool:
        """Load the ONNX model and tokenizer."""
        try:
            # Import ONNX Runtime
            import onnxruntime as ort
            
            # Load model
            model_file = os.path.join(self.model_path, "model_int8.onnx")
            if not os.path.exists(model_file):
                print(f"Model file not found: {model_file}")
                return False
            
            # Create ONNX session with CPU provider
            session_options = ort.SessionOptions()
            session_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
            
            self.session = ort.InferenceSession(
                model_file,
                sess_options=session_options,
                providers=['CPUExecutionProvider']
            )
            
            # Load tokenizer
            tokenizer_file = os.path.join(self.model_path, "tokenizer.json")
            if os.path.exists(tokenizer_file):
                with open(tokenizer_file, 'r') as f:
                    self.tokenizer = json.load(f)
            
            # Load config
            config_file = os.path.join(self.model_path, "config.json")
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    self.config = json.load(f)
            
            self.is_loaded = True
            return True
            
        except Exception as e:
            print(f"Failed to load model: {e}")
            return False
    
    def tokenize(self, text: str) -> List[int]:
        """
        Tokenize input text.
        This is a placeholder - actual tokenization depends on the model.
        """
        # TODO: Implement proper tokenization based on tokenizer.json
        # For now, return mock token IDs
        return [1] + [ord(c) % 1000 for c in text[:100]] + [2]
    
    def detokenize(self, token_ids: List[int]) -> str:
        """
        Convert token IDs back to text.
        This is a placeholder - actual detokenization depends on the model.
        """
        # TODO: Implement proper detokenization
        # For now, return placeholder
        return "".join([chr(min(127, tid)) for tid in token_ids if tid > 2])
    
    def generate(self, 
                 prompt: str,
                 max_tokens: int = 512,
                 temperature: float = 0.7,
                 top_k: int = 40,
                 top_p: float = 0.9,
                 streaming_callback: Optional[Callable[[str], None]] = None) -> str:
        """
        Generate text based on prompt.
        
        Args:
            prompt: Input text prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0 - 1.0)
            top_k: Top-K sampling parameter
            top_p: Top-P (nucleus) sampling parameter
            streaming_callback: Optional callback for streaming tokens
            
        Returns:
            Generated text
        """
        if not self.is_loaded:
            return "Error: Model not loaded"
        
        try:
            # Tokenize input
            input_ids = self.tokenize(prompt)
            
            # Generate tokens
            generated_ids = []
            for _ in range(max_tokens):
                # Run inference (placeholder logic)
                # In real implementation, this would call self.session.run()
                # For now, simulate token generation
                
                # Mock: Generate random token
                next_token = np.random.randint(3, 1000)
                generated_ids.append(next_token)
                
                # Check for EOS token (mock: token ID 2)
                if next_token == 2:
                    break
                
                # Stream token if callback provided
                if streaming_callback:
                    token_text = self.detokenize([next_token])
                    streaming_callback(token_text)
            
            # Detokenize to text
            output_text = self.detokenize(generated_ids)
            return output_text
            
        except Exception as e:
            return f"Error during generation: {e}"
    
    def sample_token(self, logits: np.ndarray, temperature: float, 
                     top_k: int, top_p: float) -> int:
        """
        Sample next token from logits using temperature, top-k, and top-p.
        
        Args:
            logits: Model output logits
            temperature: Sampling temperature
            top_k: Top-K parameter
            top_p: Top-P parameter
            
        Returns:
            Sampled token ID
        """
        # Apply temperature
        logits = logits / max(temperature, 1e-5)
        
        # Top-K filtering
        if top_k > 0:
            indices_to_remove = logits < np.partition(logits, -top_k)[-top_k]
            logits[indices_to_remove] = -float('inf')
        
        # Convert to probabilities
        probs = self._softmax(logits)
        
        # Top-P (nucleus) filtering
        if top_p < 1.0:
            sorted_indices = np.argsort(probs)[::-1]
            sorted_probs = probs[sorted_indices]
            cumsum = np.cumsum(sorted_probs)
            
            # Remove tokens with cumulative probability above threshold
            remove_indices = cumsum > top_p
            if np.any(remove_indices):
                # Keep at least one token
                remove_indices[0] = False
                sorted_indices_to_remove = sorted_indices[remove_indices]
                probs[sorted_indices_to_remove] = 0
        
        # Renormalize
        probs = probs / np.sum(probs)
        
        # Sample
        return np.random.choice(len(probs), p=probs)
    
    @staticmethod
    def _softmax(x: np.ndarray) -> np.ndarray:
        """Compute softmax values."""
        exp_x = np.exp(x - np.max(x))
        return exp_x / exp_x.sum()
    
    def unload(self) -> None:
        """Unload the model to free memory."""
        self.session = None
        self.tokenizer = None
        self.config = None
        self.is_loaded = False
