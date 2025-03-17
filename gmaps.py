@browser(
    data=["rechtsanwalt in muenster it-recht"],
)
def scrape_places_links(driver: AntiDetectDriver, query):

    # Visit Google Maps
    def visit_google_maps():
        encoded_query = urllib.parse.quote_plus(query)
        url = f'https://www.google.com/maps/search/{encoded_query}'
        driver.get(url)

        # Accept Cookies for European users
        if driver.is_in_page("https://consent.google.com/"):
            agree_button_selector = 'form:nth-child(2) > div > div > button'
            driver.click(agree_button_selector)
            driver.google_get(url)

    visit_google_maps()

# Visit an individual place and extract data
    def scrape_place_data():
        driver.get(link)
        
        # Accept Cookies for European users
        if driver.is_in_page("https://consent.google.com/"):
                agree_button_selector = 'form:nth-child(2) > div > div > button'
                driver.click(agree_button_selector)
                driver.get(link)

        # Extract title
        title_selector = 'h1'
        title = driver.text(title_selector)

        # Extract rating
        rating_selector = "div.F7nice > span"
        rating = driver.text(rating_selector)

        # Extract reviews count
        reviews_selector = "div.F7nice > span:last-child"
        reviews_text = driver.text(reviews_selector)
        reviews = int(''.join(filter(str.isdigit, reviews_text))) if reviews_text else None

        # Extract website link
        website_selector = "a[data-item-id='authority']"
        website = driver.link(website_selector)

        # Extract phone number
        phone_xpath = "//button[starts-with(@data-item-id,'phone')]"
        phone_element = driver.get_element_or_none(phone_xpath)
        phone = phone_element.get_attribute("data-item-id").replace("phone:tel:", "") if phone_element else None

        return {
            "title": title,
            "phone": phone,
            "website": website,
            "reviews": reviews,
            "rating": rating,
            "link": link,
        }