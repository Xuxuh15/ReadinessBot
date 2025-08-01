from form_handler import Form_Handler
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    ElementNotInteractableException,
    WebDriverException,
)




class FormRunner:

    def __init__(self, preset):
        self.handler = Form_Handler(preset)
        self.successful = False
        self.message = ''
        self.preset = preset

    def run(self):
        try:
            self.handler.launch_form()
            self.handler.handle_dropdown_list()
            self.handler.handle_sleep_score()
            self.handler.handle_mood_score()
            self.handler.handle_soreness_score()
            self.handler.handle_energy_score()
            self.handler.handle_performance_score()
            self.handler.handle_muscle_groups()
            self.handler.handle_comment_section()
            self.handler.submit_form()
            self.successful = True
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Element not found or timeout: {e}")
            self.message = f"{e}"
        except (ElementClickInterceptedException, ElementNotInteractableException) as e:
            print(f"Element interaction failed: {e}")
            self.message = f"{e}"
        except StaleElementReferenceException as e:
            print(f"Element went stale: {e}")
            self.message = f"{e}"
        except WebDriverException as e:
            print(f"WebDriver error: {e}")
            self.message = f"{e}"
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.message = f"{e}"
        finally:
            self.handler.exit_driver()
            self.message = f"Readiness Form submitted successfully with response: {self.preset}"

