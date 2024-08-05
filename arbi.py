from typing import List
from scraper import MLBscraper

def american_to_decimal(american_odds):
    if american_odds > 0:
        return (american_odds/100) + 1
    else:
        return (100/abs(american_odds)) + 1
def calculate_arbitrage(oddsA, oddsB):
    return ((1/oddsA) * 100) + ((1/oddsB) * 100)

class Arbitrage():
    def totals(self, games: List[dict], investment = 100):
        bookies = ["Fanduel", "Caesars", "bet365", "DraftKings", "BetMGM", "BetRivers"]
        opportunities = []
        for game in games:
            print(game["home"], game["away"])
            for i, bookie in enumerate(bookies):
                line = game[bookie]["line"]
                over, under = american_to_decimal(game[bookie]["over"]), american_to_decimal(game[bookie]["under"])
                for j, bookie2 in enumerate(bookies, i + 1):
                    line2 = game[bookie2]["line"]
                    if line2 != line:
                        continue
                    over2, under2 = american_to_decimal(game[bookie2]["over"]), american_to_decimal(game[bookie2]["under"])
                    arbi_percentage1 = calculate_arbitrage(over, under2)
                    arbi_percentage2 = calculate_arbitrage(over2, under)
                    if arbi_percentage1 < 100:
                        betA = (investment * ((1/over) * 100)) / arbi_percentage1
                        betB = (investment * ((1/under2) * 100)) / arbi_percentage1
                        bet_dict = {
                            "game": f"{game["away"]} at {game["home"]}",
                            "line": line,
                            "betA": {"bookie": bookie, "side": "over", "odds": over, "amount": betA},
                            "betB": {"bookie": bookie2, "side": "under", "odds": under2, "amount": betB},
                            "percent profit": 100 - arbi_percentage1
                        }
                        opportunities.append(bet_dict)
                    if arbi_percentage2 < 100:
                        betA = (investment * ((1/over2) * 100)) / arbi_percentage2
                        betB = (investment * ((1/under) * 100)) / arbi_percentage2
                        bet_dict = {
                            "game": f"{game["away"]} at {game["home"]}",
                            "line": line,
                            "betA": {"bookie": bookie2, "side": "over", "odds": over2, "amount": betA},
                            "betB": {"bookie": bookie, "side": "under", "odds": under, "amount": betB},
                            "percent profit": 100 - arbi_percentage2
                        }
                        opportunities.append(bet_dict)
        return opportunities

    def moneyline(self, games: List[dict], investment = 100):
        bookies = ["Fanduel", "Caesars", "bet365", "DraftKings", "BetMGM", "BetRivers"]
        opportunities = []
        for game in games:
            for i, bookie in enumerate(bookies):
                home_odds, away_odds = american_to_decimal(float(game[bookie]["home"])), american_to_decimal(float(game[bookie]["away"]))
                for j in range(i + 1, len(bookies)):
                    home_odds2, away_odds2, = american_to_decimal(float(game[bookies[j]]["home"])), american_to_decimal(float(game[bookies[j]]["away"]))
                    arbi_percentage1 = calculate_arbitrage(home_odds, away_odds2)
                    arbi_percentage2 = calculate_arbitrage(home_odds2, away_odds)
                    if arbi_percentage1 < 100:
                        betA = (investment * ((1/home_odds) * 100)) / arbi_percentage1
                        betB = (investment * ((1/away_odds2) * 100)) / arbi_percentage1
                        bet_dict = {
                            "betA": {"bookie": bookie, "home team": game["home"], "odds": game[bookie]["home"], "amount": betA},
                            "betB": {"bookie": bookies[j], "away team": game["away"], "odds": game[bookies[j]]["away"], "amount": betB},
                            "percent profit": 100 - arbi_percentage1
                        }
                        opportunities.append(bet_dict)
                    if arbi_percentage2 < 100:
                        betA = (investment * ((1/home_odds2) * 100)) / arbi_percentage2
                        betB = (investment * ((1/away_odds) * 100)) / arbi_percentage2
                        bet_dict = {
                            "betA": {"bookie": bookies[j], "home team": game["home"], "odds": game[bookies[j]]["home"], "amount": betA},
                            "betB": {"bookie": bookie, "away team": game["away"], "odds": game[bookie]["away"], "amount": betB},
                            "pecent profit": 100 - arbi_percentage2
                        }
                        opportunities.append(bet_dict)
        return opportunities

    def spread(self, games: List[dict], investment = 100):
        bookies = ["Fanduel", "Caesars", "bet365", "DraftKings", "BetMGM", "BetRivers"]
        opportunities = []

        for game in games:
            for i, bookie in enumerate(bookies):
                spread = float(game[bookie]["home"]["spread"])
                home_odds, away_odds = american_to_decimal(float(game[bookie]["home"]["odds"])), american_to_decimal(float(game[bookie]["away"]["odds"]))
                for j, bookie2 in enumerate(bookies, i + 1):
                    spread2 = float(game[bookie2]["home"]["spread"])
                    if spread != spread2:
                        continue
                    home_odds2, away_odds2 = american_to_decimal(float(game[bookie2]["home"]["odds"])), american_to_decimal(float(game[bookie2]["away"]["odds"]))
                    arbi_percentage1 = calculate_arbitrage(home_odds, away_odds2)
                    arbi_percentage2 = calculate_arbitrage(home_odds2, away_odds)
                    if arbi_percentage1 < 100:
                        betA = (investment * ((1/home_odds) * 100)) / arbi_percentage1
                        betB = (investment * ((1/away_odds2) * 100)) / arbi_percentage1
                        bet_dict = {
                            "betA": {"bookie": bookie, "home team": game["home"], "odds": game[bookie]["home"]["odds"], "amount": betA},
                            "betB": {"bookie": bookie2, "away team": game["away"], "odds": game[bookie2]["away"]["odds"], "amount": betB},
                            "percent profit": 100 - arbi_percentage1
                        }
                        opportunities.append(bet_dict)
                    if arbi_percentage2 < 100:
                        betA = (investment * ((1/home_odds2) * 100)) / arbi_percentage2
                        betB = (investment * ((1/away_odds) * 100)) / arbi_percentage2
                        bet_dict = {
                            "betA": {"bookie": bookie2, "home team": game["home"], "odds": game[bookie2]["home"]["odds"], "amount": betA},
                            "betB": {"bookie": bookie , "away team": game["away"], "odds": game[bookie]["away"]["odds"], "amount": betB},
                            "percent profit": 100 - arbi_percentage2
                        }
                        opportunities.append(bet_dict)
        return opportunities

scraper = MLBscraper()
moneyline, totals, spread = scraper.MLBmoneyline(), scraper.MLBtotals(), scraper.MLBspread()
arb = Arbitrage()
print(arb.spread(spread), arb.totals(totals), arb.moneyline(moneyline))



"""
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

"""

