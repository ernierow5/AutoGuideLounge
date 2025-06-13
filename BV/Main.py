import subprocess
import time
import sys

# Install screeninfo library: pip install screeninfo
try:
    from screeninfo import get_monitors
except ImportError:
    print("The 'screeninfo' library is not installed.")
    print("Please install it by running: pip install screeninfo")
    sys.exit(1)

def open_chrome_on_monitor(url, monitor_index, headless=False):
    """
    Opens a Chrome window with the specified URL on a particular monitor in kiosk mode.

    Args:
        url (str): The URL to open.
        monitor_index (int): The index of the monitor (0-based) to open the window on.
        headless (bool): If True, runs Chrome in headless mode (no UI).
                         This is generally not desired for multi-monitor display.
    """
    monitors = get_monitors()

    if monitor_index >= len(monitors):
        print(f"Error: Monitor index {monitor_index} is out of bounds. You only have {len(monitors)} monitors.")
        print("Please check your monitor setup or adjust the monitor_index values.")
        return

    monitor = monitors[monitor_index]
    print(f"Attempting to open Chrome on Monitor {monitor_index + 1}:")
    print(f"  Geometry: X={monitor.x}, Y={monitor.y}, Width={monitor.width}, Height={monitor.height}")

    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" # Default Chrome path

    # You might need to adjust the chrome_path if Chrome is installed elsewhere.
    # Common alternative paths:
    # "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    # Or, if Chrome is in your PATH, you might just use "chrome.exe"

    # Command-line arguments for Chrome
    # --new-window: Ensures a new window is opened, not a new tab in an existing window.
    # --kiosk: Opens Chrome in true full-screen mode without browser UI.
    # --window-position: Sets the initial X,Y coordinates of the window.
    # --window-size: Sets the initial width,height of the window.
    # --app=url: Can be used instead of just URL for a more "app-like" experience without address bar etc.
    #            However, --kiosk generally overrides much of the UI anyway.
    
    command = [
        chrome_path,
        f"--new-window",
        f"--window-position={monitor.x},{monitor.y}",
        f"--window-size={monitor.width},{monitor.height}",
        f"--kiosk", # This enables true full-screen, hiding browser UI.
        url
    ]

    if headless:
        command.insert(1, "--headless") # Add headless mode if requested

    try:
        # Use Popen to launch Chrome without waiting for it to close
        subprocess.Popen(command)
        print(f"Successfully launched Chrome for '{url}' on Monitor {monitor_index + 1}.")
    except FileNotFoundError:
        print(f"Error: Chrome not found at '{chrome_path}'.")
        print("Please ensure Chrome is installed or update the 'chrome_path' variable in the script.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Define the URLs you want to open on each monitor
    # IMPORTANT: Replace these with your desired URLs.
    urls_to_open = [
        "https://dashboard.ventrata.com/en/account/suppliers/2f0a03fe-2124-4a06-980d-88d2fc9f1ae1/bookings/availability?days=1&manifest=9fec6468-a894-4e74-b102-d1d816da99e8",
        "https://dashboard.ventrata.com/en/account/suppliers/2f0a03fe-2124-4a06-980d-88d2fc9f1ae1/bookings/availability?days=1&manifest=260aff74-d3de-48d6-98dd-ce7c3316c2b4",
        "https://dashboard.ventrata.com/en/account/suppliers/2f0a03fe-2124-4a06-980d-88d2fc9f1ae1/bookings/availability?days=7&manifest=d2bbb406-1dff-4652-9bbc-081838e9e91b"
    ]

    # Ensure you have enough monitors for the URLs you want to open.
    # The script will try to open url_to_open[0] on monitor 0, url_to_open[1] on monitor 1, etc.
    monitors_available = len(get_monitors())
    print(f"Detected {monitors_available} monitor(s).")

    if len(urls_to_open) > monitors_available:
        print("\nWarning: You have more URLs to open than detected monitors.")
        print("Some URLs might not open on a dedicated monitor.")
        print("Please ensure you have at least 3 monitors connected and active.")

    print(f"\nProcessing URL: {urls_to_open[0]} for Monitor Index: {0}")
    open_chrome_on_monitor(urls_to_open[0], 0)