import cv2
import numpy as np
from collections import deque

class HeatmapGenerator:
    def __init__(self, buffer_size, threshold, focus_shift, target_hue, hue_tolerance):
        self.frame_buffer = deque(maxlen=buffer_size)
        self.threshold = threshold
        self.focus_shift = focus_shift
        self.target_hue = target_hue
        self.hue_tolerance = hue_tolerance
        self.epsilon = 1e-10

    def add_frame(self, frame):
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        self.frame_buffer.append(hsv_frame)

    def calculate_baseline(self):
        # Calculate dynamic baseline based on the buffer
        stacked_frames = np.stack(self.frame_buffer, axis=0)
        baseline_mean = np.mean(stacked_frames, axis=0)
        baseline_std = np.std(stacked_frames, axis=0)
        return baseline_mean, baseline_std

    def create_heatmap(self, current_frame):
        baseline_mean, baseline_std = self.calculate_baseline()

        # Convert current frame to HSV
        hsv_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2HSV)

        # Calculate Z-scores for the current frame
        z_scores = (hsv_frame - baseline_mean) / (baseline_std + self.epsilon)

        # Apply focus shift
        adjusted_threshold = self.threshold * self.focus_shift

        # Create a mask for the target hue range
        lower_bound = max(0, self.target_hue - self.hue_tolerance)
        upper_bound = min(179, self.target_hue + self.hue_tolerance)
        hue_mask = (hsv_frame[:, :, 0] >= lower_bound) & (hsv_frame[:, :, 0] <= upper_bound)

        # Combine hue mask with Z-score threshold for all channels
        mask = (np.abs(z_scores) > adjusted_threshold) & hue_mask[:,:,np.newaxis]

        # Aggregate changes across all channels
        aggregate_mask = np.any(mask, axis=2)

        heatmap = np.zeros_like(hsv_frame[:, :, 0], dtype=np.uint8)
        heatmap[aggregate_mask] = 255  # Mark significant changes across any channel
        heatmap_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

         # Define kernel for morphological operations
        kernel = np.ones((20, 20), np.uint8)

        # Apply morphological operations
        heatmap_eroded = cv2.erode(heatmap, kernel, iterations=1)
        heatmap_dilated = cv2.dilate(heatmap_eroded, kernel, iterations=1)

        # Opening (erosion followed by dilation)
        heatmap_opened = cv2.morphologyEx(heatmap, cv2.MORPH_OPEN, kernel)

        # Closing (dilation followed by erosion)
        heatmap_closed = cv2.morphologyEx(heatmap, cv2.MORPH_CLOSE, kernel)

        # Choose which heatmap to return based on your preference
        # For example, if you want to use the heatmap after opening operation:
        heatmap_processed = heatmap_opened

        # Convert to colored heatmap if desired
        #heatmap_colored = cv2.applyColorMap(heatmap_processed, cv2.COLORMAP_TURBO)

        return heatmap_colored