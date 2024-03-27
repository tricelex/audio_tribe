import ffmpeg
import requests


# def transcode_video_to_audio( ffmpeg: FFmpeg, videoUrl: string):
def transcode_video_to_audio(video_url: str):
    print("fetch video data")
    video_data = requests.get(video_url).content

    # Write the video data to a file
    print("write video data to file")
    with open("input.mp4", "wb") as f:
        f.write(video_data)

    # Use ffmpeg to convert the video file to an audio file
    print("transcode video to audio")
    output = "output.mp3"
    ffmpeg.input("input.mp4").output(output).run()

    print(output)

    return output
