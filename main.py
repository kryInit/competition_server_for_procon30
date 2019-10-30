import common
import matches
import matches_matchID
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

    s = request.get_json()
    result_message = init.initialize_game_info(s)

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
    return match_id


@app.route('/ping')
def ping():
    hoge = request.headers

    return str(hoge)


def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    # tmp = field_information()
    # schedule.every(1).seconds.do(tmp.hogehoge)
    # Thread(target=run_schedule).start()

    app.run(host='localhost', port=8000)

