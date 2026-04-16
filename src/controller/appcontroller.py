import threading
import pandas as pd
import os
from src.model.urlparser import UrlParser

class AppController:
    def __init__(self, model, view):
        self.model = model
        self.parser = UrlParser()
        self.view = view

        self.view.set_analyze_command(
            text_callback=self.analyze_text_threaded,
            url_callback=self.analyze_url_threaded,
            csv_callback=self.analyze_csv_threaded
        )

    def analyze_text_threaded(self, text):
        """
        Method triggering text analysis on a detached thread level.
        :param text: Text string provided by user
        """
        thread = threading.Thread(target=self._analyze_text_task, args=(text,))
        thread.start()

    def analyze_url_threaded(self, url):
        """
        Method triggering URL extraction and analysis on a detached background thread.
        :param url: URL string provided by user
        """
        thread = threading.Thread(target=self._analyze_url_task, args=(url,))
        thread.start()

    def analyze_csv_threaded(self, file_path, row_type):
        """
        Method starting long-term CSV modifications across an isolated thread loop.
        :param file_path: File system path to the target CSV document
        :param row_type: Parsing context (Text / URL) derived from interface combo box
        """
        thread = threading.Thread(target=self._analyze_csv_task, args=(file_path, row_type))
        thread.start()

    def _analyze_csv_task(self, file_path, row_type):
        """
        Method internally executing iterative logic parsing a bulk list of inquiries.
        :param file_path: File system path handling pandas integration
        :param row_type: Scope strategy directing row values
        """
        try:
            df = pd.read_csv(file_path)
            
            target_col = df.columns[0]
            if 'Headline' in df.columns:
                target_col = 'Headline'

            preds = []
            chances = []
            mediums = []
            
            for index, row in df.iterrows():
                content = str(row[target_col])
                
                try:
                    query = content
                    if "URL" in row_type:
                        title = self.parser.extract_title(content)
                        if title:
                            query = title
                        else:
                            query = ""

                    if not query.strip():
                        preds.append("ERROR")
                        chances.append(0.0)
                        mediums.append("ERROR")
                        continue

                    is_cb, percent, medium = self.model.analyze_headline(query)
                    preds.append(is_cb)
                    chances.append(percent)
                    mediums.append(medium)
                except Exception:
                    preds.append("ERROR")
                    chances.append(0.0)
                    mediums.append("ERROR")

            df['Is_Clickbait_Pred'] = preds
            df['Clickbait_Chance'] = chances
            df['Predicted_Outlet'] = mediums

            base, ext = os.path.splitext(file_path)
            out_file = f"{base}_analyzed{ext}"
            df.to_csv(out_file, index=False, encoding='utf-8-sig')
            
            filename = os.path.basename(out_file)
            self._update_view("csv", f"Successfully processed and exported to:\n{filename}", text_color="green")
            
        except Exception as e:
            self._update_view("csv", f"An error occurred while analyzing CSV: {e}", is_error=True)

    def _analyze_text_task(self, text):
        """
        Method calling the model layer sequentially evaluating a bare string.
        :param text: Text string passed in directly
        """
        try:
            is_clickbait, percent, medium = self.model.analyze_headline(text)
            status = "Not clickbait"
            if is_clickbait:
                status = "Clickbait"
            self._update_view("text", status, is_clickbait, percent, False, f"(chance: {percent}%) [Outlet: {medium}]")
        except Exception as e:
            self._update_view("text", f"Error: {e}", is_error=True)

    def _analyze_url_task(self, url):
        """
        Method scraping website HTML content and directing title tags into the model layer.
        :param url: HTTP or HTTPS link protocol reference
        """
        try:
            title = self.parser.extract_title(url)
            if not title:
                raise Exception("The URL link is unresponsive or malformed.")

            is_clickbait, percent, medium = self.model.analyze_headline(title)
            
            pfx = f"Title found: {title}\nResult: "
            status = "Not clickbait"
            if is_clickbait:
                status = "Clickbait"
            summary = pfx + status
            summary += f" (chance: {percent}%) [Outlet: {medium}]"
            
            self._update_view("url", summary, is_clickbait, percent, False)
        except Exception as e:
            self._update_view("url", f"Error: {e}", is_error=True)

    def _update_view(self, target, msg, is_clickbait=False, percent=None, is_error=False, extra_msg=None, text_color=None):
        """
        Method utilizing event queuing to bridge custom GUI updates back from async backgrounds.
        :param target: Scope identifier for specific labels
        :param msg: Output payload text
        :param is_clickbait: Success marker triggering red logic highlighting
        :param percent: Accompanying prediction index
        :param is_error: Error marker triggering orange layout
        :param extra_msg: Suffix string appended to the resulting notification banner
        :param text_color: Color string bypassing logic overrides
        """
        if extra_msg and not is_error:
             msg = f"{msg}  {extra_msg}"
             
        self.view.after(0, lambda: self.view.set_result(
            target=target,
            text=msg,
            is_clickbait=is_clickbait,
            percent=percent,
            is_error=is_error,
            text_color=text_color
        ))
