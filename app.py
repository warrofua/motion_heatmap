import cv2
import traceback
from file_dialog import select_video_file
from stabilizer import Stabilizer
from color_analysis import HeatmapGenerator
from video_cropper import VideoCropper
from heatmap_settings import HeatmapSettings
from error_handling import ErrorHandler
from performance_monitoring import PerformanceMonitor

# File dialog to select the video file
video_path = select_video_file()
if not video_path:
    print("No file selected.")
    exit()

# Initialize the stabilizer, error handler, video cropper, and HeatmapGenerator
stabilizer = Stabilizer()
error_handler = ErrorHandler()
video_cropper = VideoCropper(video_path)
performance_monitor = PerformanceMonitor()

# Create the window for initializing HeatmapSettings
window_name = 'Frame with Heatmap Overlay'
cv2.namedWindow(window_name)
cv2.waitKey(100)  # Short delay
heatmap_settings = HeatmapSettings(window_name)

# Define the buffer size and initialize HeatmapGenerator with default or user-defined settings
buffer_size = 10  # Example buffer size
threshold = heatmap_settings.get_threshold()
opacity = heatmap_settings.get_opacity()  # Opacity might be set later
focus_shift = heatmap_settings.get_focus_shift()
target_hue = heatmap_settings.get_target_hue()
hue_tolerance = heatmap_settings.get_hue_tolerance()
heatmap_generator = HeatmapGenerator(buffer_size, threshold, focus_shift, target_hue, hue_tolerance)

# Select ROI using VideoCropper
roi = video_cropper.select_roi()

# Check if ROI is valid
if video_cropper.valid_roi:
    # Reset the video capture to the start
    video_cropper.reset_video()

    performance_monitor.start_timer()

    # Main processing loop
    while True:
        try:
            ret, frame = video_cropper.cap.read()
            error_handler.check_frame_read(ret, frame)
            if not ret:
                break

            # Crop and stabilize the frame
            cropped_frame = video_cropper.crop_frame(frame)
            stabilized_frame = stabilizer.stabilize_frame(cropped_frame)

            # Add the stabilized frame to the HeatmapGenerator
            heatmap_generator.add_frame(stabilized_frame)

            # Get current settings from trackbars
            threshold = heatmap_settings.get_threshold()
            opacity = heatmap_settings.get_opacity()
            focus_shift = heatmap_settings.get_focus_shift()
            target_hue = heatmap_settings.get_target_hue()
            hue_tolerance = heatmap_settings.get_hue_tolerance()

            # Update HeatmapGenerator settings if needed
            heatmap_generator.threshold = threshold
            heatmap_generator.focus_shift = focus_shift
            heatmap_generator.target_hue = target_hue
            heatmap_generator.hue_tolerance = hue_tolerance

            # Generate heatmap with current settings
            heatmap = heatmap_generator.create_heatmap(stabilized_frame)

            # Overlay heatmap on the cropped frame with current opacity
            overlayed_frame = cv2.addWeighted(cropped_frame, 1 - opacity, heatmap, opacity, 0)

            # Display the frame with heatmap overlay
            cv2.imshow(window_name, overlayed_frame)

            performance_monitor.record_frame_processed()

            # Break the loop on pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print("An error occurred during frame processing.")
            traceback.print_exc()  # Print detailed traceback
            break

    # Release resources
    video_cropper.cap.release()
    performance_monitor.report_performance()
    cv2.destroyAllWindows()
    
else:
    print("Invalid ROI selected.")
    video_cropper.cap.release()