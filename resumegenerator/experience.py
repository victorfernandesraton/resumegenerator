class Experience:
    def __init__(self, enterprise: str, duration, skills: list = []) -> None:
        self.enterprise = enterprise
        self.duration = duration
        self.skills = skills