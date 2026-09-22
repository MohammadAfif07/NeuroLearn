class AccessibilityManager:
    def __init__(self):
        self.accessibility_profiles = {}
        self._setup_profiles()
    
    def _setup_profiles(self):
        self.accessibility_profiles = {
            "ADHD": self.get_adhd_accommodations,
            "Dyslexia": self.get_dyslexia_accommodations,
            "Autism Spectrum": self.get_autism_accommodations
        }
    
    def get_accommodations(self, profile):
        if profile in self.accessibility_profiles:
            return self.accessibility_profiles[profile]()
        return self.get_general_accommodations()
    
    def get_adhd_accommodations(self):
        return {
            "timer_breaks": True,
            "chunked_content": True,
            "visual_reminders": True
        }
    
    def get_dyslexia_accommodations(self):
        return {
            "dyslexia_font": True,
            "text_to_speech": True,
            "simplified_language": True
        }
    
    def get_autism_accommodations(self):
        return {
            "clear_routines": True,
            "literal_language": True,
            "visual_schedules": True
        }
    
    def get_general_accommodations(self):
        return {
            "flexible_timing": True,
            "multiple_formats": True
        }