# extx.ai
> Run your own AI assistant locally on your computer with no cloud APIs, no internet requirements, and full privacy. Powered by [gpt4all](https://github.com/nomic-ai/gpt4all).

---

## License

MIT License. Do not remove credit.

## Features
- ChatGPT-style web interface
- Runs fully offline
- Messages and history saved locally
- Summarized chat titles
- Accessible from other devices on the same Wi-Fi (If you set up Windows Firewall)

---

## Requirements

- Python 3.13 (Recommended) Python 3.10+ (Required)
- \~4GB RAM minimum
- Windows Computer Recommended (This should work on a Mac or Linux Computer, however setup may be different for MacOS/Linux)

---

## Installation

### 1. **Install Python**

- Download Python from: [https://www.python.org/downloads/](https://www.python.org/downloads/)
> Be sure to check "Add Python to PATH" during installation.

### 2. **Clone or Download This Repo**

```bash
git clone https://github.com/fwextx/extx.ai.git
cd extx.ai
```

Or download the ZIP from GitHub and extract it.

### 3. **Create Virtual Environment**

```bash
python -m venv extxAI
```

### 4. **Activate Virtual Environment**

- On **Windows**:

```bash
extxAI\Scripts\activate
```

- On **macOS/Linux**:

```bash
source extxAI/bin/activate
```

### 5. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 6. **Run the App**
Assuming you activated the virtual enviroment you installed the packages in:
```bash
py app.py
```

### 7. **Access It in Your Browser**

- Local: http://127.0.0.1:5000
- Network: http://your-local-ip:5000 (for other devices on same Wi-Fi)

---

## Allow Through Firewall (Windows)

If it doesn't work on other devices:

- Go to **Windows Defender Firewall > Allow an app**
- Allow Python on **Private networks**

If it still doesn't work, open an Inbound Rule for port 5000.

---

## Tips

- New chats auto-generate titles using the first message
- Data is stored per device ID in `chat_history/history.json`
- App is 100% local. No server-side logs.
- You can run it entirely offline after installing everything

---

## FAQ

**Q: Can I use another model?**\
Yes! Change this line in `app.py`:

```python
model = GPT4All("YourModelName.gguf")
```

**Q: Why can’t I access it from my phone?**\
You may need to allow Python through Windows Firewall.

**Q: My chats disappear after restarting?**\
Check that your device ID isn’t resetting — it uses `localStorage`.

---

Made with ❤️ by Extx / `extx.ai`

