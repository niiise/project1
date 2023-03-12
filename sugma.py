# Constants are uppercase, shouldn't change
HLTV_RESULTS_URL = "https://www.hltv.org/results"
QUERY = "?"
AND = "&"
STARS = "stars="  # syntax for stars filter
MAPS = "map="  # syntax for maps filter
START_DATE = "startDate="
END_DATE = "endDate="

# These are the parts of a URL, notice how ? and & are separators
# http://     domain.ext  /my/page.html  ?a=b&x=y&z=x
# ^ protocol  ^ domain    ^ path

# Version 1
# def get_hltv_results_url(stars: int, mapname: str) -> str:
#     return HLTV_RESULTS_URL + QUERY + STARS + str(stars) + "&" + MAPS + mapname

# Version 2
# def get_hltv_results_url(stars: int | None = None, mapname: str | None = None) -> str:
#     url = HLTV_RESULTS_URL
#     if stars is not None:
#         url = url + QUERY + STARS + str(stars)
#     if mapname is not None:
#         url = url + QUERY + MAPS + mapname
#     return url

# Version 3
# def get_hltv_results_url(stars: int | None = None, mapname: str | None = None) -> str:
#     # get the query items
#     query: list[str] = []  # add to list: query.append(...)
#     if stars is not None:
#         query.append(STARS + str(stars))
#     if mapname is not None:
#         query.append(MAPS + mapname)
#
#     # build the url
#     # if len(query) == 1:
#     #     QUERY
#     # if len(query) > 1:
#     #     QUERY AND
#
#     # query[0]  first element of list
#     # query[1:]  get all items from index 1 to the end
#     # len(query)  number of elements
#     #   0         1        2  (indices)
#     # [   1   ,    2 ,    3   ]  (items)
#     #             [2,   3]  [1:]  (slice)
#     # [:]  everything
#
#     url = HLTV_RESULTS_URL
#     if len(query) > 0:
#         url = url + QUERY + query[0]
#     if len(query) > 1:
#         for part in query[1:]:
#             url = url + AND + part
#         # for i in range(1, len(query)):
#         #     url = url + QUERY + query[i]
#
#     return url

# Version 4
# def get_hltv_results_url(stars: int | None = None, mapnames: list | None = None) -> str:
#     query: list[str] = []  # add to list: query.append(...)
#     if stars is not None:
#         query.append(STARS + str(stars))
#     if mapnames is not None:
#         # example: mapnames = ["de_mirage", "de_cache"]
#         for mapname in mapnames:
#             # example iteration 1: mapname = "de_mirage"
#             # example iteration 2: mapname = "de_cache"
#             query.append(MAPS + mapname)
#
#     # we want query to look like this:
#     # query = ["map=de_mirage", "map=de_cache"]
#
#     # Good, black box, don't have to look at this anymore
#     # If query is correct, this makes the right URL
#     url = HLTV_RESULTS_URL
#     if len(query) > 0:
#         url = url + QUERY + query[0]
#     if len(query) > 1:
#         for part in query[1:]:
#             url = url + AND + part
#
#     # we want url to look like this
#     # https://www.hltv.org/results?map=de_cache&map=de_mirage
#     return url


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


# print(get_hltv_results_url())
# print(get_hltv_results_url(stars=3))
# print(get_hltv_results_url(mapnames=["de_cache"]))
# print(get_hltv_results_url(stars=3, mapnames=["de_cache"]))
# print(get_hltv_results_url(stars=3, mapnames=[]))
#
# # https://www.hltv.org/results?stars=3&map=de_cache&map=de_mirage
# print(get_hltv_results_url(mapnames=["de_cache", "de_mirage"]))
# print(get_hltv_results_url(stars=3, mapnames=["de_cache", "de_mirage"], start_date="2022-02-22", end_date="2023-03-05"))
