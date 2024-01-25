import cv2

class VideoCropper:
    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(video_path)
        self.roi = None
        self.valid_roi = False

    def select_roi(self):
        """
        Captures the first frame of the video and allows the user to select an ROI.
        Sets the ROI for the VideoCropper instance and checks its validity.
        """
        if not self.cap.isOpened():
            print("Error opening video file.")
            return None

        ret, frame = self.cap.read()
        if not ret:
            print("Error reading the first frame.")
            return None

        roi = cv2.selectROI("Select ROI", frame, False)
        cv2.destroyWindow("Select ROI")
        if roi[2] and roi[3]:  # Check if ROI has non-zero width and height
            self.roi = roi
            self.valid_roi = True
        return self.roi

    def crop_frame(self, frame):
        """
        Crops the given frame based on the previously selected ROI.
        """
        if self.valid_roi:
            return frame[int(self.roi[1]):int(self.roi[1] + self.roi[3]), int(self.roi[0]):int(self.roi[0] + self.roi[2])]
        return frame

    def reset_video(self):
        """
        Resets the video capture to the start.
        """
        if self.cap.isOpened():
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def select_second_roi(self, frame):
            """Allows the user to select a second region of interest on the given frame."""
            second_roi = cv2.selectROI("Select Second ROI", frame, False)
            cv2.destroyWindow("Select Second ROI")
            if second_roi[2] and second_roi[3]:  # Check if ROI has non-zero width and height
                return second_roi
            return None