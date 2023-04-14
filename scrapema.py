import sugma
import bs4
import requests
import datetime

# TODO: DATETIMEIFY THE RESULTS URL
# TODO: try doing this with different URLs to check it works
# TODO: try coming up with a URL that returns no results
class SeriesResult:
    def __init__(self, winner_name, loser_name, tournament_name, score_won, score_lost, series_type, stars_number, result_url, result_date):
        self.winner_name = winner_name
        self.loser_name = loser_name
        self.tournament_name = tournament_name
        self.score_won = score_won
        self.score_lost = score_lost
        self.series_type = series_type
        self.stars_number = stars_number
        self.result_url = result_url
        self.result_date = result_date

    def display(self):
        print("Tournament: " + self.tournament_name)
        print("Winner: " + self.winner_name + ", Loser: " + self.loser_name)
        print("Score: " + self.score_won + " - " + self.score_lost)
        print("Series Type: " + self.series_type)
        print("Number of Stars:" + str(self.stars_number))
        print("Match Page: " + self.result_url)
        print("Match Date: " + self.result_date)


def make_series_result_from_element(result_element, result_date) -> SeriesResult:
    team_elements = result_element.findChildren("div", {"class": "team"})
    for team_element in team_elements:  # element["class"]
        # print(team_element["class"])
        # from this we know this is a list: team_element["class"]
        # check if an element is in a list: "team-won" in team_element["class"]
        if "team-won" in team_element["class"]:
            winner_name = team_element.text
        else:
            loser_name = team_element.text

    tournament_name = result_element.findChild("span", {"class": "event-name"}).text
    score_won = result_element.findChild("span", {"class": "score-won"}).text
    score_lost = result_element.findChild("span", {"class": "score-lost"}).text
    series_type = result_element.findChild("div", {"class": "map-text"}).text
    stars_number = len(result_element.findChildren("i", {"class": "star"}))
    result_url = "https://hltv.org" + result_element.findChild("a", {"class": "a-reset"})["href"]

    series_result = SeriesResult(
        winner_name,
        loser_name,
        tournament_name,
        score_won,
        score_lost,
        series_type,
        stars_number,
        result_url,
        result_date,
    )
    return series_result


def get_results_for_url(url: str) -> list[SeriesResult]:
    series_results: list[SeriesResult] = []
    response = requests.get(url)  # downloads the hltv webpage source HTML
    soup = bs4.BeautifulSoup(response.content, features="html.parser")  # allows us to search the HTML

    # We noticed that all the results we want match this search
    all_search_results_element = soup.find("div", {"class": "allres"})  # Excludes featured results section at top

    # results_by_date_elements: [<div class="results-sublist">...</div>, <div class="results-sublist">...</div>, ...]
    # all results on the page returned by our search
    # Example in htmlma.html
    results_sublist_elements = all_search_results_element.findChildren("div", {"class": "results-sublist"})

    for results_sublist_element in results_sublist_elements:
        # TODO: get the date from this element

        # [<div class="result-con" ...>...</div>, ...]
        # corresponds to all matches that happened on a given day
        # for example, this could be NaVi-mouz and cloud9-g2 because they happened on the same day
        result_con_elements = results_sublist_element.findChildren("div", {"class": "result-con"})
        result_date = results_sublist_element.findChild(("span", "div"), {"class": "standard-headline"})
        result_date_text = result_date.text[len("Results for "):]

        # this element has our actual match results, e.g. team-won, score-won, etc.
        # it corresponds to an individual series
        for result_con_element in result_con_elements:
            series_result = make_series_result_from_element(result_con_element, result_date_text)
            series_results.append(series_result)

    return series_results


def main():
    url = sugma.get_hltv_results_url(
        stars=3,
        mapnames=["de_cache", "de_mirage"],
        start_date="2022-02-22",
        end_date="2023-03-05",
    )

    series_results = get_results_for_url(url)
    for series_result in series_results:
        series_result.display()
        print("----------------------")


if __name__ == "__main__":
    main()
