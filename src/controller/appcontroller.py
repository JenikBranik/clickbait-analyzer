class AppController:
    def __init__(self, model, view):
        """
        Constructor initializes the controller with a reference to the Model and the View.
        Immediately registers the analyze callback within the View.
        :param model: instance of Clickbait, responsible for ML predictions
        :param view: instance of MainWindow, responsible for the GUI
        """
        self.model = model
        self.view = view

        self.view.set_analyze_command(self.analyze_text)

    def analyze_text(self, text):
        """
        Main controller method triggered by the View when the user requests analysis.
        Passes the input headline to the Model and forwards the prediction result back into the View.
        :param text: headline string provided by the user via the GUI input field
        :raises Exception: any model-side error is caught and forwarded to the View as an error message
        """
        try:
            self.view.set_result("Analyzing")
            self.view.update()

            is_clickbait, percent = self.model.analyze_headline(text)

            if is_clickbait:
                result_text = f"clickbait  (chance: {percent}%)"
            else:
                result_text = f"Not clickbait  (chance: {percent}%)"

            self.view.set_result(result_text, is_clickbait=is_clickbait, percent=percent)

        except Exception as e:
            self.view.set_result(f"Error: {e}", is_error=True)
