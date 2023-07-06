from flask import Flask, render_template, request, redirect, url_for, send_file
from moviepy.editor import VideoFileClip, concatenate_videoclips
import ffmpeg
import os
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge_and_compress_videos():
    files = request.files.getlist('videos')

    video_clips = []
    for file in files:
        video_path = os.path.join('uploads', file.filename)
        file.save(video_path)
        video_clip = VideoFileClip(video_path)
        video_clips.append(video_clip)

    final_clip = concatenate_videoclips(video_clips)
    output_file = 'merged_video.mp4'
    final_clip.write_videofile(output_file)

    # Mengompresi video menggunakan ffmpeg
    input_file = output_file
    compressed_file = 'compressed_video.mp4'
    ffmpeg.input(input_file).output(compressed_file, crf=23).run()

    return send_file(compressed_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)