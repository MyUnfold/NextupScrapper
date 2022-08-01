import requests
from lxml import html
import json

from fastapi import FastAPI

app = FastAPI()


@app.get("/player/{state}/{city}/{school}/{name}")
async def get_player_data(name, school, city, state):
    try:
        url = f'https://www.maxpreps.com/m/feeds/search.ashx?type=athlete&search={name}&state={state}&gendersport=boys,basketball'
        res = requests.get(url)
        data = json.loads(res.text)
        if len(data["response"]["results"]) == 1:
            athlete_url = data["response"]["results"][0]["url"]
        else:
            for record in data["response"]["results"]:
                if (record["mostrecentSchool"]["name"]).lower() == school.lower() and (record["mostrecentSchool"]["city"]).lower() == city.lower() :
                    athlete_url = record["url"]
                    break

        data = get_athlete_info(athlete_url)


        # data = get_athlete_data(name, school, city, state)

        # Get latest season
        if "Basketball" in data["games"].keys():
            latest_season = data["games"]["Basketball"]["seasons"][0]

            # Get featured stats
            featured_stats = latest_season["featured_stats"]

            # Get featured stats keys
            featured_stats_keys = list(featured_stats.keys())
            featured_keys = []

            # Iterate keys and crete abbrevation
            for stats_key in featured_stats_keys:
                words = stats_key.split("_")
                letters = [word[0] for word in words]
                featured_keys.append(("".join(letters)).upper())

            # Create a dictionary with featured data and abrevated keys
            featured_stats_data = {}

            for i in range(len(featured_stats_keys)):
                featured_stats_data[featured_keys[i]] = featured_stats[featured_stats_keys[i]]

            # Get Total Stats
            stats = latest_season["stats"]
            for stat in stats:
                if stat["title"] == "Totals":
                    total_stats = stat["data"]

            # Calculate average per game by calculation total and divide by total games
            t_min = 0
            t_pts = 0
            t_oreb = 0
            t_dreb = 0
            t_reb = 0
            t_ast = 0
            t_stl = 0
            t_blk = 0
            t_to = 0
            t_pf = 0

            total_games = 0

            for game in total_stats:
                t_min += int(game["min"] or 0)
                t_pts += int(game["pts"] or 0)
                t_oreb += int(game["oreb"] or 0)
                t_dreb += int(game["dreb"] or 0)
                t_reb += int(game["reb"] or 0)
                t_ast += int(game["ast"] or 0)
                t_stl += int(game["stl"] or 0)
                t_blk += int(game["blk"] or 0)
                t_to += int(game["to"] or 0)
                t_pf += int(game["pf"] or 0)
                total_games += 1

            if total_games > 0:

                # Final response json
                resp = {
                    "playingPosition": data["player_grade"],
                    "improved": True,
                    "pgs": featured_stats_data,
                    "playersKpis": {
                        "MIN": "{:.2f}".format(float(t_min / total_games)),
                        "PTS": "{:.2f}".format(float(t_pts / total_games)),
                        "OREB": "{:.2f}".format(float(t_oreb / total_games)),
                        "DREB": "{:.2f}".format(float(t_dreb / total_games)),
                        "REB": "{:.2f}".format(float(t_reb / total_games)),
                        "AST": "{:.2f}".format(float(t_ast / total_games)),
                        "STL": "{:.2f}".format(float(t_stl / total_games)),
                        "BLK": "{:.2f}".format(float(t_blk / total_games)),
                        "TO": "{:.2f}".format(float(t_to / total_games)),
                        "PF": "{:.2f}".format(float(t_pf / total_games))
                    }
                }
            else:
                # Final response json
                resp = {
                    "playingPosition": data["player_grade"],
                    "improved": True,
                    "pgs": featured_stats_data,
                }

            return {"success": True, "data": resp}
        else:
            return None
    except Exception:
        print(Exception.with_traceback())
        return {"success": False, "data": {}, "message": "Something went wrong"}


cookies = {
    '_ga': 'GA1.2.69878116.1648575323',
    '_pbjs_userid_consent_data': '3524755945110770',
    '_pubcid': '0a95159b-3b36-400c-81a5-fd1e882ed61f',
    's_ecid': 'MCMID%7C77336000660111060323417149131541050962',
    '__gads': 'ID=4cfcc7f00a452c11:T=1648575324:S=ALNI_MYk_p5NY-VLmLylBsVqnHaIDSEkLA',
    'AAMC_cbsi_0': 'REGION%7C3',
    'aamgam': 'segid%3D16007068%2C1631416%2C13100219',
    'aam_uuid': '77115157537764350803403505218101588778',
    '_lr_env_src_ats': 'false',
    'trc_cookie_storage': 'taboola%2520global%253Auser-id%3De9382160-a1c5-4447-82a6-66b094f89015-tuct783fc8e',
    '_cc_cc': 'optout',
    'panoramaId_expiry': '1651167333060',
    '_admrla': '2.0-f6f90667-ecf6-d080-9941-e62dab32f0a4',
    'AMCVS_10D31225525FF5790A490D4D%40AdobeOrg': '1',
    's_cc': 'true',
    '_BB.bs': 'f|2',
    '_gid': 'GA1.2.914210977.1649161975',
    'AMCV_10D31225525FF5790A490D4D%40AdobeOrg': '1585540135%7CMCIDTS%7C19088%7CMCMID%7C77336000660111060323417149131541050962%7CMCAAMLH-1649766776%7C3%7CMCAAMB-1649766776%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1649169176s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0',
    '_tb_sess_r': '',
    '_lr_retry_request': 'true',
    '_BB.id.liveIntent': '%7B%22unifiedId%22%3A%22H7yvGLQjRNBCQJjK9u1KfE7xjVi0ZNQYg_0Yuw%22%7D',
    'bounceClientVisit4834v': 'N4IgNgDiBcIBYBcEQM4FIDMBBNAmAYnvgO6kB0AtgIYAeEATgKapkDGA9hUVQnGIwkZFqKdgDsAtMQCWYMNKoV0BegDMAbAE4A6gHYA+gCsAoowCOWAF5mASsfaX26sMSIAjKigDWAj3KIoCDwoZIhcuBgAnoxU9JgAIrgAjBK4uCAANCD0MCAgAL5AA',
    's_sq': '%5B%5BB%5D%5D',
    '__gpi': 'UID=0000037b9e8974d1:T=1649162012:RT=1649162012:S=ALNI_MZq_kraTbiY70j0G7614PbAVw-2TA',
    'OptanonAlertBoxClosed': '2022-04-05T12:33:40.324Z',
    '_BB.d': '0|||3',
    'OptanonConsent': 'isIABGlobal=false&datestamp=Tue+Apr+05+2022+17%3A33%3A43+GMT%2B0500+(Pakistan+Standard+Time)&version=6.30.0&hosts=&consentId=943e52ed-164d-425d-92c2-bcff2eb7ba1c&interactionCount=1&landingPath=NotLandingPage&groups=2%3A1%2C3%3A1%2C4%3A1%2C5%3A1&AwaitingReconsent=false&geolocation=PK%3BPB',
    'QSI_HistorySession': 'https%3A%2F%2Fwww.maxpreps.com%2Fathlete%2Fmason-williams%2Frf69W7_jEeqAzqREozo6lw%2Fbasketball%2Fstats.htm~1648838982337%7Chttps%3A%2F%2Fwww.maxpreps.com%2Fathlete%2Fmason-williams%2Frf69W7_jEeqAzqREozo6lw%2Fbasketball%2Fstats.htm%23year%3D21-22~1649161977274%7Chttps%3A%2F%2Fwww.maxpreps.com%2F~1649162012268%7Chttps%3A%2F%2Fwww.maxpreps.com%2Fsearch%2Fdefault.aspx%3Ftype%3Dathlete%26search%3DMason%2520Williams%26state%3D%26gendersport%3D~1649162023715',
    '_awl': '2.1649162023.0.5-f6f90667ecf6d0809941e62dab32f0a4-6763652d6575726f70652d7765737431-0',
    '_tb_t_ppg': 'https%3A//www.maxpreps.com/search/default.aspx%3Ftype%3Dathlete%26search%3DMason%2520Williams%26state%3D%26gendersport%3D',
    'xdibx': 'N4Ig-mBGAeDGCuAnRIBcoAOGAuBnNAjAGwAsAnMQEwAMlRA7NfQDQgYBusAdtoQMytc-VMXLECZemTKUArKw65uvVAJCIkAGzQgQrTVp0B6AIbYAFpoCm2K0YC2J3AHsuAWgDuAS02avJ-1wjRAAzIjIAdXowACsAUSsARwBBAC9EgCU451TnIk0PI0gnAGsbYt8jXGwzXAA6c2x7AGIATysTRABeSgI3Sko9EE08QlIADll6WT4-aj5pgF9WCBgMRCt2NFAAExNW4QBtUUnp2fnxomYT8b5bkhJx-kpr0goiCSkyWYBdZfAoNBNlYeMJgP9VnAvDsdLAyDsyE8CLI3CZZFZxm4SKQQm4yJArFYsSEdpA-CQCONqNJqG4TlMZpQqaQQIsgA_',
    'cto_bundle': '3Rm8Vl9qeFROQzkzd1dYZHRSQVc1dEZQdGw1d0dBOTUzbDElMkZQTmZjTmlHR0l0NUZmY2xaeFN1R1FFaEZOaDZBWXAlMkY2OWg2cjc3QURkZEdqaWRiaU5CMnROV2prZVRWUWUlMkJZUWp2MUp6c3dDWGlGJTJCSmdTYUpOZXc4RkVlNmFEa1ZVUGpJaFdqMU50VlBzQ1AlMkI0UTlXVWtLd3QxRWx1dE5KM2J3dHdYOGNGSktRVks1cGRmNUFXYkhuemE4THN6T2JBbSUyRkM',
    'cto_bidid': '-hM9L182eCUyRm1VWCUyRlQxQldNUDZrSzN4d3pUZkxMNjhvYjN3VyUyRklMb2xFeTBRNWVFMEglMkJDRlpMOFYyJTJGSnVyb09DeldFM2VpRzdkWTZSbyUyRkNzcDYwayUyRmQzUFlXOWE1R3U4TGp2M042YklxZm15OVp0ZXNFTEpOaVJscjZaMkNGMyUyRmNwa2F4NnRzT3I4Q0daWHAlMkY0MnNuVTg2UVElM0QlM0Q',
}

headers = {
    'authority': 'www.maxpreps.com',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9',
}


# def search_athlete(athlete_name, athlete_school, athlete_city, athlete_state):
#     """
#     This function perform the search operation for an athlete. Matches up the given city, school with the one found
#     for returned players. If a match is received, it returns that player's url
#     """
#
#     print(f"\nAth Name: {athlete_name}")
#     print(f"Ath school: {athlete_school}")
#     print(f"Ath city: {athlete_city}")
#
#     params = {
#         'type': 'athlete',
#         'search': f'{athlete_name}',
#         'state': f'{athlete_state}',
#         'gendersport': '',
#     }
#
#     r = requests.get('https://www.maxpreps.com/search/default.aspx', headers=headers, params=params,
#                      cookies=cookies)
#     if r.status_code == 200:
#         r = html.fromstring(r.text)
#         players = r.xpath("//li[@class='row result' and @style='']")
#
#         for player in players:
#             school_name = player.xpath(".//a[@data-js-hook='school-link']/text()")[0]
#             if school_name.lower() in athlete_school.lower():
#                 print(f"Schools matched")
#                 school_location = player.xpath(".//span[@data-js-hook='school-location']/text()")[0]
#                 if "," in school_location:
#                     city_name = school_location.split(",")[0]
#
#                     if city_name.lower() in athlete_city.lower():
#                         print(f"Cities matched")
#                         athlete_url = player.xpath(".//a[@data-js-hook='athlete-link']/@href")[0]
#                         print(f"Ath url: {athlete_url}")
#                         return athlete_url
#                 else:
#                     print("No city found")
#                     athlete_url = player.xpath(".//a[@data-js-hook='athlete-link']/@href")[0]
#                     print(f"Ath url: {athlete_url}")
#                     return athlete_url
#     else:
#         print(f"Request to search athlete failed with status {r.status_code}")


def get_category_data(url):
    """
    This function makes a request to the given game category of a player and returns the data dict
    """

    r = requests.get(url, headers=headers, cookies=cookies)
    if r.status_code == 200:
        r = html.fromstring(r.text)
        seasons = r.xpath("//div[@class='item' and @data-year]")
        seasons_data = []
        for season in seasons:
            this_season_dict = {}

            season_year = season.xpath(".//@data-year")[0]
            this_season_dict['year'] = season_year

            # Getting Featured Stats Data
            featured_stats = season.xpath(".//ul[@class='featured-stats']/li")
            featured_stats_dict = {}
            for featured_stat in featured_stats:
                featured_stat_heading = featured_stat.xpath(".//div[@class='stat-name']/text()")[0].strip()
                featured_stat_heading = featured_stat_heading.replace(" ", '_').lower()

                featured_stat_value = featured_stat.xpath(".//div[@class='stat-field']/text()")[0].strip()

                featured_stats_dict[featured_stat_heading] = featured_stat_value

            this_season_dict['featured_stats'] = featured_stats_dict

            # Getting main Stats
            stat_grids = season.xpath(".//div[@class='stats-grids']/div")
            stat_grids_data = []

            for grid in stat_grids:
                this_grid_dict = {}

                grid_title = grid.xpath(".//h3/text()")[0]
                this_grid_dict['title'] = grid_title

                grid_tables = grid.xpath(".//div/table")
                grid_tables_data = []
                for table in grid_tables:
                    table_headers = table.xpath(".//thead//a/text()")
                    table_headers = [x.lower() for x in table_headers]

                    table_body_rows = table.xpath(".//tbody/tr")

                    for table_row in table_body_rows:
                        this_row_dict = {}

                        all_td = table_row.xpath(".//td")

                        header_counter = 0
                        for td in all_td:
                            this_header = table_headers[header_counter]
                            header_counter += 1

                            try:
                                this_value = td.xpath(".//text()")[0]
                            except IndexError:
                                this_value = ''

                            this_row_dict[this_header] = this_value

                        grid_tables_data.append(this_row_dict)

                this_grid_dict['data'] = grid_tables_data

                stat_grids_data.append(this_grid_dict)

            this_season_dict['stats'] = stat_grids_data

            seasons_data.append(this_season_dict)

        return seasons_data

    else:
        print(f"Request to get category failed with status {r.status_code}")


# def get_athlete_data(athlete_name, athlete_school, athlete_city, athlete_state):
#     """
#     This is the MAIN function.
#
#     All of the data is gathered and returned as json by this function
#     """
#
#     athlete_url = search_athlete(athlete_name, athlete_school, athlete_city, athlete_state)
#     print(f"Athlete Url: {athlete_url}")
#
#     this_athlete_dict = {}
#
#     if athlete_url:
#         r = requests.get(athlete_url, headers=headers, cookies=cookies)
#         if r.status_code == 200:
#             r = html.fromstring(r.text)
#
#             this_athlete_dict['player_name'] = athlete_name
#             this_athlete_dict['player_school'] = athlete_school
#             this_athlete_dict['player_city'] = athlete_city
#             this_athlete_dict['player_state'] = athlete_state
#             this_athlete_dict['player_url'] = athlete_url
#
#             try:
#                 height = r.xpath("//span[@class='height']/text()")[0].strip()
#             except Exception:
#                 height = ''
#             this_athlete_dict['player_height'] = height
#
#             try:
#                 weight = r.xpath("//span[@class='weight']/text()")[0].strip()
#             except Exception:
#                 weight = ''
#             this_athlete_dict['player_weight'] = weight
#
#             try:
#                 grade = r.xpath("//span[@class='grade']/text()")[0].strip()
#             except Exception:
#                 grade = ''
#             this_athlete_dict['player_grade'] = grade
#
#             game_categories = r.xpath("//a[@data-la='stats']")
#             categories_dict = {}
#             for category in game_categories:
#                 category_name = category.xpath(".//text()")[0]
#                 print(f"\nCat name: {category_name}")
#
#                 category_url = category.xpath(".//@href")[0]
#                 category_url = " https://www.maxpreps.com" + category_url
#                 print(f"Cat url: {category_url}")
#
#                 category_data = get_category_data(category_url)
#
#                 categories_dict[category_name] = {'seasons': category_data}
#
#             this_athlete_dict['games'] = categories_dict
#
#         else:
#             print(f"Request failed to grab data with status {r.status_code}")
#     else:
#         print("No match found for this Athlete")
#
#     return this_athlete_dict


"""
API to get Team Stats and Roster
"""
@app.get("/team/{state}/{name}")
async def get_team_data(name, state):
    try:
        url = f'https://www.maxpreps.com/m/feeds/search.ashx?type=school&search={name}&state={state}&gendersport=boys,basketball'
        res = requests.get(url)
        data = json.loads(res.text)
        team_url = data["response"]["results"][0]["url"]
        team_basketball_url = team_url + "basketball/"
        team_roster_url = team_basketball_url + "roster/all-time/"
        team_staff_url = team_basketball_url + "staff/"
        team_schedule_url = team_basketball_url + "schedule/"
        team_schedule_alltime_url = team_basketball_url + "schedule/all-time/"

        # Get Team Stats
        r = requests.get(team_basketball_url)
        if r.status_code == 200:
            #print(r.text)
            stats = {}
            r = html.fromstring(r.text)
            stats["overall"] = r.xpath("//span[@class='StyledText-sc-yyz0ad-0 qhdev f18_bold']/text()")[0]
            stats["district"] = r.xpath("//span[@class='StyledText-sc-yyz0ad-0 qhdev f18_bold']/text()")[1]

            stats["home"] = r.xpath("//span[@class='StyledText-sc-yyz0ad-0 RecordDetailsBox__StyledDetailsRow-sc-1n4q0pk-1 doAyHc iFvYoY f11_bold_tall_upper']/span/text()")[0]
            stats["away"] = r.xpath("//span[@class='StyledText-sc-yyz0ad-0 RecordDetailsBox__StyledDetailsRow-sc-1n4q0pk-1 doAyHc iFvYoY f11_bold_tall_upper']/span/text()")[1]
            stats["neutral"] = r.xpath("//span[@class='StyledText-sc-yyz0ad-0 RecordDetailsBox__StyledDetailsRow-sc-1n4q0pk-1 doAyHc iFvYoY f11_bold_tall_upper']/span/text()")[2]
            stats["pf"] = r.xpath("//span[@class='StyledText-sc-yyz0ad-0 RecordDetailsBox__StyledDetailsRow-sc-1n4q0pk-1 doAyHc iFvYoY f11_bold_tall_upper']/span/text()")[3]
            stats["pa"] = r.xpath("//span[@class='StyledText-sc-yyz0ad-0 RecordDetailsBox__StyledDetailsRow-sc-1n4q0pk-1 doAyHc iFvYoY f11_bold_tall_upper']/span/text()")[4]
            stats["streak"] = r.xpath("//span[@class='StyledText-sc-yyz0ad-0 RecordDetailsBox__StyledDetailsRow-sc-1n4q0pk-1 doAyHc iFvYoY f11_bold_tall_upper']/span/text()")[5]

        # Get Team Roster and Player info for last 5 seasons
        r = requests.get(team_roster_url)
        if r.status_code == 200:
            # print(r.text)
            roster = []
            r = html.fromstring(r.text)
            seasons = r.xpath("//li[@class='ProgramSeasonContainer__StyledProgramSeasonContainer-sc-c78q6v-0 cApBia']")
            for season in seasons[0:5]:
                s = {}
                s["season"] = season.xpath(".//h2/span[@class='f20_bold']/text()")[0]
                s["data"] = {}
                s["data"]["head_coach"] = season.xpath(".//div[@class='StyledText-sc-yyz0ad-0 ePEddr f14_tall']/text()")[1]
                s["data"]["players"] = []
                players = season.xpath(".//div[@class='AllTimeRosterPage__StyledAthleteGrid-sc-1dia9se-0 cbYuvw']/span/a[@class='StyledAnchor-sc-jb44mu-0 fudJqG f14_tall']")
                for player in players:
                    p = {}
                    url = player.xpath(".//@href")[0]
                    name = player.xpath(".//text()")[0]
                    n = name.split(", ")
                    p["name"] = n[1] + " " + n[0]
                    p["info"] = get_player_info(url)
                    s["data"]["players"].append(p)
                roster.append(s)


        # Get All Time Stats
        r = requests.get(team_schedule_alltime_url)
        if r.status_code == 200:
            all_time = {}
            r = html.fromstring(r.text)
            streaks = r.xpath("//table")[0].xpath(".//tbody/tr")
            all_time["streak"] = []
            for streak in streaks:
                s = {}
                s["start_year"] = streak.xpath(".//td[@class='start first start-year']/text()")
                s["end_year"] = streak.xpath(".//td[@class='end end-year']/text()")
                s["streak"] = streak.xpath(".//th[@class='streak last sorted']/text()")
                all_time["streak"].append(s)

            games = r.xpath("//table")[1].xpath(".//tbody/tr")
            all_time["games"] = []
            for game in games:
                s = {}
                s["game_type"] = game.xpath(".//th[@class='gametype first sorted']/text()")
                s["record"] = game.xpath(".//td[@class='record last']/text()")
                all_time["games"].append(s)

            opponent_games = r.xpath("//table")[2].xpath(".//tbody/tr")
            all_time["opponent_games"] = []
            for game in opponent_games:
                s = {}
                s["opponent"] = game.xpath(".//th[@class='opponent first']/a/text()")
                s["record"] = game.xpath(".//td[@class='record sorted']/text()")
                all_time["opponent_games"].append(s)

        return {"success": True, "data": {"stats": stats, "roster": roster, "all_time": all_time}}

    except Exception:
        print(Exception.with_traceback())
        return {"success": False, "data": {}, "message": "Something went wrong"}


def get_player_info(url):
    """
    Function to get player info from URL
    :param url:
    :return:
    """
    try:
        data = get_athlete_info(url)

        # Get latest season
        if "Basketball" in data["games"].keys():
            latest_season = data["games"]["Basketball"]["seasons"][0]

            # Get featured stats
            featured_stats = latest_season["featured_stats"]

            # Get featured stats keys
            featured_stats_keys = list(featured_stats.keys())
            featured_keys = []

            # Iterate keys and crete abbrevation
            for stats_key in featured_stats_keys:
                words = stats_key.split("_")
                letters = [word[0] for word in words]
                featured_keys.append(("".join(letters)).upper())

            # Create a dictionary with featured data and abrevated keys
            featured_stats_data = {}

            for i in range(len(featured_stats_keys)):
                featured_stats_data[featured_keys[i]] = featured_stats[featured_stats_keys[i]]

            # Get Total Stats
            stats = latest_season["stats"]
            for stat in stats:
                if stat["title"] == "Totals":
                    total_stats = stat["data"]

            # Calculate average per game by calculation total and divide by total games
            t_min = 0
            t_pts = 0
            t_oreb = 0
            t_dreb = 0
            t_reb = 0
            t_ast = 0
            t_stl = 0
            t_blk = 0
            t_to = 0
            t_pf = 0

            total_games = 0

            for game in total_stats:
                t_min += int(game["min"] or 0)
                t_pts += int(game["pts"] or 0)
                t_oreb += int(game["oreb"] or 0)
                t_dreb += int(game["dreb"] or 0)
                t_reb += int(game["reb"] or 0)
                t_ast += int(game["ast"] or 0)
                t_stl += int(game["stl"] or 0)
                t_blk += int(game["blk"] or 0)
                t_to += int(game["to"] or 0)
                t_pf += int(game["pf"] or 0)
                total_games += 1

            if total_games > 0:

                # Final response json
                resp = {
                    "playingPosition": data["player_grade"],
                    "improved": True,
                    "pgs": featured_stats_data,
                    "playersKpis": {
                        "MIN": "{:.2f}".format(float(t_min / total_games)),
                        "PTS": "{:.2f}".format(float(t_pts / total_games)),
                        "OREB": "{:.2f}".format(float(t_oreb / total_games)),
                        "DREB": "{:.2f}".format(float(t_dreb / total_games)),
                        "REB": "{:.2f}".format(float(t_reb / total_games)),
                        "AST": "{:.2f}".format(float(t_ast / total_games)),
                        "STL": "{:.2f}".format(float(t_stl / total_games)),
                        "BLK": "{:.2f}".format(float(t_blk / total_games)),
                        "TO": "{:.2f}".format(float(t_to / total_games)),
                        "PF": "{:.2f}".format(float(t_pf / total_games))
                    }
                }
            else:
                # Final response json
                resp = {
                    "playingPosition": data["player_grade"],
                    "improved": True,
                    "pgs": featured_stats_data,
                }

            return resp
        else:
            return None
    except Exception:
        print(Exception.with_traceback())
        return {"success": False, "data": {}, "message": "Something went wrong"}


def get_athlete_info(url):
    """
    Helper Function to get athlete info from URL
    """
    this_athlete_dict = {}

    if url:
        r = requests.get(url, headers=headers, cookies=cookies)
        if r.status_code == 200:
            r = html.fromstring(r.text)

            this_athlete_dict['player_url'] = url

            try:
                height = r.xpath("//span[@class='height']/text()")[0].strip()
            except Exception:
                height = ''
            this_athlete_dict['player_height'] = height

            try:
                weight = r.xpath("//span[@class='weight']/text()")[0].strip()
            except Exception:
                weight = ''
            this_athlete_dict['player_weight'] = weight

            try:
                grade = r.xpath("//span[@class='grade']/text()")[0].strip()
            except Exception:
                grade = ''
            this_athlete_dict['player_grade'] = grade

            game_categories = r.xpath("//a[@data-la='stats']")
            categories_dict = {}
            for category in game_categories:
                category_name = category.xpath(".//text()")[0]
                #print(f"\nCat name: {category_name}")

                category_url = category.xpath(".//@href")[0]
                category_url = " https://www.maxpreps.com" + category_url
                #print(f"Cat url: {category_url}")

                category_data = get_category_data(category_url)

                categories_dict[category_name] = {'seasons': category_data}

            this_athlete_dict['games'] = categories_dict

        else:
            print(f"Request failed to grab data with status {r.status_code}")
    else:
        print("No match found for this Athlete")

    return this_athlete_dict