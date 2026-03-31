import customtkinter as ctk


class MainWindow(ctk.CTk):
    def __init__(self):
        """
        Constructor initializes and renders all graphical components of the main application window.
        Sets up the grid layout, title label, input textbox, analyze button, and result label.
        """
        super().__init__()

        self.title("Clickbait Analyzer")
        self.geometry("600x400")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text="Clickbait Headline Analyzer",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.input_textbox = ctk.CTkTextbox(self, height=150, font=ctk.CTkFont(size=14))
        self.input_textbox.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.input_textbox.insert("0.0", "Enter text to analyze...")

        self.input_textbox.bind("<FocusIn>", self._clear_placeholder)

        self.analyze_button = ctk.CTkButton(
            self,
            text="Analyze Clickbait",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40
        )
        self.analyze_button.grid(row=2, column=0, padx=20, pady=10)

        self.result_label = ctk.CTkLabel(
            self,
            text="Result will be displayed here.",
            font=ctk.CTkFont(size=18),
            text_color="gray"
        )
        self.result_label.grid(row=3, column=0, padx=20, pady=(10, 20))

        self._analyze_callback = None
        self._has_placeholder = True

    def _clear_placeholder(self, event):
        """
        Event handler that clears the placeholder text on first focus of the input textbox.
        :param event: tkinter FocusIn event object
        """
        if self._has_placeholder:
            self.input_textbox.delete("0.0", "end")
            self._has_placeholder = False

    def set_analyze_command(self, callback):
        """
        Binds an external callback function to the analyze button.
        Used by the Controller to inject its logic into this View.
        :param callback: callable that accepts a string (headline text)
        """
        self._analyze_callback = callback
        self.analyze_button.configure(command=self._on_analyze_click)

    def _on_analyze_click(self):
        """
        Internal handler triggered when the analyze button is clicked.
        Validates that the input textbox is not empty before calling the controller callback.
        """
        if self._analyze_callback:
            text = self.get_input_text()
            if text.strip() and not self._has_placeholder:
                self._analyze_callback(text)
            else:
                self.set_result("Prosím zadejte nějaký text k analýze.", is_error=True)

    def get_input_text(self):
        """
        Retrieves the current text content from the input textbox.
        :return: string with the user-entered headline text
        """
        return self.input_textbox.get("0.0", "end-1c")

    def set_result(self, text, is_clickbait=False, percent=None, is_error=False):
        """
        Updates the result label with the provided text and applies appropriate color coding.
        :param text: result message string to display
        :param is_clickbait: boolean flag indicating a clickbait prediction
        :param percent: float representing the prediction confidence (unused visually, reserved for future use)
        :param is_error: boolean flag used for displaying error messages in orange
        """
        self.result_label.configure(text=text)

        if is_error:
            self.result_label.configure(text_color="orange")
        elif is_clickbait:
            self.result_label.configure(text_color="red")
        else:
            self.result_label.configure(text_color="green")
