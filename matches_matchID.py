import common
import json
import time
import os


def make_game_state_info(match_id, rqh):
    result = common.check_authorization(rqh)
    if result:
        return result

    f_path = "./json/" + str(match_id) + "th_field_info.json"
    a_path = "./json/Authorization.json"
    token = rqh['Authorization']

    if not os.path.isfile(f_path):
        return json.loads(json.dumps({'status': 'InvalidToken'}))

    with open(a_path, 'r') as f:
        auth_info = json.load(f)
    with open(f_path, 'r') as f:
        field_info = json.load(f)

    idss = auth_info[token]
    team_id = 0
    for ids in idss:
        if ids['matchID'] == match_id:
            team_id = ids['teamID']

    if team_id == 0:
        result['startAtUnixTime'] = field_info['startedAtUnixTime']
        result['status'] = "InvalidMatches"
    elif int(time.time()) < field_info['startedAtUnixTime']:
        result['startAtUnixTime'] = field_info['startedAtUnixTime']
        result['status'] = "TooEarly"
    else:
        result['height'] = field_info['height']
        result['width'] = field_info['width']
        result['turn'] = field_info['turn']
        result['startedAtUnixTime'] = field_info['startedAtUnixTime']
        result['points'] = field_info['points']
        result['tiled'] = field_info['tiled']
        result['teams'] = field_info['teams']
        result['actions'] = field_info['actions']
        del result['teams'][0]['teamName'], result['teams'][1]['teamName']

    return json.loads(json.dumps(result))
