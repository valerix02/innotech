import abc

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from .utils import rep_operation, download_geckodriver
from selenium.webdriver import Firefox
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options


class Scrapping(Firefox):

    def __init__(self, *args, **kwargs):
        path = download_geckodriver()
        if not path:
            raise ValueError("Failed download driver!")
        opts = Options()
        opts.headless = True
        super(Scrapping, self).__init__(
            firefox_binary=FirefoxBinary('/opt/firefox/firefox'),
            executable_path=path, *args, **kwargs,
            options=opts
        )
        self.selectors = {
            'class': self.find_element_by_class_name,
            'id': self.find_element_by_id,
            'xpath': self.find_element_by_xpath,
            'name': self.find_element_by_name
        }

    def find_element_by_xpath(self, xpath, rep_time=1, rep_count=10):
        return rep_operation(lambda: super(Scrapping, self).find_element_by_xpath(xpath), rep_time, rep_count)

    # def find_element(self, by, value, rep_time=1, rep_count=10):
    #     return rep_operation(lambda: super(Scrapping, self).find_element(by, value), rep_time, rep_count)

    def click(self, el, rep_time=1, rep_count=10):
        return rep_operation(lambda: el.click(), rep_time, rep_count)

    def click_js(self, selector, mouse_click=False):
        js = f'document.querySelector(`{selector}`)'
        if mouse_click:
            js = f"""
                    var simulateClick = function (elem) {{
                        // Create our event (with options)
                        var evt = new MouseEvent('click', {{
                            bubbles: true,
                            cancelable: true,
                            view: window
                        }});
                        // If cancelled, don't dispatch our event
                        var canceled = !elem.dispatchEvent(evt);
                    }};
                    simulateClick({js})
                """
        else:
            js = f'{js}.click()'
        return self.execute_script(js)

    def scroll_to_element(self, el):
        return self.execute_script('arguments[0].scrollIntoView(true);', el)

    def until(self, timeout, method, message=''):
        return WebDriverWait(self, timeout).until(method, message)

    @abc.abstractmethod
    def invoke(self, url):
        pass
