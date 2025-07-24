import requests
import pandas as pd

RAPIDAPI_KEY = "4b38fd911dmsh0ef1ed5de02cff1p1c7613jsn43f872b0da18"

def buscar_vagas(query="data science", location="brazil", pages=1):
    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    params = {
        "query": query,
        "location": location,
        "page": 1,
        "num_pages": pages
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json().get("data", [])
        if not data:
            return pd.DataFrame()
        df = pd.DataFrame(data)
        return df[[
            "employer_name", "job_title", "job_city",
            "job_country", "job_posted_at_datetime_utc",
            "job_apply_link"
        ]]
    else:
        print("Erro:", response.status_code)
        return pd.DataFrame()

