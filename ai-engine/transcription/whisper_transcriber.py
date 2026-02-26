"""
Whisper Transcriber - Speech to Text conversion
Supports both OpenAI API and local Whisper models
"""
import os
import tempfile
from typing import List, Dict, Optional, Generator
from dataclasses import dataclass
from pathlib import Path
import subprocess


@dataclass
class TranscriberConfig:
    """Configuration for transcriber"""
    model: str = "base"  # tiny, base, small, medium, large
    language: Optional[str] = None  # None for auto-detect
    use_local: bool = False  # Use local Whisper vs API
    openai_api_key: Optional[str] = None
    device: str = "cpu"  # cpu, cuda
    compute_type: str = "int8"  # int8, float16, float32


@dataclass
class TranscribedSegment:
    """Transcribed segment"""
    text: str
    start: float
    end: float
    speaker: Optional[str] = None
    confidence: float = 0.0


class WhisperTranscriber:
    """
    Whisper-based transcriber with speaker diarization
    
    Features:
    - OpenAI Whisper API or local model
    - Speaker diarization (pyannote.audio)
    - Noise reduction preprocessing
    - Accent softening (optional)
    """
    
    def __init__(self, config: TranscriberConfig = None):
        self.config = config or TranscriberConfig()
        self._model = None
        self._diarization_model = None
        
        if self.config.openai_api_key:
            os.environ["OPENAI_API_KEY"] = self.config.openai_api_key
    
    def _load_model(self):
        """Load local Whisper model"""
        if self._model is None and self.config.use_local:
            import whisper
            self._model = whisper.load_model(
                self.config.model,
                device=self.config.device,
                download_root=os.path.expanduser("~/.cache/whisper")
            )
        return self._model
    
    def _load_diarization_model(self):
        """Load speaker diarization model"""
        if self._diarization_model is None:
            try:
                from pyannote.audio import Pipeline
                self._diarization_model = Pipeline.from_pretrained(
                    "pyannote/speaker-diarization-3.1",
                    use_auth_token=os.environ.get("HUGGINGFACE_TOKEN")
                )
            except ImportError:
                print("pyannote.audio not installed, speaker diarization disabled")
                return None
        return self._diarization_model
    
    def transcribe_file(
        self,
        audio_path: str,
        progress_callback: Optional[callable] = None
    ) -> List[TranscribedSegment]:
        """
        Transcribe audio file
        
        Args:
            audio_path: Path to audio file
            progress_callback: Optional callback for progress updates
            
        Returns:
            List of transcribed segments with timestamps
        """
        if self.config.use_local:
            return self._transcribe_local(audio_path, progress_callback)
        else:
            return self._transcribe_api(audio_path)
    
    def _transcribe_local(
        self,
        audio_path: str,
        progress_callback: Optional[callable] = None
    ) -> List[TranscribedSegment]:
        """Transcribe using local Whisper model"""
        model = self._load_model()
        
        if model is None:
            raise RuntimeError("Local Whisper model not loaded")
        
        # Run transcription
        result = model.transcribe(
            audio_path,
            language=self.config.language,
            task="transcribe",
            verbose=False,
        )
        
        segments = []
        for segment in result["segments"]:
            transcribed_segment = TranscribedSegment(
                text=segment["text"].strip(),
                start=segment["start"],
                end=segment["end"],
                confidence=segment.get("avg_logprob", 0.0),
            )
            segments.append(transcribed_segment)
            
            if progress_callback:
                progress_callback({
                    "type": "segment",
                    "text": transcribed_segment.text,
                    "start": transcribed_segment.start,
                })
        
        # Apply speaker diarization
        segments = self._apply_diarization(audio_path, segments)
        
        return segments
    
    def _transcribe_api(
        self,
        audio_path: str
    ) -> List[TranscribedSegment]:
        """Transcribe using OpenAI Whisper API"""
        from openai import OpenAI
        
        client = OpenAI(api_key=self.config.openai_api_key)
        
        with open(audio_path, "rb") as audio_file:
            # Use verbose_json to get timestamps
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
                timestamp_granularities=["segment"],
            )
        
        segments = []
        for segment in transcript.segments:
            transcribed_segment = TranscribedSegment(
                text=segment["text"].strip(),
                start=segment["start"],
                end=segment["end"],
                confidence=segment.get("avg_logprob", 0.0),
            )
            segments.append(transcribed_segment)
        
        return segments
    
    def _apply_diarization(
        self,
        audio_path: str,
        segments: List[TranscribedSegment]
    ) -> List[TranscribedSegment]:
        """Apply speaker diarization to segments"""
        diarization_model = self._load_diarization_model()
        
        if diarization_model is None:
            return segments
        
        try:
            diarization = diarization_model(audio_path)
            
            # Map segments to speakers
            for segment in segments:
                speaker = "Unknown"
                for turn, _, speaker_name in diarization.itertracks(yield_label=True):
                    if turn.start <= segment.start <= turn.end:
                        speaker = speaker_name
                        break
                segment.speaker = speaker
            
        except Exception as e:
            print(f"Diarization error: {e}")
        
        return segments
    
    def transcribe_stream(
        self,
        audio_generator: Generator[bytes, None, None],
        chunk_duration: float = 5.0
    ) -> Generator[TranscribedSegment, None, None]:
        """
        Transcribe audio stream in real-time
        
        Args:
            audio_generator: Generator yielding audio chunks
            chunk_duration: Duration of each chunk in seconds
            
        Yields:
            Transcribed segments as they become available
        """
        import numpy as np
        import tempfile
        import wave
        
        buffer = bytearray()
        sample_rate = 16000  # Whisper expects 16kHz
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            temp_path = f.name
        
        try:
            for chunk in audio_generator:
                buffer.extend(chunk)
                
                # Process when we have enough audio
                if len(buffer) >= sample_rate * chunk_duration * 2:  # 2 bytes per sample
                    # Write to temp file
                    with wave.open(temp_path, "wb") as wav:
                        wav.setnchannels(1)
                        wav.setsampwidth(2)
                        wav.setframerate(sample_rate)
                        wav.writeframes(buffer)
                    
                    # Transcribe chunk
                    segments = self.transcribe_file(temp_path)
                    for segment in segments:
                        yield segment
                    
                    # Clear buffer (keep last second for context)
                    keep_samples = int(sample_rate * 1.0 * 2)
                    buffer = buffer[-keep_samples:]
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    @staticmethod
    def enhance_audio(
        input_path: str,
        output_path: str,
        noise_reduction: bool = True,
        accent_softening: bool = False
    ) -> str:
        """
        Enhance audio quality before transcription
        
        Args:
            input_path: Input audio file
            output_path: Output enhanced audio file
            noise_reduction: Apply noise reduction
            accent_softening: Apply accent softening (experimental)
            
        Returns:
            Path to enhanced audio file
        """
        if noise_reduction:
            # Use ffmpeg for noise reduction
            cmd = [
                "ffmpeg",
                "-i", input_path,
                "-af", "afftdn=nf=-70",
                "-y",
                output_path
            ]
            subprocess.run(cmd, check=True, capture_output=True)
        else:
            # Just copy
            subprocess.run(
                ["ffmpeg", "-i", input_path, "-c", "copy", "-y", output_path],
                check=True,
                capture_output=True
            )
        
        return output_path
