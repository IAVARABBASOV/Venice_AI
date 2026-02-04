#!/usr/bin/env python3
"""
Quick start script for Venice AI Web Interface
"""

import os
import sys

def check_dependencies():
    """Check if required packages are installed"""
    required = ['flask', 'torch', 'transformers', 'bitsandbytes']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("❌ Missing dependencies:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n💡 Install with: pip install -r requirements.txt")
        return False
    
    return True

def check_gpu():
    """Check if CUDA GPU is available"""
    try:
        import torch
        if not torch.cuda.is_available():
            print("⚠️  Warning: CUDA GPU not detected")
            print("   This application requires an NVIDIA GPU with CUDA")
            response = input("\nContinue anyway? (y/n): ")
            return response.lower() == 'y'
        
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        
        print(f"✓ GPU detected: {gpu_name}")
        print(f"✓ VRAM: {gpu_memory:.1f} GB")
        
        if gpu_memory < 14:
            print("\n⚠️  Warning: Less than 14GB VRAM detected")
            print("   Application may run out of memory")
            response = input("\nContinue anyway? (y/n): ")
            return response.lower() == 'y'
        
        return True
    except Exception as e:
        print(f"❌ Error checking GPU: {e}")
        return False

def main():
    print("="*60)
    print(" Venice AI - Web Interface Launcher")
    print("="*60)
    print()
    
    # Check dependencies
    print("Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("✓ All dependencies installed\n")
    
    # Check GPU
    print("Checking GPU...")
    if not check_gpu():
        print("\n❌ GPU check failed. Exiting.")
        sys.exit(1)
    print()
    
    # Start server
    print("="*60)
    print(" Starting server...")
    print("="*60)
    print()
    
    # Import and run app
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from app import app, load_model
    
    print("Loading Venice AI model (this may take 1-2 minutes)...")
    load_model()
    
    print("\n" + "="*60)
    print(" 🚀 Server started successfully!")
    print("="*60)
    print("\n📍 Open in browser: http://localhost:5000")
    print("\n⌨️  Press Ctrl+C to stop\n")
    
    try:
        app.run(debug=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")

if __name__ == '__main__':
    main()
