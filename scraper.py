import requests
from bs4 import BeautifulSoup



class MLBscraper():
    """
    Methods include scraping odds, teams, and games and parsing them into a workable format (dictionary) for
    totals, moneyline and spread betting
    """

    def MLBspread(self):
        url = "https://www.sportsbookreview.com/betting-odds/mlb-baseball/pointspread/full-game/"
        page = requests.get(url)
        soup = BeautifulSoup(page.text, features = "html.parser")
        date = soup.find("p", class_ = "fs-8 fw-bold undefined").text
        tbody = soup.find("div", id = "tbody-mlb")
        games = tbody.find_all("div", class_ = "d-flex flex-row flex-nowrap border position-relative mt-0 GameRows_eventMarketGridContainer__GuplK GameRows_neverWrap__gnQNO")
        out = []
        bookies = ["Fanduel", "Caesars", "bet365", "DraftKings", "BetMGM", "BetRivers"]
        for game in games:
            try:
                away, home = game.find_all("b")
            except:
                continue
            markets = game.find_all("div", class_ = "OddsCells_numbersContainer__6V_XO")
            game_info = {
                "home": home.text,
                "away": away.text,
                "date": date,
                "bet type": "Point Spread",
            }
            for i, market in enumerate(markets):
                away_line, home_line = market.find_all("span", class_ = "me-2")
                game_info[bookies[i]] = {
                        "home": {"spread": None, "odds": None},
                        "away": {"spread": None, "odds": None}
                    }
                for side in [home_line,away_line]:
                    operand_seen = 0
                    l = 0
                    while operand_seen < 2:
                        if side.text[l] in "+-":
                            operand_seen += 1
                            if operand_seen >= 2:
                                break
                        l += 1
                    if side == home_line:
                        game_info[bookies[i]]["home"]["spread"] = home_line.text[:l]
                        game_info[bookies[i]]["home"]["odds"] = home_line.text[l:]
                    else:
                        game_info[bookies[i]]["away"]["spread"] = away_line.text[:l]
                        game_info[bookies[i]]["away"]["odds"] = away_line.text[l:]
            out.append(game_info)
        return out

    def MLBmoneyline(self):
        url = "https://www.sportsbookreview.com/betting-odds/mlb-baseball/"
        page = requests.get(url)
        soup = BeautifulSoup(page.text, features = "html.parser")
        date = soup.find("p", class_ = "fs-8 fw-bold undefined").text
        tbody = soup.find("div", id = "tbody-mlb")
        games = tbody.find_all("div", class_ = "d-flex flex-row flex-nowrap border position-relative mt-0 GameRows_eventMarketGridContainer__GuplK GameRows_neverWrap__gnQNO")
        out = []
        bookies = ["Fanduel", "Caesars", "bet365", "DraftKings", "BetMGM", "BetRivers"]
        for game in games:
            try:
                away, home = game.find_all("b")
            except:
                continue
            markets = game.find_all("div", class_ = "OddsCells_numbersContainer__6V_XO")
            game_info = {
                "home": home.text,
                "away": away.text,
                "date": date,
                "bet type": "Money Line",
            }
            for i, market in enumerate(markets):
                away_line, home_line = market.find_all("span", class_ = "me-2")
                game_info[bookies[i]] = {}
                game_info[bookies[i]]["home"] = home_line.text
                game_info[bookies[i]]["away"] = away_line.text
            out.append(game_info)
        return out

    def MLBtotals(self):
        url = "https://www.sportsbookreview.com/betting-odds/mlb-baseball/totals/full-game/"
        page = requests.get(url)
        soup = BeautifulSoup(page.text, features = "html.parser")
        date = soup.find("p", class_ = "fs-8 fw-bold undefined").text
        tbody = soup.find("div", id = "tbody-mlb")
        games = tbody.find_all("div", class_ = "d-flex flex-row flex-nowrap border position-relative mt-0 GameRows_eventMarketGridContainer__GuplK GameRows_neverWrap__gnQNO")
        out = []
        bookies = ["Fanduel", "Caesars", "bet365", "DraftKings", "BetMGM", "BetRivers"]
        for game in games:
            try:
                away, home = game.find_all("b")
            except:
                continue
            markets = game.find_all("div", class_ = "OddsCells_numbersContainer__6V_XO")
            game_info = {
                "home": home.text,
                "away": away.text,
                "date": date,
                "bet type": "Totals",
            }

            for i, market in enumerate(markets):
                away_line, home_line = market.find_all("span", class_ = "me-2")
                game_info[bookies[i]] = {}
                over = away_line
                under = home_line
                l = 0
                while over.text[l] != "+" and over.text[l] != "-":
                    l += 1

                line = float(over.text[:l].strip())
                game_info[bookies[i]]["line"] = line
                game_info[bookies[i]]["over"] = float(over.text[l:])
                game_info[bookies[i]]["under"] = float(under.text[l:])
            out.append(game_info)
        return out


    def sportsBookReview(self, betting_type):
        if betting_type == "Point Spread":
            url = "https://www.sportsbookreview.com/betting-odds/mlb-baseball/pointspread/full-game/"
        elif betting_type == "Money Line":
            url = "https://www.sportsbookreview.com/betting-odds/mlb-baseball/"
        elif betting_type == "Totals":
            url = "https://www.sportsbookreview.com/betting-odds/mlb-baseball/totals/full-game/"
        else:
            print("Enter valid betting type")
            return


        page = requests.get(url)
        soup = BeautifulSoup(page.text, features = "html.parser")
        date = soup.find("p", class_ = "fs-8 fw-bold undefined").text
        tbody = soup.find("div", id = "tbody-mlb")
        games = tbody.find_all("div", class_ = "d-flex flex-row flex-nowrap border position-relative mt-0 GameRows_eventMarketGridContainer__GuplK GameRows_neverWrap__gnQNO")
        out = []
        bookies = ["Fanduel", "Caesars", "bet365", "DraftKings", "BetMGM", "BetRivers"]
        for game in games:
            away, home = game.find_all("b")
            markets = game.find_all("div", class_ = "OddsCells_numbersContainer__6V_XO")
            game_info = {
                "home": home.text,
                "away": away.text,
                "date": date,
                "bet type": betting_type,
            }

            for i, market in enumerate(markets):
                away_line, home_line = market.find_all("span", class_ = "me-2")
                if betting_type == "Money Line":
                    game_info[bookies[i]] = {}
                    game_info[bookies[i]]["home"] = home_line.text
                    game_info[bookies[i]]["away"] = away_line.text

                elif betting_type == "Point Spread":
                    game_info[bookies[i]] = {
                        "home": {"spread": None, "odds": None},
                        "away": {"spread": None, "odds": None}
                    }
                    for side in [home_line,away_line]:
                        operand_seen = False
                        l = 0
                        while side.text[l] not in "+-" and operand_seen:
                            if side.text[l] in "+-":
                                operand_seen = True
                            l += 1
                        if side == home_line:
                            game_info[bookies[i]]["home"]["spread"] = home_line.text[:l]
                            game_info[bookies[i]]["home"]["odds"] = home_line.text[l:]
                        else:
                            game_info[bookies[i]]["away"]["spread"] = away_line.text[:l]
                            game_info[bookies[i]]["away"]["odds"] = away_line.text[l:]



                elif betting_type == "Totals":
                    game_info[bookies[i]] = {}
                    over = away_line
                    under = home_line
                    l = 0
                    while over.text[l] != "+" and over.text[l] != "-":
                        l += 1

                    line = float(over.text[:l].strip())
                    game_info[bookies[i]]["line"] = line
                    game_info[bookies[i]]["over"] = float(over.text[l:])
                    game_info[bookies[i]]["under"] = float(under.text[l:])


                print((away.text,away_line.text), (home.text,home_line.text))
            out.append(game_info)
        return out

mlb_odds = MLBscraper()

"""
{'home': 'CHC',
'away': 'STL',
'date': 'Friday, August 2, 2024 ',
'bet type': 'Money Line',
'Fanduel': {'home': '-104', 'away': '-112'},
'Caesars': {'home': '-5000', 'away': '+1800'},
'bet365': {'home': '+100', 'away': '-120'},
'DraftKings': {'home': '-102', 'away': '-118'},
'BetMGM': {'home': '-105', 'away': '-120'},
'BetRivers': {'home': '-177', 'away': '+116'}}


{'home': 'CHC',
'away': 'STL',
'date': 'Friday, August 2, 2024 ',
'bet type': 'Totals',
'Fanduel': {'line': 8.0, 'over': -122.0, 'under': 100.0},
'Caesars': {'line': 6.5, 'over': -149.0, 'under': 120.0},
'bet365': {'line': 8.5, 'over': -105.0, 'under': -115.0},
'DraftKings': {'line': 8.5, 'over': -105.0, 'under': -115.0},
'BetMGM': {'line': 4.5, 'over': -110.0, 'under': -120.0},
'BetRivers': {'line': 6.5, 'over': 220.0, 'under': -335.0}}


{'home': 'CHC',
'away': 'STL',
'date': 'Friday, August 2, 2024 ',
'bet type': 'Point Spread',
'Fanduel': {'home': {'spread': '+1.5', 'odds': '-176'}, 'away': {'spread': '-1.5', 'odds': '+146'}},
'Caesars': {'home': {'spread': '+1.5', 'odds': '-161'}, 'away': {'spread': '-1.5', 'odds': '+135'}},
'bet365': {'home': {'spread': '+1.5', 'odds': '-165'}, 'away': {'spread': '-1.5', 'odds': '+140'}},
'DraftKings': {'home': {'spread': '+1.5', 'odds': '-175'}, 'away': {'spread': '-1.5', 'odds': '+145'}},
'BetMGM': {'home': {'spread': '+1.5', 'odds': '-175'}, 'away': {'spread': '-1.5', 'odds': '+145'}},
'BetRivers': {'home': {'spread': '+1', 'odds': '-143'}, 'away': {'spread': '-1', 'odds': '+115'}}}

"""
