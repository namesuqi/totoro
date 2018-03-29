# coding=utf-8
# author: zengyuetian
# check if there is any peer_id is duplicated

import json

if __name__ == "__main__":
    with open("peer.json", "r") as json_file:
        seeds = json.load(json_file)["seeds"]
    print seeds

    # seeds = peer_ids["seeds"]

    ids = dict()
    for seed in seeds:
        peer_id = seed["peer_id"]
        ids[peer_id] = ids.setdefault(peer_id, 0) + 1

    print len(seeds)
    print len(ids)

    for key, value in ids.items():
        if value > 1:
            print key
    assert len(seeds) == len(ids)

