# coding=utf-8
# __author__ = 'liwenxuan'
"""

common functions
    1. adjust request param value and type
    2. create and switch a new random peer_id/file_id
    3. some operation about PNIC

"""

from behave import given, when
from features.steps.ts.const import *

import json
from collections import defaultdict
from libs.data.random_data import random_peer_id, random_file_id
from libs.database.redis_cluster import redis_cluster_setex_pnic, redis_cluster_delete_key

# -------------------------------------------------------------------------------------------------------------

# to support auto case invoked by different type params
typpie = {
    "str": str,
    "string": str,
    "unicode": unicode,
    "int": int,
    "long": long,
    "float": float,
    "number": int,
    "list": eval,
    "dict": eval,
    "tuple": eval,
    "bool": eval,
    "boolean": eval,
    # "set": set  # currently ignore it; set eval to list; set "([])" will get a set([')', '(', '[', ']'])
    "object": json.loads,
    "json": json.dumps
}


# modify request param(context.param), eg. /session/peers/<peer_id>
@given("set param {param} to {value} and type to {form}")
def set_param(context, param, value, form):
    if value in ("null", "None"):
        setattr(context, param, None)
    else:
        setattr(context, param, typpie[form](value))
    print("***", param, ":", getattr(context, param), "***")


# modify (context.target[field]), eg. /getseeds?pid=<peer_id> or request body {"peer_id": <peer_id>}
@given("set field {field} of {target} to {value} and type to {form}")
def set_field(context, field, target, value, form):
    if value in ("null", "None"):
        getattr(context, target)[field] = None
    else:
        getattr(context, target)[field] = typpie[form](value)
    print("***", target, ":", getattr(context, target), "***")


@given('modify the value of field "{field}" of {target} to "{value}" and type to "{form}"')
def modify_field_value_and_type(context, field, target, value, form):
    assert field in getattr(context, target).keys()
    set_field(context, field, target, value, form)


@given('add field "{field}" to {target}, value to "{value}" and type to "{form}"')
def add_new_field_to_target(context, field, target, value, form):
    assert field not in getattr(context, target).keys()
    set_field(context, field, target, value, form)


# delete fields
@given("delete field {field} of {target}")
def del_field(context, field, target):
    del getattr(context, target)[field]
    print("***", target, ":", getattr(context, target), "***")

# -------------------------------------------------------------------------------------------------------------


# create and switch to new peer_id
@given("create and change to new peer_id")
def create_new_peer_id(context):
    context.peer_id = random_peer_id()
    context.peer_ids.append(context.peer_id)


# create and switch to new file_id
@given("create and change to new file_id")
def create_new_file_id(context):
    context.file_id = random_file_id()
    context.file_ids.append(context.file_id)

# -------------------------------------------------------------------------------------------------------------


def defaults_of_peer_info(peer_id, stun_ip):
    return {
        "ttl": TTL,
        "peer_id": peer_id,
        "sdk_version": VERSION,
        "nat_type": NAT_TYPE,
        "public_ip": PUBLIC_IP,
        "public_port": PUBLIC_PORT,
        "private_ip": PRIVATE_IP,
        "private_port": PRIVATE_PORT,
        "province_id": PROVINCE_ID_310000,
        "isp_id": ISP_ID_100017,
        "city_id": CITY_ID_310100,
        "stun_ip": stun_ip
    }


@given("make sure that the peer_id is online, stun_ip is {stun_ip}")
def add_peer_info_to_pnic(context, stun_ip):
    if stun_ip.upper() == "STUN_IP":
        stun_ip = STUN_IP
    redis_cluster_setex_pnic(**defaults_of_peer_info(context.peer_id, stun_ip))

    context.pnic[context.peer_id] = stun_ip


@given("make sure that the peer_id is offline")
def delete_pnic(context):
    redis_cluster_delete_key("PNIC_{0}".format(context.peer_id))

    context.pnic.pop(context.peer_id, None)


def get_peer_id_distribution(pnic):
    # pnic = {"peer_id_1": "stun_ip", "peer_id_2": "stun_ip"}
    peer_id_distribution = defaultdict(list)
    for peer_id, stun_ip in pnic.items():
        peer_id_distribution[stun_ip].append(peer_id)
    return peer_id_distribution  # <type 'collections.defaultdict'>, {stun_1: [p1, p2], stun_2: [p3]}

# -------------------------------------------------------------------------------------------------------------


