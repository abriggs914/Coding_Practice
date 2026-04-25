# # # AL - Alabama
# # # AK - Alaska
# # # AS - American Samoa
# # # AZ - Arizona
# # # AR - Arkansas
# # # CA - California
# # # CO - Colorado
# # # CT - Connecticut
# # # DE - Delaware
# # # DC - District of Columbia
# # # FM - Federated States of Micronesia
# # # FL - Florida
# # # GA - Georgia
# # # GU - Guam
# # # HI - Hawaii
# # # ID - Idaho
# # # IL - Illinois
# # # IN - Indiana
# # # IA - Iowa
# # # KS - Kansas
# # # KY - Kentucky
# # # LA - Louisiana
# # # ME - Maine
# # # MH - Marshall Islands
# # # MD - Maryland
# # # MA - Massachusetts
# # # MI - Michigan
# # # MN - Minnesota
# # # MS - Mississippi
# # # MO - Missouri
# # # MT - Montana
# # # NE - Nebraska
# # # NV - Nevada
# # # NH - New Hampshire
# # # NJ - New Jersey
# # # NM - New Mexico
# # # NY - New York
# # # NC - North Carolina
# # # ND - North Dakota
# # # MP - Northern Mariana Islands
# # # OH - Ohio
# # # OK - Oklahoma
# # # OR - Oregon
# # # PW - Palau
# # # PA - Pennsylvania
# # # PR - Puerto Rico
# # # RI - Rhode Island
# # # SC - South Carolina
# # # SD - South Dakota
# # # TN - Tennessee
# # # TX - Texas
# # # UT - Utah
# # # VT - Vermont
# # # VI - Virgin Islands
# # # VA - Virginia
# # # WA - Washington
# # # WV - West Virginia
# # # WI - Wisconsin
# # # WY - Wyoming
# # # AA - Armed Forces Americas
# # # AE - Armed Forces Africa
# # # AE - Armed Forces Canada
# # # AE - Armed Forces Europe
# # # AE - Armed Forces Middle East
# # # AP - Armed Forces Pacific


# # def type_and_blur(locator, value, page, delay=50):
# #     locator.click()
# #     locator.press("Control+A")
# #     locator.press("Backspace")
# #     locator.press_sequentially(str(value), delay=delay)
# #     page.keyboard.press("Tab")  # commit field via blur/tab    


# # def log_request(request):
# #     url = request.url.lower()
# #     if "usps" in url or "zip" in url or "lookup" in url or "address" in url:
# #         print("REQUEST:", request.method, request.url)
        
# # def log_response(response):
# #     url = response.url
# #     if "zipByAddress" in url or "/ADIB" in url or "anyapp_outage_apology" in url:
# #         print("RESPONSE:", response.status, response.url)
# #         try:
# #             ct = response.headers.get("content-type", "")
# #             print("CONTENT-TYPE:", ct)
# #             if "application/json" in ct:
# #                 print("BODY:", response.text())
# #             else:
# #                 text = response.text()
# #                 print("BODY:", text[:1000])
# #         except Exception as e:
# #             print("Could not read response body:", e)


# # from playwright.sync_api import sync_playwright, expect

# # def lookup(address=None, city=None, state=None, postal=None):

# #     address = str(address or "").title().strip().replace(".", "")
# #     city = str(city or "").title().strip()
# #     state = str(state or "").upper().strip()[:2]
# #     postal = str(postal or "").upper().strip()
    
# #     print(f"Lookup {address}, {city}, {state}, {postal}")

# #     with sync_playwright() as p:
# #         context = p.chromium.launch_persistent_context(
# #             user_data_dir=r"C:\temp\usps_profile",
# #             channel="chrome",
# #             headless=False,
# #         )
# #         page = context.pages[0] if context.pages else context.new_page()
# #         page = context.pages[0] if context.pages else context.new_page()
# #         page = context.new_page()
# #         page.on("request", log_request)
# #         page.on("response", log_response)

# #         page.goto("https://tools.usps.com/zip-code-lookup.htm?byaddress")

# #         addr = page.locator('input[name="tAddress"]')
# #         city_in = page.locator('input[name="tCity"]')
# #         state_sel = page.locator('select[name="tState"]')
# #         zip_in = page.locator('input[name="tZip-byaddress"]')
# #         submit = page.locator('#zip-by-address')

# #         expect(addr).to_be_visible()
# #         expect(city_in).to_be_visible()
# #         expect(state_sel).to_be_visible()
# #         expect(zip_in).to_be_visible()
# #         expect(submit).to_be_visible()

# #         # type_and_blur(addr, address, page)
# #         # type_and_blur(city_in, city, page)
        
# #         # state_sel.select_option(state)
# #         # page.keyboard.press("Tab")

# #         # type_and_blur(zip_in, postal, page)
# #         page.goto("https://tools.usps.com/zip-code-lookup.htm?byaddress")
# #         page.keyboard.press("Tab")
# #         page.keyboard.type("133 Springhill Ave", delay=120)
# #         page.keyboard.press("Tab")
# #         page.keyboard.type("Bowling Green", delay=120)
# #         page.keyboard.press("Tab")
# #         page.keyboard.press("K")
# #         page.keyboard.press("Y")
# #         page.keyboard.press("Tab")
# #         page.keyboard.type("42101", delay=120)
# #         page.keyboard.press("Tab")
# #         page.keyboard.press("Enter")

# #         # Small pause to allow any debounced validation to finish
# #         page.wait_for_timeout(2500)
        
# #         print("State value:", state_sel.input_value())
# #         print("Address aria-invalid:", addr.get_attribute("aria-invalid"))
# #         print("Address class:", addr.get_attribute("class"))
# #         print({
# #             "address": addr.input_value(),
# #             "city": city_in.input_value(),
# #             "state": state_sel.input_value(),
# #             "zip": zip_in.input_value(),
# #         })
        
# #         # page.pause()
# #         submit.click()
        
# #         # Wait for either success or failure text
# #         page.wait_for_timeout(5000)
# #         print("State value:", state_sel.input_value())
# #         print("Address aria-invalid:", addr.get_attribute("aria-invalid"))
# #         print("Address class:", addr.get_attribute("class"))
# #         print({
# #             "address": addr.input_value(),
# #             "city": city_in.input_value(),
# #             "state": state_sel.input_value(),
# #             "zip": zip_in.input_value(),
# #         })

# #         page_text = page.locator("body").inner_text().lower()

# #         if "edit and search again." in page_text:
# #             print("Found")
# #         elif "unfortunately, this information wasn't found." in page_text:
# #             print("Failure")
# #         else:
# #             print("Unknown")
# #             print(page.locator("body").inner_text())

# #         # browser.close()
# #         input()

    
# # lookup("133 Springhill ave", "bowling green", "ky", "42101")

# # # from playwright.sync_api import sync_playwright

# # # with sync_playwright() as p:
# # #     browser = p.chromium.launch(headless=False)
# # #     page = browser.new_page()
# # #     page.goto("https://tools.usps.com/zip-code-lookup.htm?byaddress")
# # #     page.reload()

# # #     page.fill('input[name="tAddress"]', "133 Springhill ave.")
# # #     page.fill('input[name="tCity"]', "bowling green")
# # #     page.select_option('select[name="tState"]', "KY")
# # #     page.fill('input[name="tZip-byaddress"]', "42101")

# # #     page.wait_for_timeout(50)
# # #     # Click the actual clickable element
# # #     page.click('#zip-by-address')

# # #     # page.wait_for_timeout(3000)
# # #     print(page.locator("body").inner_text())

# # #     # browser.close()



# #     # from playwright.sync_api import sync_playwright

# #     # with sync_playwright() as p:
# #     #     browser = p.chromium.launch(headless=False, slow_mo=300)
# #     #     page = browser.new_page()
# #     #     page.goto("https://tools.usps.com/zip-code-lookup.htm?byaddress", wait_until="domcontentloaded")

# #     #     # Let the page settle a bit
# #     #     page.wait_for_timeout(3000)

# #     #     # Print possible state-related elements
# #     #     print("SELECT COUNT:", page.locator("a").count())
# #     #     print("INPUT COUNT:", page.locator("a").count())

# #     #     for i in range(page.locator("a").count()):
# #     #         el = page.locator("a").nth(i)
# #     #         print("A", i, el.evaluate("""e => ({
# #     #             name: e.getAttribute('name'),
# #     #             id: e.getAttribute('id'),
# #     #             class: e.getAttribute('class'),
# #     #             aria: e.getAttribute('aria-label')
# #     #         })"""))

# #     #     page.pause()  # opens Playwright inspector


# import random
# from playwright.sync_api import sync_playwright, expect


# def expand_first_result(page):
#     first_result = page.locator('#zipByAddressDiv li.list-group-item.paginate').first
#     expect(first_result).to_be_visible(timeout=random.randint(4800, 6000))

#     # If details are not visible yet, click the row.
#     detail_area = first_result.locator('.address-detail-info-wrapper')
#     if not detail_area.is_visible():
#         first_result.click()
#         expect(detail_area).to_be_visible(timeout=random.randint(4500, 6000))

#     return first_result


# def get_dpv_confirmation_indicator(page):
#     first_result = expand_first_result(page)

#     # Find the heading block that contains the target label
#     dpv_heading = first_result.locator(
#         '.detail-heading-wrapper',
#         has_text='DPV CONFIRMATION INDICATOR'
#     ).first

#     expect(dpv_heading).to_be_visible(timeout=random.randint(4000, 6000))

#     # Move to the sibling value container and grab the text
#     dpv_value = dpv_heading.locator(
#         'xpath=following-sibling::*[contains(@class, "row-detail-wrapper")][1]//p'
#     ).inner_text().strip()

#     return dpv_value


# def active_el_info(page):
#     return page.evaluate("""
#         () => {
#             const el = document.activeElement;
#             if (!el) return null;
#             return {
#                 tag: el.tagName,
#                 name: el.getAttribute("name"),
#                 id: el.getAttribute("id"),
#                 type: el.getAttribute("type"),
#                 value: ("value" in el) ? el.value : null,
#                 text: (el.innerText || el.textContent || "").trim().slice(0, 80)
#             };
#         }
#     """)


# def print_active(page, label="ACTIVE"):
#     info = active_el_info(page)
#     print(f"{label}: {info}")


# def ensure_focus(page, selector, label=None):
#     loc = page.locator(selector)
#     expect(loc).to_be_visible()
#     loc.click()
#     page.wait_for_timeout(150)

#     info = active_el_info(page)
#     print_active(page, f"FOCUS AFTER CLICK [{label or selector}]")

#     name_ok = info and info.get("name") == loc.get_attribute("name")
#     id_ok = info and info.get("id") == loc.get_attribute("id")

#     if not (name_ok or id_ok):
#         raise RuntimeError(
#             f"Focus mismatch for {label or selector}. "
#             f"Expected selector={selector}, got active={info}"
#         )
#     return loc


# def clear_and_type_active(page, text, delay=None):
#     delay = random.randint(65, 100) if delay is None else delay
#     page.keyboard.press("Control+A")
#     page.keyboard.press("Backspace")
#     page.keyboard.type(str(text), delay=delay)


# def tab_and_expect(page, expected_name=None, expected_id=None, label=None, attempts=3):
#     for i in range(attempts):
#         page.keyboard.press("Tab")
#         page.wait_for_timeout(random.randint(100, 200))
#         info = active_el_info(page)
#         print_active(page, f"TAB RESULT [{label}] attempt {i + 1}")

#         if info is None:
#             continue

#         if expected_name and info.get("name") == expected_name:
#             return info
#         if expected_id and info.get("id") == expected_id:
#             return info

#     raise RuntimeError(
#         f"Did not land on expected field [{label}]. "
#         f"Expected name={expected_name}, id={expected_id}, got active={active_el_info(page)}"
#     )


# def select_state_by_keys(page, state_code, expected_name="tState", max_steps=70):
#     """
#     Assumes focus is already on the state <select>.
#     Uses Home then ArrowDown until the desired value is reached.
#     """
#     state_code = (state_code or "").upper().strip()[:2]

#     info = active_el_info(page)
#     if not info or info.get("name") != expected_name:
#         raise RuntimeError(f"State select is not focused. Active={info}")

#     # Reset to top of the select options
#     page.keyboard.press("Home")
#     page.wait_for_timeout(random.randint(100, 200))

#     # Walk downward until the selected value matches
#     for step in range(max_steps):
#         current_value = page.locator(f'select[name="{expected_name}"]').input_value()
#         # print(f"STATE STEP {step}: {current_value}")
#         if current_value == state_code:
#             return True
#         page.keyboard.press("ArrowDown")
#         page.wait_for_timeout(random.randint(60, 100))

#     raise RuntimeError(f"Could not select state {state_code} with arrow navigation.")


# def keyboard_nav_lookup(address=None, city=None, state=None, postal=None):
#     address = str(address or "").strip().replace(".", "")
#     city = str(city or "").strip()
#     state = str(state or "").upper().strip()[:2]
#     postal = str(postal or "").strip()

#     print(f"Lookup {address}, {city}, {state}, {postal}")

#     with sync_playwright() as p:
#         # context = p.chromium.launch_persistent_context(
#         #     user_data_dir=r"C:\temp\usps_profile",
#         #     channel="chrome",
#         #     headless=False,
#         # )
#         # page = context.pages[0] if context.pages else context.new_page()
#         # browser = p.chromium.launch(channel="chrome", headless=False)
#         browser = p.firefox.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()

#         page.goto(
#             "https://tools.usps.com/zip-code-lookup.htm?byaddress",
#             wait_until="domcontentloaded"
#         )

#         addr_sel = 'input[name="tAddress"]'
#         city_sel = 'input[name="tCity"]'
#         state_sel = 'select[name="tState"]'
#         zip_sel = 'input[name="tZip-byaddress"]'
#         find_sel = '#zip-by-address'

#         # Ensure the form is present
#         expect(page.locator(addr_sel)).to_be_visible()
#         expect(page.locator(city_sel)).to_be_visible()
#         expect(page.locator(state_sel)).to_be_visible()
#         expect(page.locator(zip_sel)).to_be_visible()
#         expect(page.locator(find_sel)).to_be_visible()

#         # 1) Focus address explicitly
#         ensure_focus(page, addr_sel, "Street Address")
#         clear_and_type_active(page, address, delay=random.randint(70, 120))

#         # 2) Tab to City and verify
#         tab_and_expect(page, expected_name="tCity", label="City")
#         clear_and_type_active(page, city, delay=random.randint(75, 125))

#         # 3) Tab to State and verify
#         tab_and_expect(page, expected_name="tState", label="State")
#         select_state_by_keys(page, state)

#         # 4) Tab to ZIP and verify
#         tab_and_expect(page, expected_name="tZip-byaddress", label="ZIP")
#         clear_and_type_active(page, postal, delay=random.randint(75, 125))

#         # 5) Tab until Find is focused
#         tab_and_expect(page, expected_id="zip-by-address", label="Find button")

#         print_active(page, "READY TO SUBMIT")
#         page.wait_for_timeout(random.randint(1000, 1500))
#         page.keyboard.press("Enter")

#         page.wait_for_timeout(random.randint(2500, 5000))

#         page_text = page.locator("body").inner_text().lower()

#         if "edit and search again." in page_text:
#             print("Found")
#             dpv = get_dpv_confirmation_indicator(page)
#             print("DPV CONFIRMATION INDICATOR:", dpv)
#         elif "unfortunately, this information wasn't found." in page_text:
#             print("Failure")
#         else:
#             print("Unknown")
#             print(page.locator("body").inner_text())

#         input("Press Enter to close...")
#         # context.close()
#         context.close()
#         browser.close()


# keyboard_nav_lookup("133 Springhill Ave", "Bowling Green", "KY", "42101")
# keyboard_nav_lookup("3713 Silver Oak Ct.", "Tulsa", "OK", "74107")

from playwright.sync_api import sync_playwright, expect
import random


SPEED_FACTOR = 2


def expand_first_result(page):
    first_result = page.locator('#zipByAddressDiv li.list-group-item.paginate').first
    expect(first_result).to_be_visible(timeout=int(SPEED_FACTOR * random.randint(4000, 7500)))

    detail_area = first_result.locator('.address-detail-info-wrapper')
    if not detail_area.is_visible():
        first_result.click()
        expect(detail_area).to_be_visible(timeout=int(SPEED_FACTOR * random.randint(4500, 7500)))

    return first_result


def get_dpv_confirmation_indicator(page):
    first_result = expand_first_result(page)

    dpv_heading = first_result.locator(
        '.detail-heading-wrapper',
        has_text='DPV CONFIRMATION INDICATOR'
    ).first

    expect(dpv_heading).to_be_visible(timeout=int(SPEED_FACTOR * random.randint(4500, 7500)))

    dpv_value = dpv_heading.locator(
        'xpath=following-sibling::*[contains(@class, "row-detail-wrapper")][1]//p'
    ).inner_text().strip()

    return dpv_value


def active_el_info(page):
    return page.evaluate("""
        () => {
            const el = document.activeElement;
            if (!el) return null;
            return {
                tag: el.tagName,
                name: el.getAttribute("name"),
                id: el.getAttribute("id"),
                type: el.getAttribute("type"),
                value: ("value" in el) ? el.value : null,
                text: (el.innerText || el.textContent || "").trim().slice(0, 80)
            };
        }
    """)


def ensure_focus(page, selector, label=None):
    loc = page.locator(selector)
    expect(loc).to_be_visible()
    loc.click()
    page.wait_for_timeout(int(SPEED_FACTOR * random.randint(80, 200)))

    info = active_el_info(page)
    name_ok = info and info.get("name") == loc.get_attribute("name")
    id_ok = info and info.get("id") == loc.get_attribute("id")

    if not (name_ok or id_ok):
        raise RuntimeError(
            f"Focus mismatch for {label or selector}. "
            f"Expected selector={selector}, got active={info}"
        )
    return loc


def clear_and_type_active(page, text, delay=None):
    delay = int(SPEED_FACTOR * random.randint(60, 200) if delay is None else delay)
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    page.keyboard.type(str(text), delay=delay)


def tab_and_expect(page, expected_name=None, expected_id=None, label=None, attempts=3):
    for _ in range(attempts):
        page.keyboard.press("Tab")
        page.wait_for_timeout(int(SPEED_FACTOR * random.randint(75, 300)))
        info = active_el_info(page)

        if info is None:
            continue
        if expected_name and info.get("name") == expected_name:
            return info
        if expected_id and info.get("id") == expected_id:
            return info

    raise RuntimeError(
        f"Did not land on expected field [{label}]. "
        f"Expected name={expected_name}, id={expected_id}, got active={active_el_info(page)}"
    )


def select_state_by_keys(page, state_code, expected_name="tState", max_steps=70):
    state_code = (state_code or "").upper().strip()[:2]

    info = active_el_info(page)
    if not info or info.get("name") != expected_name:
        raise RuntimeError(f"State select is not focused. Active={info}")

    page.keyboard.press("Home")
    page.wait_for_timeout(int(SPEED_FACTOR * random.randint(75, 400)))

    for _ in range(max_steps):
        current_value = page.locator(f'select[name="{expected_name}"]').input_value()
        if current_value == state_code:
            return True
        page.keyboard.press("ArrowDown")
        page.wait_for_timeout(int(SPEED_FACTOR * random.randint(50, 150)))

    raise RuntimeError(f"Could not select state {state_code} with arrow navigation.")


def lookup(addresses: list[dict | tuple]):
    
    def keyboard_nav_lookup(address=None, city=None, state=None, postal=None):
        address = str(address or "").strip().replace(".", "")
        city = str(city or "").strip()
        state = str(state or "").upper().strip()[:2]
        postal = str(postal or "").strip()

        print(f"Lookup {address}, {city}, {state}, {postal}")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            page.goto(
                "https://tools.usps.com/zip-code-lookup.htm?byaddress",
                wait_until="domcontentloaded"
            )

            addr_sel = 'input[name="tAddress"]'
            city_sel = 'input[name="tCity"]'
            state_sel = 'select[name="tState"]'
            zip_sel = 'input[name="tZip-byaddress"]'
            find_sel = '#zip-by-address'

            expect(page.locator(addr_sel)).to_be_visible()
            expect(page.locator(city_sel)).to_be_visible()
            expect(page.locator(state_sel)).to_be_visible()
            expect(page.locator(zip_sel)).to_be_visible()
            expect(page.locator(find_sel)).to_be_visible()

            ensure_focus(page, addr_sel, "Street Address")
            clear_and_type_active(page, address, delay=int(SPEED_FACTOR * random.randint(60, 200)))

            tab_and_expect(page, expected_name="tCity", label="City")
            clear_and_type_active(page, city, delay=int(SPEED_FACTOR * random.randint(60, 200)))

            tab_and_expect(page, expected_name="tState", label="State")
            select_state_by_keys(page, state)

            tab_and_expect(page, expected_name="tZip-byaddress", label="ZIP")
            clear_and_type_active(page, postal, delay=int(SPEED_FACTOR * random.randint(60, 200)))

            tab_and_expect(page, expected_id="zip-by-address", label="Find button")

            page.wait_for_timeout(int(SPEED_FACTOR * random.randint(1200, 2600)))
            page.keyboard.press("Enter")
            page.wait_for_timeout(int(SPEED_FACTOR * random.randint(2000, 4500)))

            page_text = page.locator("body").inner_text().lower()

            if "edit and search again." in page_text:
                print("Found")
                dpv = get_dpv_confirmation_indicator(page)
                print("DPV CONFIRMATION INDICATOR:", dpv)
            elif "unfortunately, this information wasn't found." in page_text:
                print("Failure")
            else:
                print("Unknown")
                print(page.locator("body").inner_text())

            input("Press Enter to close...")
            context.close()
            browser.close()
        page.wait_for_timeout(30000)

    for i, address_ in enumerate(addresses):
        if not isinstance(address_, dict):
            address_ = dict(zip(["address", "city", "state", "postal"], address_))
        keyboard_nav_lookup(**address_)


lookup([
    ("133 Springhill Ave", "Bowling Green", "KY", "42101"),
    ("3713 Silver Oak Ct.", "Tulsa", "OK", "74107")
])