from datetime import datetime, timedelta
from fake_useragent import UserAgent


import requests


def get_page(url: str, params: dict, headers: dict | None = None) -> dict:
    """
    Retrieves JSON from headhunter api

    Parameters
    ----------
    url: str
        URL of the requested page
    params: dict
        Query parameters
    headers: dict
        Optional headers for the request

    Returns
    -------
    JSON-like dict with vacancies
    """
    page = requests.get(url, params=params, headers=headers)
    page.raise_for_status()

    return page.json()


def process_data(url: str, params: dict, headers: dict | None = None) -> str:
    """
    Processes vacancies from dictionary

    Parameters
    ----------
    url: str
        URL of the requested page
    params: dict
        Query parameters
    headers: dict
        Optional headers for the request
    
    Returns
    -------
    Message string with vacancies
    """
    try:
        data = get_page(url, params, headers)
        vacancies = []
        for vacancy in data["items"]:
            if len(vacancy["name"]) > 30:
                name = vacancy["name"][:27] + '...'
            else:
                name = vacancy["name"]

            company = vacancy['employer']['name']
            vacancy_url = vacancy["alternate_url"]

            vacancies.append(f"{name} | {company} | {vacancy_url}")

        message = '\n'.join(vacancies)
    except requests.exceptions.HTTPError as e:
        error = e if len(str(e)) < 50 else str(e)[:47] + "..."
        message = f"Something went wrong: {error}"

    return message


if __name__ == '__main__':
    url: str = "https://api.hh.ru/vacancies"

    text: str = (
        "удаленно NAME:((analyst OR DWH OR ETL OR SQL) "
        "NOT business NOT системный NOT system NOT 1С "
        "NOT financial NOT финансовый NOT SOC NOT экономист)"
    )

    date_diff: datetime = datetime.now() - timedelta(minutes=10)
    date_from: str = date_diff.strftime("%Y-%m-%dT%H:%M")

    params: dict = {
        "text": text,
        "date_from": date_from,
        "per_page": 100
    }

    ua = UserAgent()
    headers = {"User-Agent": ua.random}

    print(process_data(url, params, headers))
