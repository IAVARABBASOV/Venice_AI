# Venice AI - Local Web Interface

<div align="center">

![Venice AI](https://img.shields.io/badge/Venice_AI-Uncensored-00ffff?style=for-the-badge&logo=openai&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-ff006e?style=for-the-badge)

**A stunning cyber-noir themed web interface for running Venice AI locally with GPU acceleration**
<img width="2508" height="1127" alt="Screenshot 2026-02-04 114348" src="https://github.com/user-attachments/assets/f815b309-55f9-4985-9c8e-ded737e70491" />

</div>

## 📋 Requirements

### Hardware
- **GPU**: NVIDIA GPU with **24-60+GB VRAM** (RTX 3090/4090, A5000, etc.)
- **RAM**: 16GB+ system memory recommended
- **Storage**: 50GB free space for model download

---

## 🚀 Installation

### Method 1: Automated Setup (Recommended for Windows)

1. **Download the All_in_One bat file to easy installation**
[Download VeniceAI_AllInOne.bat](https://github.com/IAVARABBASOV/Venice_AI/releases/download/release/VeniceAI_AllInOne.bat)

## 🎮 Usage

[Huggingface Page](https://huggingface.co/AskVenice/venice-uncensored)

(Youtube)[https://www.youtube.com/watch?v=dk1vHz4qwvM]

### Starting the Server

**Windows:**
```bash
start.bat
```

The server will:
1. Check for GPU availability
2. Load the Venice AI model (1-2 minutes first time)
3. Start Flask server on `http://localhost:5000`

### Memory Management

Click the **"⟳ CLEAR MEMORY"** button to:
- Clear conversation history
- Free GPU memory
- Reset to welcome screen

This is recommended after long conversations to prevent memory buildup.

---

## ⚙️ Configuration

### Adjusting Memory Usage

Edit `app.py` to modify generation parameters:

```python
# Reduce token generation for lower memory
"max_new_tokens": 256,  # Default: 512

# Adjust context window size
max_length=1024  # Default: 2048

# Change temperature (creativity)
"temperature": 0.15,  # Lower = more focused
```

### Changing Server Port

In `app.py` 

```python
app.run(debug=False, host='0.0.0.0', port=5000)  # Change port here
```

### Customizing Appearance

Edit `templates/index.html` 


---

## 🏗️ Project Structure

```
venice-ai-web/
├── app.py                      # Flask backend server
├── start.py                    # Launch script with checks
├── requirements.txt            # Python dependencies
├── start.bat                   # Windows launcher
├── templates/
│   └── index.html             # Main HTML interface
└── README.md                  # This file
```

---

## 🔒 Privacy & Security

### Local-First Design
- All processing happens on your machine
- No data sent to external servers
- No telemetry or tracking
- Complete conversation privacy

### Security Considerations
- **Local Use Only**: Default binding to `localhost`
- **No Authentication**: Not designed for multi-user access
- **Production Warning**: Do not expose directly to internet

To expose on network (use with caution):
```python
app.run(host='0.0.0.0', port=5000)  # Accessible on local network
```

For production deployment, use a reverse proxy with authentication.

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---


⭐ Star this repo if you find it useful!

</div>
