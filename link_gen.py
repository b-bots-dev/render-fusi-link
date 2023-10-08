import requests


def link_gen(uid):
    url = "https://cpapi.footseen.xyz/room/enterRoom"

    querystring = {"lang": "1", "os": "h5", "cid": "ftsH5", "webVersion": "1000", "roomId": uid,
                   "pageID": "56f901109e787c055c5ca8bd872fe88b"}

    headers = {
        "Host": "cpapi.footseen.xyz",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "user-agent": "Mozilla/5.0 (Linux; Android 7.1.2; ASUS_Z01QD) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/86.0.4240.198 Mobile Safari/537.36",
        "origin": "origin",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://www.footseen.xyz/",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9"
    }

    try:
        with requests.get(url, params=querystring, headers=headers) as response:
            if response.status_code == 200:
                r = response.json()
                if r['msg'] == 'successful':
                    name = r['roomBaseInfo']['nickname']
                    country = r['roomBaseInfo']['addr']
                    followme = r['roomOtherInfo']['followme']
                    myfollow = r['roomOtherInfo']['myfollow']
                    hls = r['pullFlowUrlHLS']
                    flv = r['pullFlowUrl']
                    looksum = r['room']['lookSum']

                    try:
                        ticket = r['ticketRoomInfo']['tollProgressBarVo']['showTopic']
                    except KeyError:
                        ticket = None

                    head = (f'🆔 ID : {uid}\n'
                            f'👤 NAME : {name}\n'
                            f'🌏 COUNTRY : {country}\n'
                            f'👥 FANS : {followme}  |  FOLLOWED : {myfollow}')

                    if hls == '':
                        links = '\n\nOffline / paused / lag'
                    else:
                        links = (f'\n👀 VIEWS : {looksum}'
                                 f'\n\n🔗 M3U8 : {hls}\n\n'
                                 f'🔗 FLV : {flv}')

                    if ticket is None:
                        text = f'{head}{links}'
                    else:
                        text = f'{head}🎟 PAID TICKET NAME : {ticket}\n\n{links}'

                    return text

    except requests.exceptions.SSLError:
        text = 'Connection error, try again in few seconds'
        return text

    except requests.exceptions.ConnectionError:
        text = 'Connection error, try again in few seconds'
        return text
