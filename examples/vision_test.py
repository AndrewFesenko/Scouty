"""
Simple example: Camera and person tracking test.
"""

from vision.camera import Camera
from vision.tracker import PersonTracker
import cv2


def main():
    """Test camera and person tracking."""
    print("Starting camera and tracker test...")
    
    # Initialize components
    camera = Camera(camera_id=0)
    tracker = PersonTracker()
    
    # Open camera
    if not camera.open():
        print("Error: Could not open camera")
        return
    
    print("Camera opened. Press 'q' to quit.")
    
    try:
        while True:
            # Read frame
            success, frame = camera.read()
            if not success:
                print("Failed to read frame")
                break
            
            # Track person
            tracking_info = tracker.track(frame)
            
            # Draw tracking visualization
            output = tracker.draw_tracking(frame, tracking_info)
            
            # Display status
            if tracking_info['detected']:
                status = "TRACKING"
                color = (0, 255, 0)
            else:
                status = "NO TARGET"
                color = (0, 0, 255)
            
            cv2.putText(output, status, (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            
            # Show frame
            cv2.imshow('Scouty Vision Test', output)
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        camera.close()
        tracker.close()
        cv2.destroyAllWindows()
        print("Test completed")


if __name__ == '__main__':
    main()
