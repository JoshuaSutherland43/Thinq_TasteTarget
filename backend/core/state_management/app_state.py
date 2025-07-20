class AppState:
    def __init__(self, session_state):
        self.state = session_state

        if "current_page" not in self.state:
            self.state.current_page = "dashboard"
        if "generated_data" not in self.state:
            self.state.generated_data = None


def get_session_state(session_state):
    # Add any logic here if needed to set up defaults, logging, etc.
    if "initialized" not in session_state:
        session_state.initialized = True
