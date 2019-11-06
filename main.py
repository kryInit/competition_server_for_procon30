import common
import matches
import matches_matchID
import update_actions as update
import initialization as init
import json
import os
import time
import schedule
from flask import *
from threading import Thread

app = Flask(__name__)  # インスタンス生成


@app.route('/initialization', methods=["POST"])
def initialization():
    print("\nnow initializing...\n")

    json_data = request.get_json()
    result_message = init.initialize_game_info(json_data)

    print("result message = " + str(result_message))

    print("\nfinished initialization!\n")

    dict_for_json_result = {'result': result_message}

    result_json = json.loads(json.dumps(dict_for_json_result))

    return json.dumps(result_json)


@app.route('/matches')
def pre_game_info():
    print("\nnow making pre-game info...\n")

    result_message = matches.make_pre_game_info(request.headers)

    print("result message = " + str(result_message))

    print("\nfinished making pre-game info!\n")

    return result_message


@app.route('/matches/<match_id>')
def game_state_info(match_id):
    print("\nnow making game state info\n")

    result_json = matches_matchID.make_game_state_info(int(match_id), request.headers)

    print("result massage = " + str(result_json))

    print("\nfinished making game state info!\n")

    return json.dumps(result_json)


@app.route('/matches/<match_id>/action', methods=["POST"])
def update_actions(match_id):
    print("\nnow updating actions...\n")

    json_data = request.get_json()
    result_json = update.update_action(json_data, match_id, request.headers)

    print("result massage = " + str(result_json))

    print("\nfinished updating actions!\n")

    return json.dumps(result_json)


@app.route('/ping')
def ping():
    if 'Authorization' not in request.headers:
        return json.loads(json.dumps({'status': 'InvalidToken'}))

    a_path = "./json/Authorization.json"
    token = request.headers['Authorization']

    if not os.path.isfile(a_path):
        return json.loads(json.dumps({'status': 'InvalidToken'}))

    with open(a_path, 'r') as f:
        auth_info = json.load(f)
    if token not in auth_info:
        return json.loads(json.dumps({'status': 'InvalidToken'}))

    return json.loads(json.dumps({'status': 'OK'}))


def run_schedule():
    a = kr()
    while 1:
        schedule.run_pending()
        time.sleep(1)
        a.add()



class kr():
    a = 1
    def add(self):
        kr.a += 1


def hogehoge():
    a = kr()
    print(a.a)
    a.add()



if __name__ == "__main__":
    schedule.every(1).seconds.do(hogehoge)
    Thread(target=run_schedule).start()

    common.remove_all_json_file()

    app.run(host='localhost', port=8000)

    common.remove_all_json_file()

