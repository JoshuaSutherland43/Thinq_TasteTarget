from frontend.layouts.generate_layout import GeneratePage
from frontend.layouts.analyze_layout import AnalyzePage

class PageController:
    @staticmethod
    def render_current_page(current_page, data):
        if current_page == "generate":
            GeneratePage.render()
        elif current_page == "analyze" and data:
            AnalyzePage.render(data)