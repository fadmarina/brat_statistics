#coding: utf-8

from collections import OrderedDict
import os
from constants import CURRENT_DIRECTORY, ALLOWED_MISTAKES, CONTENT_MISTAKES, \
    LANG_MISTAKES, NOT_AVAILABLE, UNMATCHED


def get_files_from_dir(dir_path):
    return [
        os.path.join(dir_path, fn) for fn in os.listdir(dir_path)
        if os.path.isfile(os.path.join(dir_path, fn)) and os.path.splitext(fn)[-1] == ".ann"
    ]


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


def save_table(table, file_name, folder_name="result"):
    with open(os.path.join(CURRENT_DIRECTORY, folder_name, file_name), "w") as f:
        for title, values in table.items():
            f.write("%30s  %s  %s\n" % (title, values[0], values[1]))


def get_table(s1, s2):
    table = OrderedDict([(title, [0, 0]) for title in ALLOWED_MISTAKES])
    content_count1 = 0
    lang_count1 = 0
    content_count2 = 0
    lang_count2 = 0
    for item in s1:
            mistake_title = item[1]
            if mistake_title in CONTENT_MISTAKES:
                content_count1 += 1
            if mistake_title in LANG_MISTAKES:
                lang_count1 += 1
            if mistake_title in table:
                    table[mistake_title][0] += 1

    for item in s2:
            mistake_title = item[1]
            if mistake_title in CONTENT_MISTAKES:
                content_count2 += 1
            if mistake_title in LANG_MISTAKES:
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


def save_spans(s1_copy, s2_copy, filename):
    with open(os.path.join(CURRENT_DIRECTORY, "span_results", filename), "a") as f:
        f.write("Спаны у 1го разметчика, по которым не нашлось разметки у второго:\n")
        for el in s1_copy:
            f.write(str(el) + "\n")
        f.write("_____________" + "\n")
        f.write("Спаны у 2го разметчика, по которым не нашлось разметки у первого:\n")
        for el in s2_copy:
            f.write(str(el) + "\n")
        f.write("_____________" + "\n")


def save_spans_counters(counter, counters_deleted, counters_file1_left,
                        counters_file2_left, counters_mist_type_deleted, outputfile):
    with open(os.path.join(CURRENT_DIRECTORY, "span_results", outputfile), "a") as f:
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
        for mist_type in ALLOWED_MISTAKES:
            value = counters_mist_type_deleted.get(mist_type, 0)
            f.write("\t\t%s = %s\n" % (mist_type, value))


def get_annotations_by_files_from_dir(dir_path, ann_folder_postfixes):
    """получение списка аннотаций разных разметчиков для каждого из файлов
    список имеет вид [(p1, p2,... pn), (p1, p2,... pn), ..]
    где pi - путь до файла с аннотацией одного из разметчиков. Размер n сооветствует
    количеству (разметчиков) префиксов для папок разметчиков - ann_folder_postfixes
    """
    res = []
    for fn in os.listdir(dir_path):
        if os.path.splitext(fn)[1] == ".ann":
            ann_files_for_all_postfixes = []
            for postfix in ann_folder_postfixes:
                ann_file_path = os.path.join(dir_path + postfix, fn)
                if os.path.isfile(ann_file_path):
                    ann_files_for_all_postfixes.append(ann_file_path)

            if len(ann_files_for_all_postfixes) == len(ann_folder_postfixes):
                res.append(tuple(ann_files_for_all_postfixes))
            else:
                print u"Не полный список аннотаций\n\tпостфиксы: %s\n\tфайлы: %s" % \
                      (u",".join(ann_folder_postfixes), u",".join(ann_files_for_all_postfixes))
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


def find_intersected_errors(ann_errors_dict_for_txt):
    """Поиск пересечения ошибок для всех аннотаций одного аннотируемого файла

    :return: список типа [((начало интервала, конец интервала), [список информации об ошибках
        в порядке отсортированных названий файлов аннотаций]), ...]
    """
    result = []
    # ann_type, mistake_type, begin_mist, end_mist, error_text, weight
    for index, (ann_path, errors_list) in enumerate(sorted(ann_errors_dict_for_txt.items())):
        if index == 0:
            # инициализация результата. Еслиеще не искали пересечений
            # заполняем результат как ключ - интервал ошибки, значение - список информаций об ошибках
            for error_info in errors_list:
                # такое изваращение, чтобы можно было хранить одинаковые пересечения
                key = (error_info[2], error_info[3])
                value = [error_info]
                result.append((key, value))
        else:
            # Если ищем пересечения заполняем результат как
            # ключ - интервал пересечения, значение - список информаций об ошибках
            updated_result = []
            for (res_begin_mist, res_end_mist), res_infos in result:
                for error_info in errors_list:
                    err_begin_mist, err_end_mist = error_info[2], error_info[3]

                    # полное совпадение или пересечение не менее 5 символов
                    if (res_begin_mist == err_begin_mist and res_end_mist == err_end_mist) or \
                            (min(res_end_mist, err_end_mist) - max(res_begin_mist, err_begin_mist) >= 5):
                        inter_begin_mist = max(res_begin_mist, err_begin_mist)
                        inter_end_mist = min(res_end_mist, err_end_mist)

                        # такое изваращение, чтобы можно было хранить одинаковые пересечения
                        key = (inter_begin_mist, inter_end_mist)
                        value = res_infos + [error_info]
                        updated_result.append((key, value))
            result = updated_result
    return result


def find_group_of_files(ann_folder_postfixes):
    """Функция находит адреса разных разметок одного и того же файла по всем подпапкам
    """
    annotations_by_files = []
    for dir in os.listdir(CURRENT_DIRECTORY):
        if len(dir) >= 2 and dir[-2:] not in ann_folder_postfixes:
            dir_path = os.path.join(CURRENT_DIRECTORY, dir)
            annotations_by_files += get_annotations_by_files_from_dir(dir_path, ann_folder_postfixes)
    return annotations_by_files


def get_errors_for_paths_group(paths_group):
    """Получение списка ошибок для всех файлов аннотаций в пределах
    одного аннотируемого текста

    :param paths_group: список аннотаций одного аннотируемого текста
    :return: словарь типа {"путь до файла с аннотацией": список ошибок}. Количество
        ключей соответствует количеству разметчиков
    """
    errors_list_by_ann = {}
    for file_path in paths_group:
        errors_list = []
        with open(file_path, "r") as f:
            for line in f:
                parts = line.strip().split('\t')
                ann_type = parts[0]
                error_text = parts[-1].strip()

                if ann_type.strip()[0] is "T":
                    infos = parts[1].split(' ')
                    mistake_type = infos[0]
                    if mistake_type != "Good_job":
                        begin_mist = int(infos[1])
                        end_mist = int(infos[2])
                        errors_list.append((ann_type, mistake_type, begin_mist, end_mist, error_text))

                if ann_type.strip()[0] is "A":
                    infos = parts[1].split(' ')
                    if infos[0] == "Weight":
                        mist_weight = infos[2]
                        errors_list[-1] += (mist_weight,)

        errors_list_by_ann[file_path] = errors_list
    return errors_list_by_ann
