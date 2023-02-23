import tkinter as tk
import random

class DemoWindow:
    def __init__(self, master):
        self.master = master
        master.title("Demo Window")
		
        self.id_after_animate = None

        # Create the label and button
        self.color_label = tk.Label(master, text="Colours", font=("Arial", 20))
        self.color_label.pack()

        self.color_button = tk.Button(master, text="Click Me", command=self.open_top_level)
        self.color_button.pack()

        # Create a list of colors to use
        self.colors = ['red', 'green', 'blue', 'purple', 'orange', 'yellow']
		
        self.top_level = None
        self.label = None
        self.button = None

        # Start animating the label
        self.animate_label()

    def animate_label(self):
        print(f"animate")
        # Change the color of each letter in the label to a random color
        #new_text = ""
        #for letter in self.color_label.cget("text"):
        #    new_text += f"{{{{{random.choice(self.colors)}}}}}{letter}"
        self.color_label.config(foreground=random.choice(self.colors))
        
        # Call this function again after 100ms
        self.id_after_animate = self.master.after(100, self.animate_label)

    def open_top_level(self):
		
        if self.top_level is None:
		
            # Stop animating the label
            self.master.after_cancel(self.id_after_animate)
            
            # Create a top-level window
            self.top_level = tk.Toplevel(self.master)
            self.top_level.title("Top Level Window")
		    
            # Create a label and button in the top-level window
            self.label = tk.Label(self.top_level, text="This is a top-level window", font=("Arial", 20))
            self.label.pack()
		    
            #self.top_level.protocol("WM_DELETE_WINDOW", self.resume_animation)
            self.button = tk.Button(self.top_level, text="Close", command=self.close_top_level)
            self.button.pack()
		    
            # Override the destroy method of the top-level window
            #self.top_level.destroy = self.close_top_level
            self.top_level.protocol("WM_DELETE_WINDOW", self.close_top_level)
			
            self.color_button.config(command=None)

    def close_top_level(self):
        print(f"close_top_level")
        # Resume animating the label
        self.resume_animation()

        # Call the original destroy method to destroy the top-level window
        self.top_level.destroy()

        self.color_button.config(command=self.open_top_level)
        self.top_level = None

    def resume_animation(self):
        # Start animating the label again
        print(f"resume_animation")
        self.animate_label()

# Create the main window
root = tk.Tk()

# Create the demo window
demo = DemoWindow(root)

# Start the main loop
root.mainloop()
