import cv2
import numpy as np

class Stabilizer:
    def __init__(self):
        self.prev_gray = None
        self.prev_points = None
        self.frame_counter = 0
        self.feature_redection_threshold = 5
        self.transform_buffer = []  # Buffer to store recent transformations
        self.smoothing_window_size = 5  # Size of the smoothing window
        self.max_level = 3  # Maximum level of the pyramid
        self.win_size = (15, 15)  # Window size for optical flow
        self.min_feature_quality = 0.01
        self.max_feature_quality = 0.1
        self.min_feature_distance = 30
        self.max_feature_distance = 100

    def adjust_feature_parameters(self, num_features):
        """
        Adjust feature detection parameters based on the number of detected features.
        """
        if num_features < 50:
            self.min_feature_quality = min(self.max_feature_quality, self.min_feature_quality * 1.1)
            self.min_feature_distance = max(10, self.min_feature_distance - 5)
        elif num_features > 150:
            self.min_feature_quality = max(self.min_feature_quality, self.min_feature_quality / 1.1)
            self.min_feature_distance = min(self.max_feature_distance, self.min_feature_distance + 5)

    def process_first_frame(self, frame):
        self.prev_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.prev_points = cv2.goodFeaturesToTrack(self.prev_gray, maxCorners=200, qualityLevel=0.01, minDistance=30)
        self.frame_counter = 0
        self.transform_buffer = []
        num_features = len(self.prev_points)
        self.adjust_feature_parameters(num_features)

    def add_to_buffer(self, transform):
        if len(self.transform_buffer) >= self.smoothing_window_size:
            self.transform_buffer.pop(0)
        self.transform_buffer.append(transform)

    def average_transform(self):
        if len(self.transform_buffer) == 0:
            return None
        return np.mean(self.transform_buffer, axis=0)

    def stabilize_frame(self, curr_frame):
        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)

        if self.prev_gray is None or self.frame_counter >= self.feature_redection_threshold:
            self.prev_gray = curr_gray
            self.prev_points = cv2.goodFeaturesToTrack(self.prev_gray, maxCorners=200, qualityLevel=0.01, minDistance=30)
            self.frame_counter = 0
            num_features = len(self.prev_points)
            self.adjust_feature_parameters(num_features)
            return curr_frame

        # Calculate optical flow with pyramidal approach
        curr_points, status, _ = cv2.calcOpticalFlowPyrLK(
            self.prev_gray, curr_gray, 
            self.prev_points, None, 
            winSize=self.win_size, 
            maxLevel=self.max_level)

        good_prev_points = self.prev_points[status == 1]
        good_curr_points = curr_points[status == 1]

        if len(good_prev_points) < 4 or len(good_curr_points) < 4:
            return curr_frame

        # Use RANSAC to filter out outliers
        transform, inliers = cv2.estimateAffinePartial2D(good_prev_points, good_curr_points, method=cv2.RANSAC, ransacReprojThreshold=3.0)

        if transform is None or inliers is None or np.sum(inliers) < 4:
            return curr_frame

        # Add the current transform to the buffer
        self.add_to_buffer(transform)

        # Calculate the average transform
        avg_transform = self.average_transform()
        if avg_transform is None:
            return curr_frame

        height, width = curr_frame.shape[:2]
        stabilized_frame = cv2.warpAffine(curr_frame, avg_transform, (width, height))

        # Update for next frame
        self.prev_gray = curr_gray.copy()
        self.prev_points = good_curr_points[inliers.ravel() == 1].reshape(-1, 1, 2)

        self.frame_counter += 1

        return stabilized_frame