import plotly.graph_objs as go

class ChartBuilder:
    @staticmethod
    def build_interest_distribution(data):
        interests = {}
        for persona in data['personas']:
            for cat, val in persona['cultural_interests'].items():
                interests[cat] = interests.get(cat, 0) + len(val)

        return go.Figure(data=[go.Bar(x=list(interests.keys()), y=list(interests.values()), marker_color='black')])