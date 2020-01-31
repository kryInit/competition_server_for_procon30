import common
import copy
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

    saut = field_info['startedAtUnixTime']
    ims = field_info['intervalMillis']
    tms = field_info['turnMillis']
    turn = field_info['turns']
    if team_id == 0:
        result['startAtUnixTime'] = saut
        result['status'] = "InvalidMatches"
    elif int(time.time()) < saut:
        result['startAtUnixTime'] = saut
        result['status'] = "TooEarly"
    elif (time.time()-saut)/((tms+tms)/1000) > turn or (time.time()-saut)%((tms+ims)/1000) >= tms/1000:
        result['startAtUnixTime'] = saut
        result['status'] = "UnacceptableTime"
    else:
        result = write_actions(match_id, team_id, json_data, field_info)

    return result


def write_actions(match_id, team_id, json_data, field_info):
    tpath = "./json/" + str(match_id) + "-" + str(team_id) + "_tmp_actions_executed.json"
    tmp_result_actions = {'actions': field_info['actions']}
    result_actions = {'actions': []}
    tmp_actions = {}
    agent_ids = set()

    if os.path.isfile(tpath):
        with open(tpath, 'r') as f:
            tmp_actions = json.load(f)

    for team in field_info['teams']:
        if team['teamID'] == team_id:
            for agent in team['agents']:
                agent_ids.add(agent['agentID'])

    for i in range(len(tmp_result_actions['actions'])):
        if tmp_result_actions['actions'][i]['agentID'] in agent_ids:
            del tmp_result_actions['actions'][i]['apply']
            result_actions['actions'].append(tmp_result_actions['actions'][i])

    if 'actions' not in json_data:
        for agent_id, action in tmp_actions.items():
            if int(agent_id) in agent_ids:
                tmp = action
                tmp['agentID'] = agent_id
                tmp['turn'] = field_info['turn']
                result_actions['actions'].append(tmp)
        return result_actions

    actions_data = json_data['actions']

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

        if (agent_id not in agent_ids) or (type != "move" and type != "remove" and type != "stay") or (max(abs(dy), abs(dx)) > 1) or (type == "stay" and (dy != 0 or dx != 0)):
            continue

        tmp_actions[str(agent_id)] = {'type': type, 'dy': dy, 'dx': dx, 'turn': field_info['turn']}

    for agent_id, action in tmp_actions.items():
        tmp = copy.deepcopy(action)
        tmp['agentID'] = agent_id
        result_actions['actions'].append(tmp)

    with open(tpath, mode='w') as f:
        json.dump(tmp_actions, f, indent=2)

    return result_actions
