# coding=utf-8
# author: zengyuetian

from libs.data.random_data import random_peer_id, random_file_id
from libs.database.etcd_handler import del_etcd_key
from libs.database.redis_single import redis_single_delete_key
from libs.database.redis_cluster import redis_cluster_delete_key

from features.steps.ts.const import STUN_IP
from features.steps.push_hub.const import PUSH_ID


def before_scenario(context, scenario):
    context.peer_id = random_peer_id()
    context.file_id = random_file_id()

    context.peer_ids = [context.peer_id]
    context.file_ids = [context.file_id]

    if 'redis' in scenario.tags:
        context.pnic = {}  # {peer_id: stun_ip}
        redis_cluster_delete_key("PNIC_{0}".format(context.peer_id))
    if 'pnic' in scenario.tags:
        context.pnic = {}  # {peer_id: stun_ip}
        redis_cluster_delete_key("PNIC_{0}".format(context.peer_id))
    if 'rrpc' in scenario.tags:
        redis_single_delete_key("RRPC_{0}".format(STUN_IP))
    if 'pspfc' in scenario.tags:
        redis_single_delete_key("PSPFC_{0}".format(PUSH_ID))
    if 'etcd_user_p2p' in scenario.tags:
        # delete p2p/cdn set from etcd
        peer_prefix = str(context.peer_id).zfill(8)[:8]
        key_name = "/business/ops/sdk/p2p/users/{0}".format(peer_prefix)
        del_etcd_key(key_name)
    if 'etcd_httpdns_user_domain' in scenario.tags:
        context.user_id = ""
        context.user_name = ""
        context.peer_id = ""
        context.expected_host = ""
    # if 'fosc' in scenario.tags:
    #     redis_cluster_delete_key("{FOSC_{0}_{1}}".format(context.file_id, ISP_100017))
    if 'clear_pspfc' in scenario.tags:
        context.delete_key = ""
    if 'clear_rrpc' in scenario.tags:
        context.redis_key = ""


def after_scenario(context, scenario):
    if 'redis' in scenario.tags:
        for peer_id in context.peer_ids:
            redis_cluster_delete_key("PNIC_{0}".format(peer_id))
    if 'pnic' in scenario.tags:
        for peer_id in context.peer_ids:
            redis_cluster_delete_key("PNIC_{0}".format(peer_id))
    if 'rrpc' in scenario.tags:
        redis_single_delete_key("RRPC_{0}".format(STUN_IP))
    if 'pspfc' in scenario.tags:
        redis_single_delete_key("PSPFC_{0}".format(PUSH_ID))
    if 'etcd_user_p2p' in scenario.tags:
        # delete p2p/cdn set from etcd
        peer_prefix = str(context.peer_id).zfill(8)[:8]
        key_name = "/business/ops/sdk/p2p/users/{0}".format(peer_prefix)
        del_etcd_key(key_name)
    if 'etcd_httpdns_user_domain' in scenario.tags:
        user_key = "/business/httpdns/v2/users/" + context.user_id
        domain_key = "/business/httpdns/v2/domain_ip_map/" + context.user_name
        if context.user_id is not None and context.user_id is not "" \
                and context.user_name is not None and context.user_name is not "":
            del_etcd_key(domain_key)
            del_etcd_key(user_key)
        else:
            raise Exception("ETCD: key should not be null !")
    if 'clear_pspfc' in scenario.tags:
        redis_single_delete_key(get_pspfc_key(context.delete_key))
    if 'clear_rrpc' in scenario.tags:
        redis_single_delete_key(context.redis_key)


def before_feature(context, feature):
    if 'mysql_config_for_dir' in feature.tags:
        pass


def after_feature(context, feature):
    if 'mysql_config_for_dir' in feature.tags:
        pass


def get_pspfc_key(push_id):
    if push_id.upper() == "PUSH_ID":
        push_id = PUSH_ID
    return "PSPFC_{0}".format(push_id)

