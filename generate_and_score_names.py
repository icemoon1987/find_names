#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################
#
# File Name:  generate_and_score_names.py
#
# Function:   
#
# Usage:  
#
# Input:  
#
# Output:	
#
# Author: wenhai.pan
#
# Create Time:    2019-02-11 16:13:14
#
######################################################

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append(".")
sys.path.append("..")
import os
import time
from datetime import datetime, timedelta
from conf import config


def decide_gender(type1, type2):

    if type1 == type2:
        return type1

    if type1 == "neutral":
        return type2

    if type2 == "neutral":
        return type1

    return "neutral"


def generate_names_by_two_concepts(first_name, concept1, concept2):

    name_results = []

    key_list = ["male", "female", "neutral"]

    for key_type1 in key_list:
        character_list1 = concept1[key_type1]

        for key_type2 in key_list:
            character_list2 = concept2[key_type2]

            for char1 in character_list1:
                for char2 in character_list2:

                    result = {}
                    result["name"] = [first_name, char1, char2]
                    result["gender"] = decide_gender(key_type1, key_type2)
                    result["concept"] = [concept1["concept"], concept2["concept"]]

                    name_results.append(result)

    return name_results


def generate_names(first_name, name_conf):
    name_results = []

    for concept1 in config.NAME_CONF:
        for concept2 in config.NAME_CONF:
            result = generate_names_by_two_concepts(first_name, concept1, concept2)
            
            name_results.extend(result)

    return name_results


def result_to_string(result):

    tmp = []
    tmp.append("".join(result["name"]))
    tmp.append(result["gender"])
    tmp.append(",".join(result["concept"]))
    tmp.append(str(result["score"]))

    return "\t".join(tmp)


def get_concept_weight(concept, name_conf):

    for name in name_conf:
        if concept == name["concept"]:
            return name["weight"]

    return 0.0


def score_single_name(name, name_conf, weight_conf):

    concept_num = len(name["concept"])

    concept_score = 0
    for concept in name["concept"]:
        concept_score += 1 * get_concept_weight(concept, name_conf) / float(concept_num)

    score = concept_score * weight_conf["concept"]

    return score


def score_names(name_results, name_conf, weight_conf):
    result = []

    for name in name_results:

        score = score_single_name(name, name_conf, weight_conf)

        name["score"] = score

        result.append(name)

    return result


def main():

    name_results = generate_names(config.FIRST_NAME, config.NAME_CONF)
    name_results = score_names(name_results, config.NAME_CONF, config.WEIGHTS)

    for result in name_results:
        print result_to_string(result)

    return


if __name__ == "__main__":
    main()


