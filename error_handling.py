class ErrorHandler:
    def __init__(self):
        pass

    def check_frame_read(self, ret, frame):
        if not ret or frame is None:
            raise ValueError("Error reading frame from video.")

    def check_frame_cropping(self, frame, roi):
        if frame.shape[0] < roi[1] + roi[3] or frame.shape[1] < roi[0] + roi[2]:
            raise ValueError("ROI is out of frame bounds during cropping.")

    def handle_exception(self, e):
        # Custom handling of exceptions
        print(f"An error occurred: {e}")

# Usage Example:
# from error_handling import ErrorHandler
# error_handler = ErrorHandler()
# In the main loop:
# error_handler.check_frame_read(ret, frame)
# error_handler.check_frame_cropping(frame, roi)
# In an exception block:
# error_handler.handle_exception(e)