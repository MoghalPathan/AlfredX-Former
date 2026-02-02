# 🦇 AlfredX: Waynecore Assistant

<p align="center">
  <img src="assets/images/logo.png" alt="AlfredX Logo" width="200">
</p>

<p align="center">
  <strong>AI-powered desktop assistant inspired by JARVIS & Alfred Pennyworth</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#project-structure">Structure</a>
</p>

---

## 🎯 Features

### 🎤 Winter Soldier Protocol (Voice Activation)
Speak 10 Batman-themed activation words in sequence to unlock:
```
GOTHAM → SHADOW → KNIGHT → LEGACY → PROTOCOL
GUARDIAN → VENGEANCE → JUSTICE → WAYNE → ACTIVATE
```

### 🌐 Bilingual Support
- **English**: British butler personality (formal, witty, "Sir/Master")
- **Turkish**: Casual friendly assistant
- **Auto-detection**: Automatically switches based on speech

### 💻 System Control
- Open/close applications
- Take screenshots
- System information (CPU, RAM, Disk)
- Lock screen
- Shutdown/restart

### 🎵 Media Control
- Volume up/down/mute
- Play/pause/skip tracks
- Media key simulation

### 🧠 AI Conversation
- Natural language understanding via Groq API (Llama 3)
- Context-aware responses
- Personality-driven interactions

### 🎨 JARVIS-Style GUI
- Cyan/teal HUD interface
- Rotating AI core animation
- Circular system gauges
- Voice waveform visualization
- Real-time activity log

---

## 📦 Installation

### Prerequisites
- Python 3.10+
- Windows 10/11
- Microphone
- Internet connection (for AI features)

### Step 1: Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/AlfredX-Waynecore-Assistant.git
cd AlfredX-Waynecore-Assistant
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download Vosk Models
Download and extract to project root:
- [English Model](https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip) → `model-en/`
- [Turkish Model](https://alphacephei.com/vosk/models/vosk-model-small-tr-0.3.zip) → `model-tr/`

### Step 5: Configure API Key
```bash
cp .env.example .env
```
Edit `.env` and add your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```
Get free key at: https://console.groq.com/

---

## 🚀 Usage

### Run the Application
```bash
python main.py
```

### Login Options
1. **Voice Activation**: Speak the 10 activation words
2. **Text Password**: Enter `MEZEYAT`

### Voice Commands (English)
```
"Open Chrome"
"What's the time?"
"Take a screenshot"
"Volume up"
"Play music"
"What's the weather like?"
"Search for Python tutorials"
```

### Voice Commands (Turkish)
```
"Chrome'u aç"
"Saat kaç?"
"Ekran görüntüsü al"
"Sesi aç"
"Müzik çal"
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **GUI Framework** | PyQt5 |
| **Speech Recognition** | Vosk (offline) |
| **Text-to-Speech** | Edge-TTS (Microsoft) |
| **AI/LLM** | Groq API (Llama 3) |
| **Computer Vision** | OpenCV + MediaPipe |
| **System Control** | psutil, pyautogui |
| **Audio Control** | pycaw |
| **Database** | SQLite |

---

## 📁 Project Structure

```
AlfredX/
├── main.py                 # Application entry point
├── requirements.txt        # Dependencies
├── .env                    # API keys (gitignored)
├── .env.example            # Template
│
├── config/                 # Configuration
│   ├── settings.py         # App settings
│   ├── activation_words.py # Winter Soldier protocol
│   └── personas.py         # Alfred's personality
│
├── core/                   # Core functionality
│   ├── listener.py         # Speech recognition
│   ├── speaker.py          # Text-to-speech
│   ├── brain.py            # AI integration
│   ├── language_detector.py
│   └── command_parser.py
│
├── gui/                    # User interface
│   ├── main_window.py
│   ├── login_screen.py
│   ├── dashboard.py
│   ├── widgets/            # Custom widgets
│   │   ├── circular_gauge.py
│   │   ├── waveform.py
│   │   ├── rotating_core.py
│   │   └── hud_panel.py
│   └── styles/
│       └── themes.py       # JARVIS theme
│
├── skills/                 # Skill modules
│   ├── system_control.py
│   ├── media_control.py
│   ├── file_manager.py
│   ├── web_search.py
│   └── vision.py
│
├── assets/                 # Resources
│   ├── icons/
│   ├── sounds/
│   └── images/
│
├── model-en/               # English Vosk model (gitignored)
├── model-tr/               # Turkish Vosk model (gitignored)
│
└── data/                   # Runtime data
    └── command_history.db
```

---

## 🎨 Theme Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Cyan | `#00f7ff` | Primary accent |
| Cyan Dim | `#00a8b3` | Secondary text |
| Teal | `#00d4aa` | Success/User |
| Green | `#00ff88` | Status OK |
| Orange | `#ffaa00` | Warning |
| Red | `#ff3333` | Error |
| Dark | `#000000` | Background |

---

## 🔮 Roadmap

- [ ] Hand gesture control (MediaPipe)
- [ ] Face recognition login
- [ ] Smart home integration
- [ ] Custom wake word
- [ ] Plugin system
- [ ] Mobile companion app

---

## 👨‍💻 Author

**[Your Name]**
- Final Year Computer Engineering Project
- [Your University]
- [Your Email]
- [Your GitHub]

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by JARVIS from Iron Man
- Alfred Pennyworth from DC Comics
- Winter Soldier activation sequence from Marvel
- Anthropic Claude for development assistance

---

<p align="center">
  <strong>🦇 "I shall be your guide through the digital night, Master Wayne." 🦇</strong>
</p>
