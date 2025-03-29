from itertools import chain
from functools import reduce, partial


def time_to_millisec(time):
    time_str = str(time)
    if time == "NaN":
        return "0"
    else:
        time_pair = str.split(time_str, ".")
        sec = time_pair[0]
        milli_sec = time_pair[1] if len(time_pair) == 2 else "0"
        milli_sec = f"{milli_sec:0<3}" if len(milli_sec) < 3 else milli_sec
        milli_sec = milli_sec[0:3] if len(milli_sec) > 3 else milli_sec
        merged_milli_sec = int(sec) * 1000 + int(milli_sec)

        return f"{merged_milli_sec}"


def norm_time(ann):
    milli_start = time_to_millisec(ann["start"])
    milli_end = time_to_millisec(ann["end"])
    return {**ann, "start": milli_start, "end": milli_end}


def norm_nms(nms_tup):
    nms_type = nms_tup[0]
    nms_list = nms_tup[1]
    return map(lambda ann: {**ann, "ann_value": nms_type}, nms_list)


def get_nms_anns(nms_obj: dict):
    nms_list = nms_obj.items() if nms_obj else [("key", None)]
    activated_nms = filter(lambda key_val: key_val[1], nms_list)
    flatten_activated = list(chain(*map(norm_nms, activated_nms)))
    return list(flatten_activated)


def slots_reducer(acc, cur):
    start = cur["start"]
    end = cur["end"]
    return [*acc, start, end]


def norm_slot(idx_slot):
    idx = idx_slot[0]
    slot_id = f"ts{idx+1}"
    slot = idx_slot[1]
    return (slot, slot_id)


def add_slot_refs(time_slot_map, ann):
    start = ann["start"]
    end = ann["end"]
    slot_ref1 = time_slot_map[start]
    slot_ref2 = time_slot_map[end]
    return {**ann, "slot_ref1": slot_ref1, "slot_ref2": slot_ref2}


def add_ann_value(ann):
    gloss_id = ann["gloss_id"]
    ann_value = gloss_id
    return {**ann, "ann_value": ann_value}


def add_ann_id(start_id, idx_ann):
    idx, ann = idx_ann
    return {"ann_id": f"a{idx + start_id}", **ann}


def to_elan_obj(obj):

    ko_snt = obj["krlgg_sntenc"]["koreanText"]
    ksl_gloss = obj["sign_lang_sntenc"]

    strong_anns = obj["sign_script"]["sign_gestures_strong"] or []
    strong_anns = map(norm_time, strong_anns)
    strong_anns = [*map(add_ann_value, strong_anns)]

    weak_anns = obj["sign_script"]["sign_gestures_weak"] or []
    weak_anns = map(norm_time, weak_anns)
    weak_anns = [*map(add_ann_value, weak_anns)]

    nms_anns = get_nms_anns(obj["nms_script"])
    nms_anns = [*map(norm_time, nms_anns)]

    anns = strong_anns + weak_anns + nms_anns

    time_slot_keys = sorted(list(set(reduce(slots_reducer, anns, []))))

    if len(time_slot_keys) < 2:
        time_slot_keys = [
            *time_slot_keys,
            "4000",
        ]  # 주석이 안되어 있는 자료 처리를 위해

    time_slot_map = dict(map(norm_slot, enumerate(time_slot_keys)))

    first_slot_ref = time_slot_map[time_slot_keys[0]]
    last_slot_ref = time_slot_map[time_slot_keys[-1]]

    strong_anns = sorted(
        map(partial(add_slot_refs, time_slot_map), strong_anns),
        key=lambda ann: int(ann["start"]),
    )
    weak_anns = sorted(
        map(partial(add_slot_refs, time_slot_map), weak_anns),
        key=lambda ann: int(ann["start"]),
    )
    nms_anns = sorted(
        map(partial(add_slot_refs, time_slot_map), nms_anns),
        key=lambda ann: int(ann["start"]),
    )

    strong_start_id = 3
    weak_start_id = strong_start_id + len(strong_anns)
    nms_start_id = weak_start_id + len(weak_anns)

    ms_strong = [
        *map(
            partial(add_ann_id, strong_start_id),
            enumerate(strong_anns),
        )
    ]

    ms_weak = [
        *map(
            partial(add_ann_id, weak_start_id),
            enumerate(weak_anns),
        )
    ]

    nms_script = [
        *map(
            partial(add_ann_id, nms_start_id),
            enumerate(nms_anns),
        )
    ]

    def nms_type_reducer(acc, cur):
        nms_type = f'nms_{cur["ann_value"]}'
        acc[nms_type] = acc[nms_type] if nms_type in acc else []
        acc[nms_type] = [*acc[nms_type], cur]
        return acc

    nms_script_dict = reduce(nms_type_reducer, nms_script, dict())

    ko_snt = [
        {
            "ann_id": "a1",
            "slot_ref1": first_slot_ref,
            "slot_ref2": last_slot_ref,
            "ann_value": ko_snt,
        }
    ]
    ksl_gloss = [
        {
            "ann_id": "a2",
            "slot_ref1": first_slot_ref,
            "slot_ref2": last_slot_ref,
            "ann_value": ksl_gloss,
        }
    ]

    elan_obj = {
        "time_slots": time_slot_map.items(),
        "ko": ko_snt,
        "ksl_simple": ksl_gloss,
        "nms": nms_script_dict,
        "ms_strong": ms_strong,
        "ms_weak": ms_weak,
    }

    return elan_obj
