from requests_html import HTMLSession, Element
from tenacity import retry, RetryError, stop_after_attempt, wait_exponential
from typing import Optional

# originally by Lev Kochergin


def ck_prices(ck_url: str) -> dict[str, dict[str, float]]:
    """
    Finds the prices off of cardkingdom.com and returns them as a
    dictionary like this.

    {
        "nm": {"amount": 8, "price": 0.99},
        "lp": {"amount": 8, "price": 0.79},
        "mp": {"amount": 5, "price": 0.59},
        "hp": {"amount": 0, "price": 0.39},
    }
    """

    session = HTMLSession()  # start a html web session
    conditions: tuple[str] = ('nm', 'lp', 'mp', 'hp')

    # this decorator says that we will try to get data from cardkingdom up
    # to six times, and it will wait exponentially up to five seconds
    # between requests.
    @retry(stop=stop_after_attempt(6), wait=wait_exponential(max=5))
    def get_elements(session: HTMLSession) -> list[Element]:
        """helper function for retrying searching up the card page.
        returns four elements: one for each condition of the card asked for."""
        with session:
            r = session.get(ck_url)
        # this is the CSS selector for prices
        elements: list[Element] = r.html.find('.amtAndPrice')
        if elements:
            return elements
        # if no cards were found, then tenacity will retry searching
        # up the page and finding the card elements by raising Exception
        raise Exception

    try:
        elements = get_elements(session)
    except RetryError:
        return {}

    final_prices: dict[str, dict[str, float]] = {}

    for (condition, element) in zip(conditions, elements):
        # we need to chop off the $ at the beginning of the price
        find = element.find('.stylePrice', first=True)
        price = float(find.text[1:])

        # will not have a div there if there are none avaliable
        find: Optional[Element] = element.find('.styleQty', first=True)
        num = 0 if not find else int(find.text)

        final_prices[condition] = {'amount': num, 'price': price}

    return final_prices

#ck_prices('https://www.cardkingdom.com/mtg/fifth-dawn/avarice-totem')