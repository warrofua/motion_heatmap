import time
import os
import psutil

class PerformanceMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.frame_count = 0
        self.process = psutil.Process(os.getpid())
        self.initial_memory_use = self.process.memory_info().rss / 1024 ** 2  # Convert to MB

    def start_timer(self):
        self.start_time = time.time()

    def record_frame_processed(self):
        self.frame_count += 1

    def report_performance(self):
        elapsed_time = time.time() - self.start_time
        fps = self.frame_count / elapsed_time if elapsed_time > 0 else 0
        current_memory_use = self.process.memory_info().rss / 1024 ** 2  # Convert to MB
        memory_usage = current_memory_use - self.initial_memory_use
        cpu_usage = self.process.cpu_percent() / psutil.cpu_count()

        print(f"Processed {self.frame_count} frames in {elapsed_time:.2f} seconds ({fps:.2f} FPS)")
        print(f"Memory usage: {memory_usage:.2f} MB")
        print(f"Average CPU usage: {cpu_usage:.2f}%")

# Usage Example:
# from performance_monitoring import PerformanceMonitor
# performance_monitor = PerformanceMonitor()

# At the beginning of processing:
# performance_monitor.start_timer()

# In the main loop:
# performance_monitor.record_frame_processed()

# At the end of processing:
# performance_monitor.report_performance()