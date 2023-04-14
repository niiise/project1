HLTV_RESULTS_URL = "https://www.hltv.org/results"
QUERY = "?"
AND = "&"
STARS = "stars="
MAPS = "map="
START_DATE = "startDate="
END_DATE = "endDate="


def get_hltv_results_url(
    stars: int | None = None,
    mapnames: list[str] | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> str:
    query: list[str] = []
    if stars is not None:
        query.append(STARS + str(stars))
    if mapnames is not None:
        for mapname in mapnames:
            query.append(MAPS + mapname)
    if start_date is not None:
        query.append(START_DATE + start_date)
    if end_date is not None:
        query.append(END_DATE + end_date)

    url = HLTV_RESULTS_URL
    if len(query) > 0:
        url = url + QUERY + query[0]
    if len(query) > 1:
        for part in query[1:]:
            url = url + AND + part

    return url
