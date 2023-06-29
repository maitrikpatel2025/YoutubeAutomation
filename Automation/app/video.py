# import os
# import random
# from pydub import AudioSegment
# from moviepy.editor import ImageSequenceClip, AudioFileClip

# try:
#     # directory containing image files
#     image_dir = "images"

#     # get a list of all image file paths
#     all_image_files = [os.path.join(image_dir, img) for img in os.listdir(image_dir) if img.endswith(".jpg")]
#     # select a random subset of images
#     num_images = len(all_image_files)  # or however many images you want
#     if num_images == 0:
#         raise ValueError("No images found in the directory")

#     image_files = random.sample(all_image_files, num_images)

#     # load audio file and get its duration
#     audio_file = "./script_audio.mp3"
#     audio = AudioSegment.from_mp3(audio_file)
#     audio_duration = len(audio) / 1000  # duration in seconds

#     # calculate duration per image based on audio length
#     duration_per_image = audio_duration / num_images  # duration of each image

#     # load images into moviepy
#     clip = ImageSequenceClip(image_files, durations=[duration_per_image]*len(image_files))

#     # set the frames per second
#     clip = clip.set_duration(duration_per_image*len(image_files)).set_fps(24)

#     # set audio
#     audio_clip = AudioFileClip(audio_file)

#     clip = clip.set_audio(audio_clip)

#     # write the result to a file
#     clip.fps = 24
#     clip.write_videofile('video.mp4', codec='libx264')

# except FileNotFoundError as e:
#     print(f"Error: {e}")
# except Exception as e:
#     print(f"Something went wrong: {e}")

# import os
# import random
# from pydub import AudioSegment
# from moviepy.editor import *

# # directory of images
# image_dir = 'images'
# # path of audio file
# audio_file = './script_audio.mp3'

# # get a list of all image file paths
# all_image_files = [os.path.join(image_dir, img) for img in os.listdir(image_dir) if img.endswith(".jpg")]
# # select a random subset of images
# num_images = len(all_image_files)  # or however many images you want
# if num_images == 0:
#     raise ValueError("No images found in the directory")

# image_files = random.sample(all_image_files, num_images)

# # load audio file and get its duration
# audio = AudioSegment.from_mp3(audio_file)
# audio_duration = len(audio) / 1000  # duration in seconds

# # calculate duration per image based on audio length
# duration_per_image = audio_duration / num_images  # duration of each image

# video_clips = []
# for image_file in image_files:
#     img_clip = ImageClip(image_file, duration=duration_per_image)
#     effect = random.randint(1, 3)
#     if effect == 1:
#         img_clip = img_clip.fadein(1).fadeout(1)  # fade in and fade out over 1 second
#     elif effect == 2:
#         img_clip = img_clip.crossfadein(1).crossfadeout(1)  # crossfade in and out over 1 second
#     else:
#         img_clip = img_clip.resize(1.3)  # 1.3 times bigger
#         img_clip = img_clip.crop(x_center=img_clip.w/2, y_center=img_clip.h/2, width=img_clip.w/1.3, height=img_clip.h/1.3)
#     video_clips.append(img_clip)

# # concatenate all clips
# video = concatenate_videoclips(video_clips)
# video.fps = 24
# # add the audio
# audio_background = AudioFileClip(audio_file)
# final_audio = CompositeAudioClip([audio_background])
# video = video.set_audio(final_audio)

# video.write_videofile("final_output.mp4")
import cv2
import numpy as np
import os
import random
from PIL import Image, ImageEnhance, ImageDraw, ImageFilter
from pydub import AudioSegment

# Directory of images
image_dir = 'images'
# Path of audio file
audio_file = './script_audio_hindi.mp3'

# Get a list of all image file paths
all_image_files = [os.path.join(image_dir, img) for img in os.listdir(
    image_dir) if img.endswith(".jpg")]

# Select a random subset of images
num_images = len(all_image_files)
if num_images == 0:
    raise ValueError("No images found in the directory")

image_files = random.sample(all_image_files, num_images)

# Load audio file and get its duration
audio = AudioSegment.from_mp3(audio_file)
audio_duration = len(audio) / 1000  # duration in seconds

# Calculate the total number of frames for the entire video based on the audio duration
total_frames = int(audio_duration * 24)  # Assuming a frame rate of 24 FPS

# Calculate the number of frames per image
frames_per_image = total_frames // num_images

# Create video writer
frame = cv2.imread(image_files[0])
height, width, layers = frame.shape
video = cv2.VideoWriter(
    'video.avi', cv2.VideoWriter_fourcc(*'XVID'), 24, (width, height))


def add_image_with_slide(video, img, frames):
    width, height = img.size
    # Extend the canvas to create room for sliding
    canvas = Image.new('RGB', (width*2, height))

    # Slide in
    for i in range(frames // 3):
        # Position the image to the right at the beginning
        pos = i * (width // (frames // 3))
        new_frame = canvas.copy()
        new_frame.paste(img, (pos, 0))
        new_frame = new_frame.crop((width // 2, 0, width + width // 2, height))
        video.write(cv2.cvtColor(np.array(new_frame), cv2.COLOR_RGB2BGR))

    for i in range(frames // 3, 2 * frames // 3):
        video.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
    # Slide out
    for i in range(frames // 3):
        # Position the image to the left at the end
        pos = width // 2 - i * (width // (frames // 3))
        new_frame = canvas.copy()
        new_frame.paste(img, (pos, 0))
        new_frame = new_frame.crop((0, 0, width, height))
        video.write(cv2.cvtColor(np.array(new_frame), cv2.COLOR_RGB2BGR))


def add_image_with_zoom(video, img, frames):
    width, height = img.size

    # Zoom in
    for i in np.linspace(1, 1.3, frames // 3):
        zoomed = img.resize((int(width*i), int(height*i)))
        center = zoomed.width // 2, zoomed.height // 2
        cropped = zoomed.crop((center[0] - width // 2, center[1] -
                              height // 2, center[0] + width // 2, center[1] + height // 2))
        video.write(cv2.cvtColor(np.array(cropped), cv2.COLOR_RGB2BGR))
    
    for i in range(frames // 3, 2 * frames // 3):
        video.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
    # Zoom out
    for i in np.linspace(1, 1.3, frames // 3)[::-1]:
        zoomed = img.resize((int(width*i), int(height*i)))
        center = zoomed.width // 2, zoomed.height // 2
        cropped = zoomed.crop((center[0] - width // 2, center[1] -
                              height // 2, center[0] + width // 2, center[1] + height // 2))
        video.write(cv2.cvtColor(np.array(cropped), cv2.COLOR_RGB2BGR))


def add_image_with_fade(video, img, frames):
    enhancer = ImageEnhance.Brightness(img)

    # Fade in
    for i in np.linspace(0, 1, frames // 3):
        enhanced_im = enhancer.enhance(i)
        video.write(cv2.cvtColor(np.array(enhanced_im), cv2.COLOR_RGB2BGR))

    # Static image
    for i in range(frames // 3, 2 * frames // 3):
        video.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))

    # Fade out
    for i in np.linspace(1, 0, frames // 3):
        enhanced_im = enhancer.enhance(i)
        video.write(cv2.cvtColor(np.array(enhanced_im), cv2.COLOR_RGB2BGR))


def add_image_with_zoom_and_slide(video, img, frames):
    width, height = img.size
    # Extend the canvas to create room for sliding
    canvas = Image.new('RGB', (width*2, height))
    # Slide in and Zoom in
    for i in np.linspace(1, 1.3, frames // 3):
        # Position the image to the right at the beginning
        pos = (frames // 3 - i) * (width // (frames // 3))
        zoomed = img.resize((int(width*i), int(height*i)))
        center = zoomed.width // 2, zoomed.height // 2
        cropped = zoomed.crop((center[0] - width // 2, center[1] -
                              height // 2, center[0] + width // 2, center[1] + height // 2))
        new_frame = canvas.copy()
        new_frame.paste(cropped, (int(pos), 0))
        new_frame = new_frame.crop((width // 2, 0, width + width // 2, height))
        video.write(cv2.cvtColor(np.array(new_frame), cv2.COLOR_RGB2BGR))

    # Static image
    for i in range(frames // 3, 2 * frames // 3):
        video.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))

    # Slide out and Zoom out
    for i in np.linspace(1, 1.3, frames // 3)[::-1]:
        # Position the image to the left at the end
        pos = (i - 1) * (width // (frames // 3))
        zoomed = img.resize((int(width*i), int(height*i)))
        center = zoomed.width // 2, zoomed.height // 2
        cropped = zoomed.crop((center[0] - width // 2, center[1] -
                              height // 2, center[0] + width // 2, center[1] + height // 2))
        new_frame = canvas.copy()
        new_frame.paste(cropped, (int(pos), 0))
        new_frame = new_frame.crop((0, 0, width, height))
        video.write(cv2.cvtColor(np.array(new_frame), cv2.COLOR_RGB2BGR))

    # Slide out and Zoom out

def add_image_with_zoom_and_fade(video, img, frames):
    width, height = img.size

    # Zoom in with fade-in
    for i in np.linspace(0, 1, frames // 4):
        zoom_factor = 1 + i * 0.3
        zoomed = img.resize((int(width*zoom_factor), int(height*zoom_factor)))
        center = zoomed.width // 2, zoomed.height // 2
        cropped = zoomed.crop((center[0] - width // 2, center[1] -
                              height // 2, center[0] + width // 2, center[1] + height // 2))
        enhanced_im = ImageEnhance.Brightness(cropped).enhance(i)
        video.write(cv2.cvtColor(np.array(enhanced_im), cv2.COLOR_RGB2BGR))

    # Static image with full zoom
    for i in range(frames // 4, 3 * frames // 4):
        zoom_factor = 1.3
        zoomed = img.resize((int(width*zoom_factor), int(height*zoom_factor)))
        center = zoomed.width // 2, zoomed.height // 2
        cropped = zoomed.crop((center[0] - width // 2, center[1] -
                              height // 2, center[0] + width // 2, center[1] + height // 2))
        video.write(cv2.cvtColor(np.array(cropped), cv2.COLOR_RGB2BGR))

    # Zoom out with fade-out
    for i in np.linspace(1, 0, frames // 4):
        zoom_factor = 1 + i * 0.3
        zoomed = img.resize((int(width*zoom_factor), int(height*zoom_factor)))
        center = zoomed.width // 2, zoomed.height // 2
        cropped = zoomed.crop((center[0] - width // 2, center[1] -
                              height // 2, center[0] + width // 2, center[1] + height // 2))
        enhanced_im = ImageEnhance.Brightness(cropped).enhance(i)
        video.write(cv2.cvtColor(np.array(enhanced_im), cv2.COLOR_RGB2BGR))


def add_image_with_slide_and_fade(video, img, frames):
    width, height = img.size
    # Extend the canvas to create room for sliding
    canvas = Image.new('RGB', (width*2, height))

    # Slide in with fade-in
    for i in np.linspace(0, 1, frames // 4):
        pos = i * (width // (frames // 4))
        new_frame = canvas.copy()
        new_frame.paste(img, (int(pos), 0))
        new_frame = new_frame.crop((width // 2, 0, width + width // 2, height))
        enhanced_im = ImageEnhance.Brightness(new_frame).enhance(i)
        video.write(cv2.cvtColor(np.array(enhanced_im), cv2.COLOR_RGB2BGR))

    # Static image
    for i in range(frames // 4, 3 * frames // 4):
        video.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))

    # Slide out with fade-out
    for i in np.linspace(1, 0, frames // 4):
        pos = (1 - i) * (width // (frames // 4))
        new_frame = canvas.copy()
        new_frame.paste(img, (int(pos), 0))
        new_frame = new_frame.crop((width // 2, 0, width + width // 2, height))
        enhanced_im = ImageEnhance.Brightness(new_frame).enhance(i)
        video.write(cv2.cvtColor(np.array(enhanced_im), cv2.COLOR_RGB2BGR))


def add_image_with_crossfade(video, img, frames):
    width, height = img.size
    alpha = np.linspace(0, 1, frames // 2)

    # Crossfade in
    for a in alpha:
        img_blend = Image.blend(img, Image.new(
            'RGB', (width, height), (255, 255, 255)), a)
        video.write(cv2.cvtColor(np.array(img_blend), cv2.COLOR_RGB2BGR))

    # Static image
    for _ in range(frames // 2):
        video.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))

    # Crossfade out
    for a in reversed(alpha):
        img_blend = Image.blend(img, Image.new(
            'RGB', (width, height), (255, 255, 255)), a)
        video.write(cv2.cvtColor(np.array(img_blend), cv2.COLOR_RGB2BGR))


def add_image_with_iris(video, img, frames):
    width, height = img.size
    center = (width // 2, height // 2)
    radius = 0
    radius_increment = max(width, height) / (frames // 2)

    # Iris effect in
    for _ in range(frames // 2):
        mask = Image.new('L', (width, height), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([(center[0] - radius, center[1] - radius),
                          (center[0] + radius, center[1] + radius)], fill=255)
        img_masked = Image.composite(img, Image.new(
            'RGB', (width, height), (0, 0, 0)), mask)
        video.write(cv2.cvtColor(np.array(img_masked), cv2.COLOR_RGB2BGR))
        radius += radius_increment

    # Static image
    for _ in range(frames // 2):
        video.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))

    # Iris effect out
    for _ in range(frames // 2):
        mask = Image.new('L', (width, height), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([(center[0] - radius, center[1] - radius),
                          (center[0] + radius, center[1] + radius)], fill=255)
        img_masked = Image.composite(img, Image.new(
            'RGB', (width, height), (0, 0, 0)), mask)
        video.write(cv2.cvtColor(np.array(img_masked), cv2.COLOR_RGB2BGR))
        radius -= radius_increment


def add_image_with_cube(video, img, frames):
    width, height = img.size
    cube_size = min(width, height) // 2
    cube_increment = cube_size / (frames // 2)

    # Cube effect in
    for i in range(frames // 2):
        cube_mask = Image.new('L', (width, height), 0)
        cube_draw = ImageDraw.Draw(cube_mask)
        cube_draw.rectangle([(i * cube_increment, i * cube_increment),
                            (width - i * cube_increment, height - i * cube_increment)], fill=255)
        img_masked = Image.composite(img, Image.new(
            'RGB', (width, height), (0, 0, 0)), cube_mask)
        video.write(cv2.cvtColor(np.array(img_masked), cv2.COLOR_RGB2BGR))

    # Static image
    for _ in range(frames // 2):
        video.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))

    # Cube effect out
    for i in range(frames // 2):
        cube_mask = Image.new('L', (width, height), 0)
        cube_draw = ImageDraw.Draw(cube_mask)
        cube_draw.rectangle([(i * cube_increment, i * cube_increment),
                            (width - i * cube_increment, height - i * cube_increment)], fill=255)
        img_masked = Image.composite(img, Image.new(
            'RGB', (width, height), (0, 0, 0)), cube_mask)
        video.write(cv2.cvtColor(np.array(img_masked), cv2.COLOR_RGB2BGR))


def add_image_with_blur(video, img, frames):
    width, height = img.size
    kernel_size = 15
    kernel_increment = kernel_size / (frames // 2)

    # Blur effect in
    for i in range(frames // 2):
        blurred = img.filter(ImageFilter.GaussianBlur(kernel_size))
        video.write(cv2.cvtColor(np.array(blurred), cv2.COLOR_RGB2BGR))
        kernel_size -= kernel_increment

    # Static image
    for _ in range(frames // 2):
        video.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))

    # Blur effect out
    for i in range(frames // 2):
        blurred = img.filter(ImageFilter.GaussianBlur(kernel_size))
        video.write(cv2.cvtColor(np.array(blurred), cv2.COLOR_RGB2BGR))
        kernel_size += kernel_increment


# Add images to video with fade-in and fade-out effects
for image_file in image_files:
    img = Image.open(image_file)
    effect = random.choice([add_image_with_fade, add_image_with_zoom, add_image_with_blur, add_image_with_blur, add_image_with_iris, add_image_with_blur, add_image_with_blur, add_image_with_fade, add_image_with_crossfade,
                           add_image_with_crossfade,  add_image_with_iris, add_image_with_fade, add_image_with_zoom_and_fade, add_image_with_zoom])
    effect(video, img, frames_per_image)
video.release()

# Convert avi video to mp4
os.system(f"ffmpeg -i video.avi -codec copy video.mp4")

# Add audio to the video
os.system(
    f"ffmpeg -i video.mp4 -i {audio_file} -codec copy -shortest final_output.mp4")
