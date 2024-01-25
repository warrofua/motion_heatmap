import numpy as np

def calculate_baseline(video_cropper, stabilizer, num_frames=5):
    baseline_frames = []
    for _ in range(num_frames):
        ret, frame = video_cropper.cap.read()
        if not ret:
            print("Error reading frame or end of video reached.")
            break

        # Crop and stabilize the frame
        cropped_frame = video_cropper.crop_frame(frame)
        stabilized_frame = stabilizer.stabilize_frame(cropped_frame)
        baseline_frames.append(stabilized_frame)

    if baseline_frames:
        # Convert list of frames to a NumPy array for efficient computation
        frames_array = np.array(baseline_frames)
        baseline_mean = np.mean(frames_array, axis=0)
        baseline_std = np.std(frames_array, axis=0)
        return baseline_mean, baseline_std
    else:
        print("No frames were processed for baseline calculation.")
        return None, None