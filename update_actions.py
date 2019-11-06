import common
import json
import time
import os


def update_action(json_data, match_id, rqh):
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
        if str(ids['matchID']) == str(match_id):
            team_id = ids['teamID']

    if team_id == 0:
        result['startAtUnixTime'] = field_info['startedAtUnixTime']
        result['status'] = "InvalidMatches"
    elif int(time.time()) < field_info['startedAtUnixTime']:
        result['startAtUnixTime'] = field_info['startedAtUnixTime']
        result['status'] = "TooEarly"
    # UnacceptableTimeを追加しておく
    else:
        result = write_actions(match_id, team_id, json_data, field_info)

    return result


def write_actions(match_id, team_id, json_data, field_info):
    if 'actions' not in json_data:
        return {}

    path = "./json/" + str(match_id) + "-" + str(team_id) + "_actions_executed.json"
    tpath = "./json/"+ str(match_id) + "-" + str(team_id) + "_tmp_actions_executed.json"
    result_actions = {'actions': []}
    tmp_actions = {}
    actions_data = json_data['actions']
    agent_ids = set()

    if os.path.isfile(path):
        with open(path, 'r') as f:
            result_actions = json.load(f)

    if os.path.isfile(tpath):
        with open(tpath, 'r') as f:
            tmp_actions = json.load(f)


    for team in field_info['teams']:
        if team['teamID'] == team_id:
            for agent in team['agents']:
                agent_ids.add(agent['agentID'])

    for action in actions_data:
        keys = ['agentID', 'type', 'dx', 'dy']

        invalid_key = False
        for key in keys:
            if key not in action:
                invalid_key = True

        if invalid_key:
            continue

        agent_id = action['agentID']
        type = action['type']
        dy = action['dy']
        dx = action['dx']

        if (agent_id not in agent_ids) or (type != "move" and type != "remove") or (max(abs(dy), abs(dx)) > 1):
            continue

        tmp = {'agentID': agent_id, 'type': type, 'dy': dy, 'dx': dx, 'turn': field_info['turn']}
        tmp_actions[str(agent_id)] = {'type': type, 'dy': dy, 'dx': dx}

    with open(tpath, mode='w') as f:
        json.dump(tmp_actions, f, indent=2)

    for k, v in tmp_actions.items():
        tmp = {'agentID': k}
        tmp.update(v)
        tmp['turn'] = field_info['turn']
        result_actions['actions'].append(tmp)

    return result_actions
