from typing import List, Dict, Union
from http.cookies import SimpleCookie
from sqlalchemy.orm import Session
import ScanRequestCookie
import ScanResponseCookie
import ScanRequestCookieAttribute
import ScanResponseCookieAttribute

def get_cookies_custom(
    headers: dict[str, str | list[str]], header_type: str
) -> list[dict[str, str]]:
    cookies = []

    cookie_header = headers.get(header_type, None)
    if not cookie_header:
        return cookies

    cookie_entries = (
        cookie_header if isinstance(cookie_header, list) else [cookie_header]
    )

    for cookie_entry in cookie_entries:
        attributes = cookie_entry.split("; ")
        cookie = {"name": "", "value": ""}

        name_value = attributes.pop(0).split("=", 1)
        cookie["name"] = name_value[0].strip()
        cookie["value"] = name_value[1].strip() if len(name_value) > 1 else ""

        # Extract and store additional attributes dynamically
        for attribute in attributes:
            key_value = attribute.split("=", 1)
            key = key_value[0].strip().lower()
            value = key_value[1] if len(key_value) > 1 else ""

            cookie[key] = value
        cookies.append(cookie)

    return cookies

def get_cookie(headers: Dict[str, Union[str, List[str]]], header_type: str) -> List[Dict[str, str]]:
    """
    Extracts cookies from the headers. Handles both 'Set-Cookie' and 'Cookie' header(s).
    
    Parameters:
    - headers: The headers dictionary containing either 'Set-Cookie' or 'Cookie'
    - header_type: Either 'Set-Cookie' or 'Cookie'
    
    Returns:
    - A list of dictionaries containing cookie attributes and values of the relevant header_type.
    """
    cookies = []
    cookie_header = headers.get(header_type, None)
    if not cookie_header:
        return cookies

    cookie_entries = cookie_header if isinstance(cookie_header, list) else [cookie_header]

    for entry in cookie_entries:
        parsed_cookie = SimpleCookie(entry)
        for morsel_name, morsel in parsed_cookie.items():
            cookie = {"name": morsel_name, "value": morsel.value}
            # Extract and store additional attributes dynamically
            for key in morsel.keys():
                if morsel[key]:
                    cookie[key.lower()] = morsel[key]
            cookies.append(cookie)
    return cookies

def get_or_create_response_cookie_attribute(dbs: Session, attribute_name: str) -> int:
    if attribute_name.lower() == "name":
        return None

    attribute = (
        dbs.query(models.ScanResponseCookieAttribute)
        .filter_by(attribute_name=attribute_name)
        .first()
    )
    if not attribute:
        attribute = models.ScanResponseCookieAttribute(attribute_name=attribute_name)
        dbs.add(attribute)
        dbs.commit()
        dbs.refresh(attribute)
    return attribute.id

def get_or_create_request_cookie_attribute(dbs: Session, attribute_name: str) -> int:
    if attribute_name.lower() == "name":
        return None

    attribute = (
        dbs.query(models.ScanRequestCookieAttribute)
        .filter_by(attribute_name=attribute_name)
        .first()
    )
    if not attribute:
        attribute = models.ScanRequestCookieAttribute(attribute_name=attribute_name)
        dbs.add(attribute)
        dbs.commit()
        dbs.refresh(attribute)
    return attribute.id

def get_scan_response_cookies(dbs: Session, cookies: List[Dict[str, str]], scan_item_id: int):
    for cookie_data in cookies:
        for key, value in cookie_data.items():
            attribute_id = get_or_create_response_cookie_attribute(dbs, key)
            if key == "name" or attribute_id is None:
                continue
            models.ScanResponseCookie.get_or_create(
                dbs,
                name=cookie_data["name"],
                value=value,
                attribute_id=attribute_id,
                scan_item_id=scan_item_id,
            )

def get_scan_request_cookies(dbs: Session, cookies: List[Dict[str, str]], scan_item_id: int):
    for cookie_data in cookies:
        for key, value in cookie_data.items():
            attribute_id = get_or_create_request_cookie_attribute(dbs, key)
            if key == "name" or attribute_id is None:
                continue
            models.ScanRequestCookie.get_or_create(
                dbs,
                name=cookie_data["name"],
                value=value,
                attribute_id=attribute_id,
                scan_item_id=scan_item_id,
            )

def main():
    # Sample headers with 'Set-Cookie' and 'Cookie' to display usage 
    headers = {
        "Set-Cookie": [
            "sessionid=123abc; Path=/; HttpOnly",
            "userid=456def; Secure; Path=/user",
        ],
        "Cookie": "sessionid=123abc; userid=456def"
    }

    # Simulate a database session
    dbs = Session()  
    
    scan_item_id = 1  

    # Extract and process response cookies
    response_cookies = get_cookies(headers, "Set-Cookie")
    print("Response Cookies:", response_cookies)
    get_scan_response_cookies(dbs, response_cookies, scan_item_id)

    # Extract and process request cookies
    request_cookies = get_cookies(headers, "Cookie")
    print("Request Cookies:", request_cookies)
    get_scan_request_cookies(dbs, request_cookies, scan_item_id)


if __name__ == "__main__":
    main()
