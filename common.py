import os


def kill_game(match_id):
    # Authorization関係もちゃんと処理する
    path = "./json/" + str(match_id) + "th_field_info.json"
    os.remove(path)

