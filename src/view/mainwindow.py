import customtkinter as ctk
from customtkinter import filedialog
from src.model.targetfile import TargetFile
import os

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Clickbait Analyzer")
        self.geometry("600x400")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frames = {}
        
        self._analyze_text_callback = None
        self._analyze_url_callback = None
        self._analyze_csv_callback = None

        self._setup_menu_frame()
        self._setup_text_frame()
        self._setup_url_frame()
        self._setup_csv_frame()

        self._show_frame("menu_frame")

    def _show_frame(self, frame_name):
        """
        Method to switch visibility to a targeted frame layout.
        :param frame_name: String identifier of the target frame
        """
        for name, frame in self.frames.items():
            frame.grid_forget()
        self.frames[frame_name].grid(row=0, column=0, sticky="nsew")

    def _setup_menu_frame(self):
        """
        Method to instantiate and lay out the main menu frame.
        """
        frame = ctk.CTkFrame(self)
        frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(frame, text="Clickbait Analyzer", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=(50, 30))

        btn_text = ctk.CTkButton(frame, text="Text input", height=50, font=ctk.CTkFont(size=16),
                                 command=lambda: self._show_frame("text_frame"))
        btn_text.grid(row=1, column=0, padx=40, pady=10, sticky="ew")

        btn_url = ctk.CTkButton(frame, text="URL address", height=50, font=ctk.CTkFont(size=16),
                                command=lambda: self._show_frame("url_frame"))
        btn_url.grid(row=2, column=0, padx=40, pady=10, sticky="ew")

        btn_csv = ctk.CTkButton(frame, text="CSV Batch Processor", height=50, font=ctk.CTkFont(size=16),
                                command=lambda: self._show_frame("csv_frame"))
        btn_csv.grid(row=3, column=0, padx=40, pady=10, sticky="ew")

        self.frames["menu_frame"] = frame

    def _setup_text_frame(self):
        """
        Method to instantiate and lay out the text analysis frame.
        """
        frame = ctk.CTkFrame(self)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        title_label = ctk.CTkLabel(frame, text="Text Analyzer", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.text_input = ctk.CTkTextbox(frame, height=150, font=ctk.CTkFont(size=14))
        self.text_input.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.text_input.insert("0.0", "Enter text to analyze...")
        self.text_input.bind("<FocusIn>", lambda e: self.text_input.delete("0.0", "end") if self.text_input.get("0.0", "end-1c") == "Enter text to analyze..." else None)

        btn_analyze = ctk.CTkButton(frame, text="Analyze Text", font=ctk.CTkFont(size=16, weight="bold"), height=40,
                                    command=lambda: self._on_analyze_click("text"))
        btn_analyze.grid(row=2, column=0, padx=20, pady=10)

        self.text_result_label = ctk.CTkLabel(frame, text="Result will be displayed here.", font=ctk.CTkFont(size=16), text_color="gray")
        self.text_result_label.grid(row=3, column=0, padx=20, pady=10)

        btn_back = ctk.CTkButton(frame, text="Back to menu", fg_color="gray", hover_color="darkgray",
                                 command=lambda: self._show_frame("menu_frame"))
        btn_back.grid(row=4, column=0, padx=20, pady=(0, 20))

        self.frames["text_frame"] = frame

    def _setup_url_frame(self):
        """
        Method to instantiate and lay out the URL analysis frame.
        """
        frame = ctk.CTkFrame(self)
        frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(frame, text="URL Analyzer", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.url_input = ctk.CTkEntry(frame, placeholder_text="Enter http:// or https://...", font=ctk.CTkFont(size=14), height=40)
        self.url_input.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        btn_analyze = ctk.CTkButton(frame, text="Analyze URL", font=ctk.CTkFont(size=16, weight="bold"), height=40,
                                    command=lambda: self._on_analyze_click("url"))
        btn_analyze.grid(row=2, column=0, padx=20, pady=10)

        self.url_result_label = ctk.CTkLabel(frame, text="Result will be displayed here.", font=ctk.CTkFont(size=16), text_color="gray")
        self.url_result_label.grid(row=3, column=0, padx=20, pady=10)

        btn_back = ctk.CTkButton(frame, text="Back to menu", fg_color="gray", hover_color="darkgray",
                                 command=lambda: self._show_frame("menu_frame"))
        btn_back.grid(row=4, column=0, padx=20, pady=(0, 20))

        self.frames["url_frame"] = frame

    def _setup_csv_frame(self):
        """
        Method to instantiate and lay out the CSV batch processing frame.
        """
        frame = ctk.CTkFrame(self)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(4, weight=1)
        
        content_frame = ctk.CTkFrame(frame, fg_color="transparent")
        content_frame.grid(row=1, column=0, padx=20, pady=20, sticky="n")
        content_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(content_frame, text="Batch CSV Analyzer", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=(0, 20))

        controls_frame = ctk.CTkFrame(content_frame)
        controls_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=1)
        combo_label = ctk.CTkLabel(controls_frame, text="Data Type:", font=ctk.CTkFont(size=14, weight="bold"))
        combo_label.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="e")
        
        self.csv_type_combobox = ctk.CTkComboBox(controls_frame, values=["Items are text", "Items are URL links"], font=ctk.CTkFont(size=14), width=180)
        self.csv_type_combobox.grid(row=0, column=1, padx=(10, 20), pady=(20, 10), sticky="w")

        file_label = ctk.CTkLabel(controls_frame, text="Target CSV:", font=ctk.CTkFont(size=14, weight="bold"))
        file_label.grid(row=1, column=0, padx=(20, 10), pady=(10, 20), sticky="e")
        
        file_action_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        file_action_frame.grid(row=1, column=1, padx=(10, 20), pady=(10, 20), sticky="w")

        btn_select = ctk.CTkButton(file_action_frame, text="Browse...", width=80, command=self._pick_csv_file)
        btn_select.grid(row=0, column=0, padx=(0, 10))

        self.csv_file_label = ctk.CTkLabel(file_action_frame, text="No file selected", font=ctk.CTkFont(size=13, slant="italic"), text_color="gray")
        self.csv_file_label.grid(row=0, column=1, sticky="w")
        
        self.selected_csv_path = None

        btn_analyze = ctk.CTkButton(content_frame, text="Start Batch Analyze", font=ctk.CTkFont(size=16, weight="bold"), height=45, width=220,
                                    command=lambda: self._on_analyze_click("csv"))
        btn_analyze.grid(row=2, column=0, padx=20, pady=(20, 10))

        self.csv_result_label = ctk.CTkLabel(content_frame, text='', font=ctk.CTkFont(size=14), text_color="gray")
        self.csv_result_label.grid(row=3, column=0, padx=20, pady=(0, 10))

        btn_back = ctk.CTkButton(frame, text="Back to menu", fg_color="gray", hover_color="darkgray", width=120,
                                 command=lambda: self._show_frame("menu_frame"))
        btn_back.grid(row=5, column=0, padx=20, pady=(0, 20))

        self.frames["csv_frame"] = frame

    def _pick_csv_file(self):
        """
        Method invoking a native file dialog for robust CSV target file selection.
        Handles instantiation via a secure utility validation wrapper.
        """
        from pathlib import Path
        try:
            initial_dir = Path.home() / "Downloads"
            filepath = filedialog.askopenfilename(initialdir=initial_dir, title="Select CSV file", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
            
            if not filepath:
                return

            target = TargetFile(filepath)
            
            self.selected_csv_path = target.get_target_file
            self.csv_file_label.configure(text=os.path.basename(self.selected_csv_path))

            self.set_result("csv", "")
            
        except TypeError as e:
            self.set_result("csv", f"TypeError: {e}", is_error=True)
        except FileNotFoundError as e:
            self.set_result("csv", f"File Error: {e}", is_error=True)
        except PermissionError as e:
            self.set_result("csv", f"Permission: {e}", is_error=True)
        except OSError as e:
            self.set_result("csv", f"OS Error: {e}", is_error=True)
        except Exception as e:
            self.set_result("csv", f"Value Error: {e}", is_error=True)

    def set_analyze_command(self, text_callback, url_callback, csv_callback):
        """
        Method injecting callback bindings supplied externally by the application Controller.
        :param text_callback: Execution callback for single text processing
        :param url_callback: Execution callback for fetching and scraping URLs
        :param csv_callback: Execution callback for batch dataset migrations
        """
        self._analyze_text_callback = text_callback
        self._analyze_url_callback = url_callback
        self._analyze_csv_callback = csv_callback

    def _on_analyze_click(self, input_type):
        """
        Method routing dynamic payload content from current active user inputs to designated execution callbacks.
        :param input_type: Designates originating frame identifier
        """
        if input_type == "text" and self._analyze_text_callback:
            text = self.text_input.get("0.0", "end-1c").strip()
            if text and text != "Enter text to analyze...":
                self.set_result("text", "Processing...", text_color="gray")
                self._analyze_text_callback(text)
            else:
                self.set_result("text", "Please enter some text for analysis.", is_error=True)
                
        elif input_type == "url" and self._analyze_url_callback:
            url = self.url_input.get().strip()
            if url:
                self.set_result("url", "Downloading URL and processing (running in the background)....", text_color="gray")
                self._analyze_url_callback(url)
            else:
                self.set_result("url", "Please enter a URL link.", is_error=True)
                
        elif input_type == "csv" and self._analyze_csv_callback:
            if self.selected_csv_path:
                self.set_result("csv", "Evaluating and processing batch CSV...", text_color="gray")
                self._analyze_csv_callback(self.selected_csv_path, self.csv_type_combobox.get())
            else:
                self.set_result("csv", "No CSV file selected.", is_error=True)

    def set_result(self, target="text", text="", is_clickbait=False, percent=None, is_error=False, text_color=None):
        """
        Method safely updating respective result labels with colored typography denoting output statuses.
        :param target: Window specific scope identifier
        :param text: Payload string containing the result message
        :param is_clickbait: Boolean signifying predicted metric threshold
        :param percent: Unused probability indicator value
        :param is_error: Boolean flagging a faulty state triggering warning colors
        :param text_color: Specific bypass for typography mapping
        """
        if target == "text":
            label = self.text_result_label
        elif target == "url":
            label = self.url_result_label
        elif target == "csv":
            label = self.csv_result_label
        else:
            return

        label.configure(text=text)

        if text_color:
            label.configure(text_color=text_color)
        elif is_error:
            label.configure(text_color="orange")
        elif is_clickbait:
            label.configure(text_color="red")
        else:
            label.configure(text_color="green")
