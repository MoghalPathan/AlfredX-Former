import os

print("=" * 50)
print("🦇 AlfredX Setup Verification")
print("=" * 50)

# Test Python packages
packages = [
    ("PyQt5", "PyQt5"),
    ("Vosk", "vosk"),
    ("Sounddevice", "sounddevice"),
    ("Numpy", "numpy"),
    ("Psutil", "psutil"),
    ("OpenCV", "cv2"),
    ("Groq", "groq"),
    ("Edge-TTS", "edge_tts"),
    ("MediaPipe", "mediapipe"),
    ("PyAutoGUI", "pyautogui"),
]

print("\n📦 Package Status:")
print("-" * 30)

for name, module in packages:
    try:
        __import__(module)
        print(f"✅ {name}")
    except ImportError:
        print(f"❌ {name} - FAILED")

# Test Vosk models
print("\n🎤 Vosk Models:")
print("-" * 30)

if os.path.exists("model-en"):
    print("✅ English model (model-en)")
else:
    print("❌ English model - NOT FOUND")
    print("   Download from: https://alphacephei.com/vosk/models")

if os.path.exists("model-tr"):
    print("✅ Turkish model (model-tr)")
else:
    print("❌ Turkish model - NOT FOUND")
    print("   Download from: https://alphacephei.com/vosk/models")

# Test .env file
print("\n🔑 Configuration:")
print("-" * 30)

if os.path.exists(".env"):
    print("✅ .env file exists")
else:
    print("⚠️  .env file - Will create later")

print("\n" + "=" * 50)
print("🦇 Setup verification complete!")
print("=" * 50)