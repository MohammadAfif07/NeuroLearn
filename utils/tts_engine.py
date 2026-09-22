import streamlit as st
import base64
import os
import re
import tempfile
from io import BytesIO
try:
    from gtts import gTTS
    import pygame
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

class TTSEngine:
    def __init__(self):
        self.supported_languages = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German'
        }
        self.speech_rates = {
            'slow': 0.8,
            'normal': 1.0,
            'fast': 1.2
        }
    
    def text_to_speech(self, text, language='en', rate='normal', filename=None):
        """Convert text to speech using gTTS"""
        if not TTS_AVAILABLE:
            st.warning("gTTS and pygame not available. Please install: pip install gtts pygame")
            return None
            
        try:
            # Clean and prepare text
            cleaned_text = self.clean_text_for_speech(text)
            
            if not cleaned_text.strip():
                return None
            
            # Create gTTS object
            tts = gTTS(text=cleaned_text, lang=language, slow=(rate == 'slow'))
            
            # Create audio file
            if filename is None:
                filename = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
            
            tts.save(filename)
            return filename
            
        except Exception as e:
            st.error(f"Text-to-speech error: {str(e)}")
            return None
    
    def clean_text_for_speech(self, text):
        """Clean text for better speech synthesis"""
        # Remove markdown formatting
        text = re.sub(r'[#*_`~]', '', text)
        
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Limit text length for performance
        if len(text) > 1000:
            text = text[:1000] + "... [content truncated]"
        
        return text
    
    def play_audio(self, audio_file):
        """Play audio file using pygame"""
        if not TTS_AVAILABLE:
            return
            
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
                
        except Exception as e:
            st.error(f"Audio playback error: {str(e)}")
    
    def create_audio_player(self, audio_file):
        """Create an HTML audio player for the generated speech"""
        try:
            with open(audio_file, 'rb') as f:
                audio_bytes = f.read()
            
            audio_b64 = base64.b64encode(audio_bytes).decode()
            audio_html = f'''
                <audio controls autoplay style="width: 100%">
                    <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                    Your browser does not support the audio element.
                </audio>
            '''
            return audio_html
            
        except Exception as e:
            st.error(f"Audio player creation error: {str(e)}")
            return None
    
    def chunk_text_for_speech(self, text, max_chunk_length=500):
        """Split long text into chunks for better TTS performance"""
        sentences = re.split(r'[.!?]+', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_chunk_length:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def generate_speech_with_controls(self, text, language='en', rate='normal'):
        """Generate speech with playback controls"""
        if not text.strip():
            st.warning("No text available for speech synthesis.")
            return
        
        # Chunk long text
        chunks = self.chunk_text_for_speech(text)
        
        if len(chunks) > 1:
            st.info(f"Content split into {len(chunks)} parts for better audio quality.")
        
        for i, chunk in enumerate(chunks):
            if len(chunks) > 1:
                st.write(f"**Part {i+1} of {len(chunks)}:**")
                st.write(chunk[:200] + "..." if len(chunk) > 200 else chunk)
            
            # Generate audio file
            with st.spinner(f"Generating audio for part {i+1}..."):
                audio_file = self.text_to_speech(chunk, language, rate)
            
            if audio_file and os.path.exists(audio_file):
                # Create audio player
                audio_html = self.create_audio_player(audio_file)
                if audio_html:
                    st.markdown(audio_html, unsafe_allow_html=True)
                
                # Download button
                with open(audio_file, 'rb') as f:
                    audio_data = f.read()
                
                st.download_button(
                    label=f"Download Audio Part {i+1}",
                    data=audio_data,
                    file_name=f"neurolearn_audio_part_{i+1}.mp3",
                    mime="audio/mp3"
                )
                
                # Clean up temporary file
                try:
                    os.unlink(audio_file)
                except:
                    pass
                
                st.markdown("---")

# Alternative TTS using browser's built-in speech synthesis (no external API needed)
class BrowserTTS:
    def __init__(self):
        self.js_code = """
        <script>
        function speakText(text, rate=1.0, pitch=1.0) {
            if ('speechSynthesis' in window) {
                // Cancel any ongoing speech
                speechSynthesis.cancel();
                
                // Create speech synthesis utterance
                const utterance = new SpeechSynthesisUtterance();
                utterance.text = text;
                utterance.rate = rate;
                utterance.pitch = pitch;
                utterance.volume = 1;
                
                // Speak the text
                speechSynthesis.speak(utterance);
                
                return true;
            } else {
                return false;
            }
        }
        
        function stopSpeech() {
            if ('speechSynthesis' in window) {
                speechSynthesis.cancel();
            }
        }
        
        function pauseSpeech() {
            if ('speechSynthesis' in window) {
                speechSynthesis.pause();
            }
        }
        
        function resumeSpeech() {
            if ('speechSynthesis' in window) {
                speechSynthesis.resume();
            }
        }
        </script>
        """
    
    def create_speech_controls(self, text, element_id="speech-content"):
        """Create HTML controls for browser-based text-to-speech"""
        
        controls_html = f"""
        <div style="border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin: 10px 0;">
            <h4>🎧 Text-to-Speech Controls</h4>
            <div style="display: flex; gap: 10px; flex-wrap: wrap; align-items: center;">
                <button onclick="speakText(document.getElementById('{element_id}').innerText, 0.8, 1.0)" 
                        style="background: #4CAF50; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer;">
                    🐢 Slow Speech
                </button>
                <button onclick="speakText(document.getElementById('{element_id}').innerText, 1.0, 1.0)" 
                        style="background: #2196F3; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer;">
                    🚶 Normal Speech
                </button>
                <button onclick="speakText(document.getElementById('{element_id}').innerText, 1.2, 1.0)" 
                        style="background: #FF9800; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer;">
                    🏃 Fast Speech
                </button>
                <button onclick="pauseSpeech()" 
                        style="background: #FFC107; color: black; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer;">
                    ⏸️ Pause
                </button>
                <button onclick="resumeSpeech()" 
                        style="background: #00BCD4; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer;">
                    ▶️ Resume
                </button>
                <button onclick="stopSpeech()" 
                        style="background: #F44336; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer;">
                    ⏹️ Stop
                </button>
            </div>
            <div style="margin-top: 10px; font-size: 12px; color: #666;">
                <i>Uses your browser's built-in speech synthesis. Works best in Chrome and Edge.</i>
            </div>
        </div>
        """
        
        return self.js_code + controls_html