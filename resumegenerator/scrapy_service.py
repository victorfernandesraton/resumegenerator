from collections.abc import Iterable
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from resumegenerator.experience import Experience

USERNAME_XPATH = (
    "/html/body/main/section[1]/div/div/form[1]/div[1]/div[1]/div/div/input"
)
PASSWORD_XPATH = (
    "/html/body/main/section[1]/div/div/form[1]/div[1]/div[2]/div/div/input"
)
BUTTON_LOGIN_XPATH = "/html/body/main/section[1]/div/div/form[1]/div[2]/button"
PROFILE_LINK_XPATH = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/div/div[1]/div/a"
MODAL_CLOSE_XPATH = "/html/body/div[2]/div/div/section/button"

NOT_LOGGED = {
    "EXPERIENCE_BLOCK_XPATH": "/html/body/main/section[1]/div/section/section[4]/div/ul/li",
    "EXPERIENCE_ENTERPRISE": "div/h4/a",
    "HAS_SUBITEMS": "ul/li",
    "DURATION": "div/div/p[1]/span/span",
    "SUB_ENTERPRISE": "a/div/div[2]/h4",
    "SUB_DURATION": "a/div/div[2]/p",
}
LOGGED = {
    "EXPERIENCE_BLOCK_XPATH": "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[6]/div[3]/ul/li",
    "EXPERIENCE_ENTERPRISE": "div/div[2]/div[1]/div[1]/span[1]/span[1]",
    "HAS_SUBITEMS": "div/div[2]/div[2]/ul/li",
    "DURATION": "",
    "SUB_ENTERPRISE": "",
    "SUB_DURATION": "",
}


class ScrapyService:
    def __init__(self, driver: WebDriver, username: str, password: str | None) -> None:
        self.driver = driver
        self.username = username
        self.password = password

    @staticmethod
    def get_duration_in_years(duration_text: str) -> int:
        return 1 if duration_text.find("years") == -1 else int(duration_text[0])


    def get_experience_in_subitems(self,experience: WebElement)-> Experience:
        label_item = experience.find_element(
            By.XPATH, self.xpath["SUB_ENTERPRISE"]
        ).text
        duration_text = experience.find_element(
            By.XPATH, self.xpath["SUB_DURATION"]
        ).text
        duration = self.get_duration_in_years(duration_text)
        return Experience(enterprise=label_item, duration=duration)

    def get_experience_in_item(self, experience: WebElement)-> Experience:
            label_item = experience.find_element(
                By.XPATH, self.xpath["EXPERIENCE_ENTERPRISE"]
            ).text
            duration_text = experience.find_element(
                By.XPATH, self.xpath["DURATION"]
            ).text
            duration = self.get_duration_in_years(duration_text)
            return Experience(enterprise=label_item, duration=duration)


    def login(self):
        if not self.password:
            self.driver.get(f"http://linkedin.com/in/{self.username}")

        else:
            self.driver.get("https://linkedin.com")

            self.driver.implicitly_wait(0.5)

            text_input = self.driver.find_element(By.XPATH, USERNAME_XPATH)
            password_input = self.driver.find_element(By.XPATH, PASSWORD_XPATH)
            button_login = self.driver.find_element(By.XPATH, BUTTON_LOGIN_XPATH)

            text_input.send_keys(self.username)
            password_input.send_keys(self.password)
            button_login.click()

    def go_personal_page(self):
        if self.password:
            WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element(By.XPATH, PROFILE_LINK_XPATH)
            )

            button_go_profile = self.driver.find_element(By.XPATH, PROFILE_LINK_XPATH)
            button_go_profile.click()
        else:
            WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element(By.XPATH, MODAL_CLOSE_XPATH)
            )
            button_close_modal = self.driver.find_element(By.XPATH, MODAL_CLOSE_XPATH)
            button_close_modal.click()

    def get_experiences(self)-> Iterable[Experience]:
        result = []
        self.xpath = NOT_LOGGED if not self.password else LOGGED
        WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element(By.XPATH, self.xpath["EXPERIENCE_BLOCK_XPATH"])
        )
        list_experiences = self.driver.find_elements(
            By.XPATH, self.xpath["EXPERIENCE_BLOCK_XPATH"]
        )

        for experience in list_experiences:
            sub_experiences = experience.find_elements(
                By.XPATH, self.xpath["HAS_SUBITEMS"]
            )
            if len(sub_experiences) > 0:
                result.append(self.get_experience_in_subitems(experience))
            else:
                result.append(self.get_experience_in_item(experience))

        return result

    def quit(self):
        self.driver.quit()
