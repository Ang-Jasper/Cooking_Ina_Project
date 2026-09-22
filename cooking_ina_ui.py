import customtkinter as ctk
import os 
from timer_audio import CookingTimer


class CookingInaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cooking Ina - Digital Cooking Assistant")
        self.root.geometry("650x520")
        
        # Rescaling Feature & Minimum Window Boundary
        self.root.resizable(True, True)
        self.root.minsize(550, 480)
        
        # Color Palette (Burnt Rust Theme)
        self.bg_color = "#9E472A"         # Deep rust background
        self.card_bg = "#B05638"          # Lighter clay shade for inner timer card
        self.primary_orange = "#C46849"   # Warm terracotta tone for main buttons
        self.hover_orange = "#D67A5B"     # Soft clay hover state
        self.text_light = "#FFFFFF"       # White text for contrast on dark background
        self.accent_green = "#4CAF50"     # Green for advancing to the next step
        
        self.root.configure(fg_color=self.bg_color)

        project_dir = os.path.dirname(os.path.abspath(__file__))
        audio_path = os.path.join(project_dir, "Bell.mp4")

        # Initialize Backend Timer (30 minutes = 1800 seconds)
        self.timer = CookingTimer(initial_seconds=5, alarm_filename=audio_path)

        self.setup_ui()
        self.update_timer_display()
        
    def setup_ui(self):
        # Main Container Frame
        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Top Section: Recipe & Step Info
        self.header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(10, 10))
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="Recipe: Adobo Placeholder", 
                                        font=("Helvetica", 22, "bold"), text_color=self.text_light)
        self.title_label.pack(pady=(0, 5))
        
        self.step_label = ctk.CTkLabel(self.header_frame, text="Step 1: Marinate the pork and chicken for 30 minutes.", 
                                       font=("Helvetica", 15), text_color=self.text_light, wraplength=500)
        self.step_label.pack(fill="x")
        
        # Middle Section: Centered Timer Bounding Box
        self.timer_box = ctk.CTkFrame(self.main_container, fg_color=self.card_bg, corner_radius=20)
        self.timer_box.pack(expand=True, pady=15)
        
        self.timer_label = ctk.CTkLabel(self.timer_box, text="30:00", 
                                        font=("Helvetica", 76, "bold"), text_color=self.text_light)
        self.timer_label.pack(padx=45, pady=15)
        
        # Bottom Section: Core Timer Controls
        self.controls_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.controls_frame.pack(pady=10)
        
        # Main Actions (Start, Pause, Extend)
        self.start_btn = ctk.CTkButton(self.controls_frame, text="Start", font=("Helvetica", 14, "bold"),
                                       fg_color=self.primary_orange, hover_color=self.hover_orange, 
                                       text_color=self.text_light, width=110, height=36, command=self.on_start)
        self.start_btn.grid(row=0, column=0, padx=8)
        
        self.pause_btn = ctk.CTkButton(self.controls_frame, text="Pause", font=("Helvetica", 14, "bold"),
                                       fg_color=self.primary_orange, hover_color=self.hover_orange, 
                                       text_color=self.text_light, width=110, height=36, command=self.on_pause)
        self.pause_btn.grid(row=0, column=1, padx=8)
        
        self.extend_btn = ctk.CTkButton(self.controls_frame, text="+1 Min", font=("Helvetica", 14, "bold"),
                                        fg_color=self.primary_orange, hover_color=self.hover_orange, 
                                        text_color=self.text_light, width=110, height=36, command=self.on_extend)
        self.extend_btn.grid(row=0, column=2, padx=8)
        
        # Footer Section: Navigation
        self.nav_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.nav_frame.pack(pady=(10, 5))
        
        self.repeat_btn = ctk.CTkButton(self.nav_frame, text="Repeat Step", font=("Helvetica", 13),
                                        fg_color="#8D8D8D", hover_color="#707070", 
                                        width=130, height=34, command=self.on_repeat)
        self.repeat_btn.grid(row=0, column=0, padx=10)
        
        self.next_btn = ctk.CTkButton(self.nav_frame, text="Next Step ->", font=("Helvetica", 13, "bold"),
                                      fg_color=self.accent_green, hover_color="#388E3C", 
                                      width=130, height=34, command=self.on_next_step)
        self.next_btn.grid(row=0, column=1, padx=10)

    def update_timer_display(self):
        """Fetches the formatted string from the timer module and updates the label."""
        self.timer_label.configure(text=self.timer.get_time_formatted())

    def tick(self):
        """The GUI loop that asks the timer to count down."""
        if self.timer.is_running:
            self.timer.decrement()
            self.update_timer_display()
            
            # Continue the loop every 1000ms if still running
            if self.timer.is_running:
                self.root.after(1000, self.tick)

    def on_start(self):
            # Only start the UI tick loop if the timer successfully started
            if not self.timer.is_running and self.timer.start():
                self.tick()
    
    def on_pause(self):
        self.timer.pause()
    
    def on_extend(self):
        self.timer.extend(60)
        self.update_timer_display()
    
    def on_repeat(self):
        self.timer.reset(1800)
        self.update_timer_display()
    
    def on_next_step(self):
        print("Backend hook: Load next step logic here")

if __name__ == "__main__":
    # Initialize the window
    ctk.set_appearance_mode("Light")
    root = ctk.CTk()
    app = CookingInaGUI(root)
    root.mainloop()