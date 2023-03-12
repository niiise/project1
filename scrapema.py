import sugma
import bs4
import requests


# TODO: try doing this with different URLs to check it works
# TODO: try coming up with a URL that returns no results

url = sugma.get_hltv_results_url(
    stars=3,
    mapnames=["de_cache", "de_mirage"],
    start_date="2022-02-22",
    end_date="2023-03-05",
)

# TODO: turn this & down into a function that accepts a URL and prints the results from that page
response = requests.get(url)

# HTTP status codes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status (not important lol)
# Web pages are made of HTML (structure), CSS (designs), JavaScript (code to make it do stuff)

print(url)
# print(response.content)

# requests: http part: gets a webpage from a server, downloads the HTML
# bs4: represent the html as Python (instead of us doing rudimentary text search) & allow us to query the document

# think of soup as containing the whole page
soup = bs4.BeautifulSoup(response.content, features="html.parser")

# docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#kinds-of-filters
# trivia: div is an html tag, open tag <div>, close tag </div>
# for each element in here, we would expect element["class"] to be "result"
elements_that_probably_have_match_results = soup.find_all("div", {"class": "result"})

# TODO: (later, this is probably too hard to bother trying): print the date before each of these (we will have to modify
# the initial find_all above)^^
# maybe this would look like results_sublist_element = find_all("results-sublists")
# you could get the date by findChild in results_sublist_element
# then you have to find result_element by doing results_sublist_element.findChild("result") etc.

for result_element in elements_that_probably_have_match_results:
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

    # Winner: Grayhound, loser: 00NATION
    # TODO: (low priority) get this code to work and not have these errors (you might need to define the variables ahead of time)
    print("Winner: " + winner_name + ", Loser: " + loser_name)

    # TODO (try me first): print the tournament name
    # TODO (try me first: tricky): print the score
    # TODO (try me first: tricky): print "bo3", "bo5", "mrg", etc.
    # TODO (very tricky, will be impressed if you get this): print the number of stars


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
            <td class="event"><img alt="ESL Pro League Season 17" class="event-logo smartphone-only" src="https://img-cdn.hltv.org/eventlogo/PhVPy7kXO_J_nfTng7a87h.png?ixlib=java-2.1.0&amp;w=50&amp;s=a56cc668c5dfeb6b8bc8676b7ad8021a" title="ESL Pro League Season 17"/><span class="event-name">ESL Pro League Season 17</span></td>
            <td class="star-cell">
            <div class="map-text">bo3</div>
            </td>
        </tr>
    </table>
</div>
"""
