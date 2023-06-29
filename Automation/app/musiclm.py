from diffusers import AudioLDMPipeline
import torch
import numpy
import soundfile as sf

# Define the path to save
output_path = 'audio_file.wav'

# Save the audio


repo_id = "cvssp/audioldm-s-full-v2"
pipe = AudioLDMPipeline.from_pretrained(repo_id, torch_dtype=torch.float32)
pipe = pipe.to("cpu")

prompt = "Optimistic melody about the arrival of spring, full of joy and hope, tranquil flute in the background, upbeat with a gentle guitar riff"
audio = pipe(prompt, num_inference_steps=10, audio_length_in_s=10.0).audios[0]

sf.write(output_path, audio, samplerate=22050) 