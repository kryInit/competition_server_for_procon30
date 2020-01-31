import os
import json
import glob


def kill_game(match_id):
    # Authorization関係もちゃんと処理する
    f_path = "./json/" + str(match_id) + "th_field_info.json"
    if os.path.isfile(f_path):
        os.remove(f_path)

    a_path = "./json/Authorization.json"
    with open(a_path, 'r') as f:
        auth = json.load(f)

    del_token = set()
    for token, matches in auth.items():
        idx = set()
        for i in range(len(matches)):
            if str(matches[i]['matchID']) == str(match_id):
                idx.add(i)
        for i in idx:
            del matches[i]
        if not matches:
            del_token.add(token)
    for token in del_token:
        del auth[token]

    with open(a_path, 'w') as f:
        json.dump(auth, f, indent=2)


def check_authorization(rqh):
    it = json.loads(json.dumps({'status': 'InvalidToken'}))
    if 'Authorization' not in rqh:
        return it

    a_path = "./json/Authorization.json"
    token = rqh['Authorization']

    if not os.path.isfile(a_path):
        return it

    with open(a_path, 'r') as f:
        auth_info = json.load(f)
    if token not in auth_info:
        return it

    return {}


def remove_all_json_file():
    for p in glob.glob("./json/*.json"):
        if os.path.isfile(p):
            os.remove(p)
