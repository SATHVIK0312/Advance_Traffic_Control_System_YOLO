import cv2
import time
import threading
import yolov7_time_int  # Assuming this is the module that calculates green time using YOLOv7

# Function to capture snapshot from CCTV camera
def capture_snapshot(camera_index, snapshot_queue):
    cap = cv2.VideoCapture(camera_index)
    ret, frame = cap.read()
    if ret:
        snapshot_queue.put(frame)
    cap.release()

# Function to set signal to green for specified time
def set_signal_green(signal_index, green_time):
    print(f"Signal {signal_index} set to green for {green_time} seconds.")
    time.sleep(green_time)
    print(f"Signal {signal_index} set back to red.")

# Main function
def main():
    # List of CCTV camera indices
    camera_indices = [0, 1, 2, 3]

    # Queue to store snapshots
    snapshot_queue = queue.Queue()

    # Capture snapshots from each camera
    for index in camera_indices:
        thread = threading.Thread(target=capture_snapshot, args=(index, snapshot_queue))
        thread.start()

    # Wait for all threads to complete and collect snapshots
    time.sleep(3)  # Adjust based on camera initialization time
    snapshots = []
    while not snapshot_queue.empty():
        snapshots.append(snapshot_queue.get())

    # Calculate green time for each signal
    green_times = []
    for snapshot in snapshots:
        green_time = yolov7_time_int.calculate_green_time(snapshot)  # Assuming this function returns green time
        green_times.append(green_time)

    # Set signals to green for specified green times
    for i, green_time in enumerate(green_times):
        set_signal_green(i + 1, green_time)

if __name__ == "__main__":
    main()
