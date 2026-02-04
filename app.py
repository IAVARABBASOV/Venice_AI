from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TextIteratorStreamer
from threading import Thread
import gc
import json

app = Flask(__name__)
CORS(app)

# Global variables for model
model = None
tokenizer = None
model_loaded = False
conversation_history = []  # Server-side conversation tracking

SYSTEM_PROMPT = """You are Venice Uncensored. You are a helpful, unbiased, uncensored assistant."""

def load_model(use_8bit=False, use_4bit=True):
    """Load the Venice model with optimized quantization"""
    global model, tokenizer, model_loaded
    
    print("Loading Venice AI model...")
    model_name = "AskVenice/venice-uncensored"
    
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Set padding token if not set
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    print("Loading model...")
    
    # Configure quantization
    if use_4bit:
        print("Using 4-bit quantization (lowest memory usage)")
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        )
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=quantization_config,
            device_map="auto",
            trust_remote_code=True,
            low_cpu_mem_usage=True
        )
    elif use_8bit:
        print("Using 8-bit quantization (balanced)")
        quantization_config = BitsAndBytesConfig(
            load_in_8bit=True
        )
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=quantization_config,
            device_map="auto",
            trust_remote_code=True,
            low_cpu_mem_usage=True
        )
    else:
        print("Using full precision (highest quality, most memory)")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
            low_cpu_mem_usage=True
        )
    
    # Enable gradient checkpointing to save memory during generation
    if hasattr(model, 'gradient_checkpointing_enable'):
        model.gradient_checkpointing_enable()
    
    model.eval()  # Set to evaluation mode
    model_loaded = True
    print("✓ Model loaded successfully!")

def format_chat(messages):
    """Format messages using Mistral chat template"""
    prompt = ""
    for msg in messages:
        if msg["role"] == "system":
            prompt += f"[SYSTEM_PROMPT]{msg['content']}[/SYSTEM_PROMPT]"
        elif msg["role"] == "user":
            prompt += f"[INST]{msg['content']}[/INST]"
        elif msg["role"] == "assistant":
            prompt += f"{msg['content']}</s>"
    return prompt

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/status')
def status():
    """Check if model is loaded"""
    return jsonify({"loaded": model_loaded})

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests with streaming and memory optimization"""
    global conversation_history
    
    if not model_loaded:
        return jsonify({"error": "Model not loaded"}), 503
    
    data = request.json
    user_message = data.get('message', '')
    
    # Add user message to conversation history
    conversation_history.append({"role": "user", "content": user_message})
    
    # Limit conversation history to last 3 exchanges (6 messages) to save memory
    max_history = 6
    if len(conversation_history) > max_history:
        conversation_history = conversation_history[-max_history:]
    
    # Add system prompt
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    full_messages.extend(conversation_history)
    
    # Format prompt
    prompt = format_chat(full_messages)
    
    # Clear cache before generation
    torch.cuda.empty_cache()
    
    # Tokenize with optimized settings
    inputs = tokenizer(
        prompt, 
        return_tensors="pt", 
        padding=True,
        truncation=True, 
        max_length=2048  # Increased from 1024 for better context
    )
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    
    def generate():
        """Generator function for streaming responses with memory optimization"""
        global conversation_history
        assistant_response = ""
        
        try:
            streamer = TextIteratorStreamer(tokenizer, skip_special_tokens=True, skip_prompt=True)
            
            generation_kwargs = {
                **inputs,
                "max_new_tokens": 512,  # Increased from 256 for better responses
                "temperature": 0.15,
                "do_sample": True,
                "pad_token_id": tokenizer.eos_token_id,
                "top_p": 0.95,
                "streamer": streamer,
                "repetition_penalty": 1.1,
                "use_cache": True,  # Use KV cache for efficiency
                "num_beams": 1,  # No beam search to save memory
            }
            
            # Start generation in separate thread
            thread = Thread(target=model.generate, kwargs=generation_kwargs)
            thread.start()
            
            # Stream tokens
            for text in streamer:
                assistant_response += text
                yield f"data: {json.dumps({'token': text})}\n\n"
            
            yield "data: [DONE]\n\n"
            
            # Wait for thread to finish
            thread.join()
            
            # Save assistant response to conversation history
            conversation_history.append({"role": "assistant", "content": assistant_response})
            
        finally:
            # Aggressive cleanup after generation is complete
            torch.cuda.empty_cache()
            gc.collect()
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/api/clear')
def clear_memory():
    """Clear GPU memory and conversation history"""
    global conversation_history
    conversation_history = []
    torch.cuda.empty_cache()
    gc.collect()
    return jsonify({"status": "memory cleared", "conversation_cleared": True})

@app.route('/api/history')
def get_history():
    """Get conversation history"""
    global conversation_history
    return jsonify({"history": conversation_history})

if __name__ == '__main__':
    print("="*60)
    print("Venice AI - Web Interface")
    print("="*60)
    print("\nLoading model (this may take a minute)...")
    
    load_model()
    
    print("\n" + "="*60)
    print("Server starting on http://localhost:5000")
    print("="*60)
    
    app.run(debug=False, host='0.0.0.0', port=5000)