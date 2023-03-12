import sugma
import bs4
import requests


# TODO: try doing this with different URLs to check it works
# TODO: try coming up with a URL that returns no results
class SeriesResult:
    def __init__(self, winner_name, loser_name, tournament_name, score_won, score_lost, series_type, stars_number):
        self.winner_name = winner_name
        self.loser_name = loser_name
        self.tournament_name = tournament_name
        self.score_won = score_won
        self.score_lost = score_lost
        self.series_type = series_type
        self.stars_number = stars_number

    def display(self):
        print("Tournament: " + self.tournament_name)
        print("Winner: " + self.winner_name + ", Loser: " + self.loser_name)
        print("Score: " + self.score_won + " - " + self.score_lost)
        print("Series Type: " + self.series_type)
        print(str(self.stars_number) + " stars")


def get_results_for_url(url: str) -> list[SeriesResult]:
    series_results: list[SeriesResult] = []
    response = requests.get(url)  # downloads the hltv webpage source HTML
    soup = bs4.BeautifulSoup(response.content, features="html.parser")  # allows us to search the HTML

    # We noticed that all the results we want match this search
    result_elements = soup.find("div", {"class": "allres"}).findChildren("div", {"class": "result"})
    for result_element in result_elements:
        # get all elements <div> that have class="team", in this case Grayhound and 00NATION
        # list of two elements, <div class="team-won team">Grayhound</div> and <div class="team">00NATION</div>
        # elements_inside_our_result_that_are_probably_a_team_name
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

        series_result = SeriesResult(winner_name, loser_name, tournament_name, score_won, score_lost, series_type, stars_number)
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


main()

"""
<div class="result">  <----- tag is "div", element has {"class": "result"}
    <table>
        <tr>
            <td class="team-cell">
                <div class="line-align team1">
                    <div class="team-won team">Grayhound</div> <---- second search, children with tag div, class=team
                    <img alt="Grayhound" class="team-logo" src="https://img-cdn.hltv.org/teamlogo/IjyAECYg-7zLXJEUj-aRqa.svg?ixlib=java-2.1.0&amp;s=def9c53f5b91c85af4a5a0a6f2606d26" title="Grayhound"/>
                </div>
            </td>
            <td class="result-score">
                <span class="score-won">2</span> - <span class="score-lost">1</span>
            </td>
            <td class="team-cell">
                <div class="line-align team2">
                    <img alt="00NATION" class="team-logo" src="https://img-cdn.hltv.org/teamlogo/-LUi1MZwRXN6fQ_pbha7Ke.png?ixlib=java-2.1.0&amp;w=50&amp;s=c030a8759455d70338739d5643e39172" title="00NATION"/>
                    <div class="team">00NATION</div>  <--- the second result we get for {"class": "team"}
                </div>
            </td>
            <td class="event">
                <img alt="ESL Pro League Season 17" class="event-logo smartphone-only" src="https://img-cdn.hltv.org/eventlogo/PhVPy7kXO_J_nfTng7a87h.png?ixlib=java-2.1.0&amp;w=50&amp;s=a56cc668c5dfeb6b8bc8676b7ad8021a" title="ESL Pro League Season 17"/>
                <span class="event-name">ESL Pro League Season 17</span>
            </td>
            <td class="star-cell">
                <div class="map-and-stars">
                    <div class="stars">
                        <i class="fa fa-star star"></i>
                        <i class="fa fa-star star"></i>
                        <i class="fa fa-star star"></i>
                    </div>
                    <div class="map map-text">bo3</div>
                </div>
            </td>
        </tr>
    </table>
</div>
"""
