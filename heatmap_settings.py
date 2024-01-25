import cv2

class HeatmapSettings:
    def __init__(self, window_name):
        """
        Initialize the HeatmapSettings class with a given window name.
        Args:
            window_name (str): Name of the OpenCV window.
        """
        self.window_name = window_name
        self.initialize_trackbars()

    def initialize_trackbars(self):
        """
        Create trackbars for adjusting heatmap settings.
        """
        cv2.createTrackbar('Threshold', self.window_name, 20, 100, self.update_threshold)
        cv2.createTrackbar('Opacity', self.window_name, 30, 100, self.update_opacity)
        cv2.createTrackbar('Focus Shift', self.window_name, 50, 100, self.update_focus_shift)
        cv2.createTrackbar('Target Hue', self.window_name, 0, 179, self.update_target_hue)
        cv2.createTrackbar('Hue Tolerance', self.window_name, 10, 50, self.update_hue_tolerance)

    # callback methods for each trackbar
    def update_threshold(self, x):
        # Update threshold based on trackbar position
        pass

    def update_opacity(self, x):
        # Update opacity based on trackbar position
        pass

    def update_focus_shift(self, x):
        # Update focus shift based on trackbar position
        pass

    def update_target_hue(self, x):
        # Update target hue based on trackbar position
        pass

    def update_hue_tolerance(self, x):
        # Update hue tolerance based on trackbar position
        pass

    def get_threshold(self):
        """
        Get the current threshold value from the trackbar.
        Returns:
            float: Current threshold setting as a fraction of the maximum value.
        """
        return cv2.getTrackbarPos('Threshold', self.window_name) / 100.0

    def get_opacity(self):
        """
        Get the current opacity value from the trackbar.
        Returns:
            float: Current opacity setting as a fraction of the maximum value.
        """
        return cv2.getTrackbarPos('Opacity', self.window_name) / 100.0

    def get_focus_shift(self):
        """
        Get the current focus shift value from the trackbar.
        Returns:
            float: Current focus shift setting, adjusted by a constant value.
        """
        return 10 + cv2.getTrackbarPos('Focus Shift', self.window_name) / 100.0

    def get_target_hue(self):
        """
        Get the current target hue value from the trackbar.
        Returns:
            int: Current target hue setting.
        """
        return cv2.getTrackbarPos('Target Hue', self.window_name)

    def get_hue_tolerance(self):
        """
        Get the current hue tolerance value from the trackbar.
        Returns:
            int: Current hue tolerance setting.
        """
        return cv2.getTrackbarPos('Hue Tolerance', self.window_name)


    