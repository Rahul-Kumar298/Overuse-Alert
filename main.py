import time
import os
import pygame
import tkinter as tk
import threading

# Global variables
interval_thread = None
running = True

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def play_reminder_music():
    pygame.mixer.init()
    pygame.mixer.music.load(r"D:\python\Project\Overuse Alert\Overuse-Alert\alert.mp3") 
    pygame.mixer.music.play()

def remind_later(root):
    root.destroy()  # Close the current message box
    # Set a timer to remind after ten minutes
    threading.Timer(600, show_popup).start()

def ok(root, interval_thread):
    global running
    root.destroy()  # Close the current message box
    global interval
    interval += 600  # Add ten minutes to the interval
    running = False  # Set the flag to stop the thread gracefully
    if interval_thread is not None:  # Check if the thread exists
        interval_thread.join()  # Wait for the thread to finish
    if running:  # Restart the timer with the updated interval if the program is still running
        Wdr(interval)  

def show_popup():
    root = tk.Tk()
    root.configure(background='aqua')
    root.withdraw()
    root.attributes("-topmost", True)
    
    # Create the custom window
    popup_window = tk.Toplevel(root)
    popup_window.title("JAVRIS")
    message = """It's time for a break! Remember, regular breaks are essential for productivity and well-being. Step away from your desk for 10 minutes, stretch, hydrate, or take a short walk. Your future self will thank you"""
    message_label = tk.Label(popup_window, text=message, wraplength=300)
    message_label.pack(pady=10)

    # Calculate position to place the custom window at the bottom right corner
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    popup_width = 350
    popup_height = 250
    x_pos = screen_width - popup_width
    y_pos = screen_height - popup_height
    popup_window.geometry(f"300x150+{x_pos}+{y_pos}")

    # Add "Remind Later" button
    remind_button = tk.Button(popup_window, text="Remind Later", command=lambda: remind_later(root))
    remind_button.pack(side=tk.LEFT, padx=10, pady=10)
    
    # Add "OK" button
    ok_button = tk.Button(popup_window, text="OK", command=lambda: ok(root, interval_thread))
    ok_button.pack(side=tk.RIGHT, padx=10, pady=10)

    root.mainloop()

def Wdr(interval):
    global interval_thread
    global running
    while running:
        clear_screen()
        music_thread = threading.Thread(target=play_reminder_music)
        popup_thread = threading.Thread(target=show_popup)
        music_thread.start()
        popup_thread.start()
        time.sleep(interval)  # Wait for the specified interval

if __name__ == "__main__":
    interval = 9000  # interval in seconds
    interval_thread = threading.Thread(target=Wdr, args=(interval,))
    interval_thread.start()

    # Wait for user input to exit
    input("Press Enter to exit...\n")

    # Set running flag to False to stop the threads gracefully
    running = False
