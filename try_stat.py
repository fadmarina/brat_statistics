#coding: utf-8
from collections import OrderedDict, Counter
from os import listdir
from os.path import isfile, join, splitext, exists

NOT_AVAILABLE = "n/a"
UNMATCHED = "unmatched"
current_directory = "C:\LTC\\brat_sources\\"
allowed_mistakes = [
    "Content",
        "content_reference",
            "omission",
            "non-sense",
        "content_cohesion",
            "theme",
            "rheme",
            "connector",
            "logic",
        "content_pragmatics",
            "register",
            "use",
    "Language",
    "Language_lexical",
        "lexical",
        "combinability",
    "Language_morphology",
    "Language_syntax",
        "incomplete_structure",
        "ungrammatical",
        "word_order",
    "Laguage_spelling",
        "capitals",
    "Language_punctuation",
    "Delete",
    "All:",
    "Content:",
    "Language:"
]

lang_mistakes = [
    "Language",
    "Language_lexical",
        "lexical",
        "combinability",
    "Language_morphology",
    "Language_syntax",
        "incomplete_structure",
        "ungrammatical",
        "word_order",
    "Laguage_spelling",
        "capitals",
    "Language_punctuation",
    "Delete"
]

content_mistakes = [
    "Content",
        "content_reference",
            "omission",
            "non-sense",
        "content_cohesion",
            "theme",
            "rheme",
            "connector",
            "logic",
        "content_pragmatics",
            "register",
            "use"
]


def get_files_from_dir(dir_path):
    return [join(dir_path, fn) for fn in listdir(dir_path) if isfile(join(dir_path, fn)) and splitext(fn)[-1] == ".ann"]


def get_tech(tech1, tech2):
    technology_val = ["background_info", "SL", "too_literal", "too_free", "proper_name", "TL"]
    table = OrderedDict([(title, [0, 0]) for title in technology_val])
    for item in tech1:
            tech_title = item[2]
            if tech_title in table:
                    table[tech_title][0] += 1

    for item in tech2:
            tech_title = item[2]
            if tech_title in table:
                    table[tech_title][1] += 1
    print table
    return table


def save_tech_table(table, file_name):
        with open(current_directory + "results_tech\\"+file_name, "w") as f:
                for title, values in table.items():
                        f.write("%30s  %s  %s\n" % (title, values[0], values[1]))


def get_table(s1, s2):
    table = OrderedDict([(title, [0, 0]) for title in allowed_mistakes])
    content_count1 = 0
    lang_count1 = 0
    content_count2 = 0
    lang_count2 = 0
    for item in s1:
            mistake_title = item[1]
            if mistake_title in content_mistakes:
                content_count1 += 1
            if mistake_title in lang_mistakes:
                lang_count1 += 1
            if mistake_title in table:
                    table[mistake_title][0] += 1

    for item in s2:
            mistake_title = item[1]
            if mistake_title in content_mistakes:
                content_count2 += 1
            if mistake_title in lang_mistakes:
                lang_count2 += 1
            if mistake_title in table:
                    table[mistake_title][1] += 1
    table["All:"][0] = len(s1)
    table["All:"][1] = len(s2)
    table["Content:"][0] = str(content_count1)
    table["Content:"][1] = str(content_count2)
    table["Language:"][0] = str(lang_count1)
    table["Language:"][1] = str(lang_count2)
    return table


def save_table(table, file_name):
        with open(current_directory + "results\\"+file_name, "w") as f:
                for title, values in table.items():
                        f.write("%30s  %s  %s\n" % (title, values[0], values[1]))


def save_spans(s1_copy, s2_copy, filename):
    with open(current_directory + "span_results\\"+filename, "a") as f:
        f.write("Спаны у 1го разметчика, по которым не нашлось разметки у второго:\n")
        for el in s1_copy:
            f.write(str(el) + "\n")
        f.write("_____________" + "\n")
        f.write("Спаны у 2го разметчика, по которым не нашлось разметки у первого:\n")
        for el in s2_copy:
            f.write(str(el) + "\n")
        f.write("_____________" + "\n")


def save_spans_counters(counter, counters_deleted, counters_file1_left, counters_file2_left, counters_mist_type_deleted, outputfile):
    with open(current_directory + "span_results\\"+outputfile, "a") as f:
        f.write("Всего грубо совпавших спанов:" + str(counter) + "\n")
        f.write("Счетчики весов совпавших спанов:\n")
        for weight, value in counters_deleted.items():
            f.write("\t\t%s = %s\n" % (weight, value))
        f.write("Счетчики весов несовпавших спанов:\n")
        f.write("\tФайл ***:\n")
        for weight, value in counters_file1_left.items():
            f.write("\t\t%s = %s\n" % (weight, value))
        f.write("\tФайл T:\n")
        for weight, value in counters_file2_left.items():
            f.write("\t\t%s = %s\n" % (weight, value))
        f.write("Счетчики всех подряд типов в совпавших спанах:\n")
        for mist_type in allowed_mistakes:
            value = counters_mist_type_deleted.get(mist_type, 0)
            f.write("\t\t%s = %s\n" % (mist_type, value))


def get_comparers_from_dir(dir_path):
    res = []
    for fn in listdir(dir_path):
        fn_path = join(dir_path, fn)
        fn_from_T_path = join(dir_path + "_T", fn)
        if isfile(fn_path) and splitext(fn)[-1] == ".ann" and exists(fn_from_T_path):
            res.append((fn_path, fn_from_T_path))
    return res


def get_weight_name(item, weight_index=4):
    try:
        item_weight = item[weight_index]
    except IndexError:
        item_weight = NOT_AVAILABLE
    return item_weight


def get_removing_spans_weight(item1, items2):
    item1_weight = get_weight_name(item1)
    if item1_weight == NOT_AVAILABLE:
        return item1_weight

    for item2 in items2:
        item2_weight = get_weight_name(item2)
        if item1_weight != item2_weight:
            if item2_weight == NOT_AVAILABLE:
                return item2_weight
            return UNMATCHED
    return item1_weight


def get_removing_spans_mistake_types(item1, items2):
    list_of_types = []
    list_of_types.append(item1[1])
    for item2 in items2:
        list_of_types.append(item2[1])
    return list_of_types


def span_good_mistakes(s1, s2, outputfile):
    s1_copy = s1[:]
    s2_copy = s2[:]
    counters_deleted = Counter()
    counters_mist_type_deleted = Counter()

    matches = {}
    counter = 0
    counter_of_types = 0
    for item1 in s1_copy:
            matches[item1] = []
            for item2 in s2_copy:
                    if item1[2] <= item2[2]:
                            first_left = item1[2]
                            first_right = item1[3]
                            second_left = item2[2]
                            second_right = item2[3]
                    else:
                            first_left = item2[2]
                            first_right = item2[3]
                            second_left = item1[2]
                            second_right = item1[3]


                    if (first_right >= second_right and second_right - second_left >= 1) or (first_right < second_right and first_right - second_left >= 1):
                            matches[item1].append(item2)

    from pprint import pprint
    pprint(matches)

    for item1, items2 in matches.items():
        if items2:
            add = False
            for item2 in items2:
                if item2[1] == item1[1]:
                    counter_of_types += 1
                try:
                    s2_copy.remove(item2)
                except ValueError:
                    # item2 уже удален из s2_copy
                    pass
                else:
                    add = True

            s1_copy.remove(item1)
            if add:
                counter += 1

                removing_spans_weight = get_removing_spans_weight(item1, items2)
                counters_deleted[removing_spans_weight] += 1

                removing_spans_mist_type = get_removing_spans_mistake_types(item1, items2)
                for type in removing_spans_mist_type:
                    counters_mist_type_deleted[type] += 1
                    if type in lang_mistakes:
                        counters_mist_type_deleted["Language:"] += 1
                    elif type in content_mistakes:
                        counters_mist_type_deleted["Content:"] += 1
                    counters_mist_type_deleted["All:"] += 1

    def get_left_weights_counters(s):
        file_counter_left = Counter()
        for item in s:
            item_weight = get_weight_name(item)
            file_counter_left[item_weight] += 1
        return file_counter_left

    # print s1_copy
    # print s2_copy
    # print counter
    counters_file1_left = get_left_weights_counters(s1_copy)
    counters_file2_left = get_left_weights_counters(s2_copy)
    save_spans(s1_copy, s2_copy, outputfile)
    save_spans_counters(counter, counters_deleted, counters_file1_left, counters_file2_left, counters_mist_type_deleted, outputfile)

if __name__ == "__main__":
    results = []
    source_dir = current_directory
    for dir in listdir(source_dir):
        if not dir.endswith("_T"):
            results += get_comparers_from_dir(source_dir+dir)

    print results

        #собираем из каждой пары файлов  наборы тэгов
    for pair_of_files in results:
        s1 = []
        tech1 = []

        f = open(pair_of_files[0], "r")
        for line in f:
            parts = line.strip().split('\t')
            ann_type = parts[0]
            if ann_type.strip()[0] is "T":
                infos = parts[1].split(' ')
                mistake_type = infos[0]
                if  mistake_type != "Good_job":
                    begin_mist = int(infos[1])
                    end_mist = int(infos[2])
                    s1.append((ann_type, mistake_type, begin_mist, end_mist))

            if ann_type.strip()[0] is "A":
                infos = parts[1].split(' ')
                if infos[0] == "Technology":
                    mist_code = infos[1]
                    mist_source = infos[2]
                    tech1.append((ann_type, mist_code, mist_source))

                if infos[0] == "Weight":
                    mist_code = infos[1]
                    mist_weight = infos[2]
                    s1[-1] += (mist_weight, )
        #print tech1

        #print "Разметчик 1%s  ", s1
        f.close()

        s2 = []
        tech2 = []
        f = open(pair_of_files[1], "r")
        for line in f:
            parts = line.strip().split('\t')
            ann_type = parts[0]
            if ann_type.strip()[0] is "T":
                infos = parts[1].split(' ')
                mistake_type = infos[0]
                if  mistake_type != "Good_job":
                    begin_mist = int(infos[1])
                    end_mist = int(infos[2])
                    s2.append((ann_type, mistake_type, begin_mist, end_mist))

            if ann_type.strip()[0] is "A":
                infos = parts[1].split(' ')
                if infos[0] == "Technology":
                    mist_code = infos[1]
                    mist_source = infos[2]
                    tech2.append((ann_type, mist_code, mist_source))

                if infos[0] == "Weight":
                    mist_code = infos[1]
                    mist_weight = infos[2]
                    s2[len(s2)-1] += (mist_weight, )
        #print tech2

        #print "Разметчик 2%s  ", s2
        f.close()

        #количество совпавших спанов
        spans_out = pair_of_files[0].split("\\")[4]+"SpanRes.txt"
        span_good_mistakes(s1, s2, spans_out)

        output = pair_of_files[0].split("\\")[4]+"Res.txt"
        print output
        table = get_table(s1,s2)
        print table
        save_table(table,output)

        tech_output = pair_of_files[0].split("\\")[4]+"Tech.txt"
        tech_table = get_tech(tech1, tech2)
        save_tech_table(tech_table, tech_output)