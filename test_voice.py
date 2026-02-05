"""
AlfredX Voice Test Script
=========================
Run this to test if your microphone and voice recognition are working.
"""

import sys
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


def test_microphone():
    """Test if microphone is working."""
    print("\n" + "="*50)
    print("🎤 MICROPHONE TEST")
    print("="*50)
    
    try:
        import sounddevice as sd
        
        # List audio devices
        print("\n📋 Available audio devices:")
        print(sd.query_devices())
        
        # Get default input device
        default_input = sd.query_devices(kind='input')
        print(f"\n✅ Default input device: {default_input['name']}")
        
        # Try to record a short audio sample
        print("\n🎤 Recording 2 seconds of audio... Speak now!")
        duration = 2
        sample_rate = 16000
        
        recording = sd.rec(int(duration * sample_rate), 
                          samplerate=sample_rate, 
                          channels=1, 
                          dtype='int16')
        sd.wait()
        
        # Check if we got audio
        import numpy as np
        max_amplitude = np.max(np.abs(recording))
        
        if max_amplitude > 500:
            print(f"✅ Audio captured! Max amplitude: {max_amplitude}")
            return True
        else:
            print(f"⚠️ Audio very quiet. Max amplitude: {max_amplitude}")
            print("   Check your microphone volume and try again.")
            return False
            
    except Exception as e:
        print(f"❌ Microphone test failed: {e}")
        return False


def test_vosk_models():
    """Test if Vosk models are loaded."""
    print("\n" + "="*50)
    print("📦 VOSK MODELS TEST")
    print("="*50)
    
    try:
        from config.settings import Settings
        from vosk import Model, SetLogLevel
        
        SetLogLevel(-1)
        
        models_ok = True
        
        # Test English model
        if Settings.MODEL_EN_PATH.exists():
            try:
                print(f"\n📁 English model path: {Settings.MODEL_EN_PATH}")
                model = Model(str(Settings.MODEL_EN_PATH))
                print("✅ English model loaded successfully!")
            except Exception as e:
                print(f"❌ English model failed: {e}")
                models_ok = False
        else:
            print(f"❌ English model not found at {Settings.MODEL_EN_PATH}")
            models_ok = False
        
        # Test Turkish model
        if Settings.MODEL_TR_PATH.exists():
            try:
                print(f"\n📁 Turkish model path: {Settings.MODEL_TR_PATH}")
                model = Model(str(Settings.MODEL_TR_PATH))
                print("✅ Turkish model loaded successfully!")
            except Exception as e:
                print(f"❌ Turkish model failed: {e}")
                models_ok = False
        else:
            print(f"❌ Turkish model not found at {Settings.MODEL_TR_PATH}")
            models_ok = False
        
        return models_ok
        
    except ImportError:
        print("❌ Vosk not installed. Run: pip install vosk")
        return False
    except Exception as e:
        print(f"❌ Vosk test failed: {e}")
        return False


def test_speech_recognition():
    """Test actual speech recognition."""
    print("\n" + "="*50)
    print("🗣️ SPEECH RECOGNITION TEST")
    print("="*50)
    
    try:
        from core.listener import Listener
        
        print("\n🎤 Initializing listener...")
        listener = Listener(language="en")
        
        if not listener.is_available():
            print("❌ Listener not available")
            return False
        
        print("✅ Listener initialized")
        
        recognized_texts = []
        
        def on_speech(text):
            print(f"   ✅ Recognized: {text}")
            recognized_texts.append(text)
        
        def on_partial(text):
            print(f"   ... Hearing: {text}", end='\r')
        
        listener.on_speech_recognized = on_speech
        listener.on_partial_result = on_partial
        
        print("\n🎤 Listening for 10 seconds...")
        print("   Say some words like: 'Hello', 'Gotham', 'Shadow', 'Knight'")
        print("-" * 40)
        
        listener.start_listening()
        
        # Listen for 10 seconds
        for i in range(10, 0, -1):
            print(f"   Time remaining: {i}s  ", end='\r')
            time.sleep(1)
        
        print("\n")
        listener.stop_listening()
        
        print("-" * 40)
        
        if recognized_texts:
            print(f"✅ Speech recognition working!")
            print(f"   Recognized {len(recognized_texts)} phrase(s):")
            for text in recognized_texts:
                print(f"      - {text}")
            return True
        else:
            print("⚠️ No speech recognized. Try speaking louder.")
            return False
        
    except Exception as e:
        print(f"❌ Speech recognition test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_activation_words():
    """Test activation word validation."""
    print("\n" + "="*50)
    print("🔐 ACTIVATION WORDS TEST")
    print("="*50)
    
    try:
        from config.activation_words import ActivationWords
        
        print(f"\n📋 Activation sequence ({len(ActivationWords.SEQUENCE)} words):")
        for i, word in enumerate(ActivationWords.SEQUENCE, 1):
            print(f"   {i}. {word.upper()}")
        
        # Test validation
        print("\n🧪 Testing word validation...")
        
        test_cases = [
            ("gotham", 0, True),
            ("shadow", 1, True),
            ("knight", 2, True),
            ("night", 2, True),  # Alternative
            ("random", 0, False),
            ("activate", 9, True),
        ]
        
        all_passed = True
        for word, index, expected in test_cases:
            result = ActivationWords.validate_word(word, index)
            status = "✅" if result == expected else "❌"
            if result != expected:
                all_passed = False
            print(f"   {status} validate_word('{word}', {index}) = {result} (expected {expected})")
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Activation words test failed: {e}")
        return False


def run_full_test():
    """Run all tests."""
    print("\n" + "="*60)
    print("🦇 ALFREDX VOICE SYSTEM TEST")
    print("="*60)
    
    results = {}
    
    # Test 1: Microphone
    results['microphone'] = test_microphone()
    
    # Test 2: Vosk models
    results['vosk_models'] = test_vosk_models()
    
    # Test 3: Activation words (no mic needed)
    results['activation_words'] = test_activation_words()
    
    # Test 4: Speech recognition (only if mic and models work)
    if results['microphone'] and results['vosk_models']:
        results['speech_recognition'] = test_speech_recognition()
    else:
        print("\n⚠️ Skipping speech recognition test (mic or models not working)")
        results['speech_recognition'] = False
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {test_name.replace('_', ' ').title()}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Voice activation should work.")
    else:
        print("⚠️ SOME TESTS FAILED. Check the issues above.")
    print("="*60)
    
    return all_passed


if __name__ == "__main__":
    run_full_test()
    
    input("\nPress Enter to exit...")
