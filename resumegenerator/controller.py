from .scrapy_service import ScrapyService


class Controller:
    def __init__(self, scrapy: ScrapyService, company):
        self.scrapy = scrapy
        self.company = company
        self.experiences = []

    def get_local_experiences(self):
        pass

    def get_remote_experiences(self):
        try:
            self.scrapy.login()
            self.scrapy.go_personal_page()
            self.experiences = self.scrapy.get_experiences()
            for item in self.experiences:
                print(item.enterprise, item.duration)
        finally:
            self.scrapy.quit()
        
    def generate_resume(self):
        pass
