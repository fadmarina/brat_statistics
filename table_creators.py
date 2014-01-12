#coding: utf-8

import csv
import os
from constants import CONTENT_MISTAKES, LANG_MISTAKES, WEIGHTS
from stat_counter import find_group_of_files, get_errors_for_paths_group, find_intersected_errors


def get_error_main_type_table(intersected_errors_for_txt, column_names, output_path,
                              create=True, print_column_names=False, add_column=None):
    mode = "w" if create else "a"
    with open(output_path, mode) as f:
        writer = csv.writer(f)
        if print_column_names:
            writer.writerow(["Совпавшие спаны"] + column_names)

        for (begin_mist, end_mist), error_infos in intersected_errors_for_txt:
            # ann_type, mistake_type, begin_mist, end_mist, error_text, weight
            row = ["%s %s %s" % (begin_mist, end_mist, error_infos[0][4])]
            for error_info in error_infos:
                error_type = error_info[1]
                if error_type in CONTENT_MISTAKES:
                    row.append("1")
                elif error_type in LANG_MISTAKES:
                    row.append("2")
                else:
                    row.append("N/A")
            if add_column:
                row.append(add_column)
            writer.writerow(row)


def get_error_weight_table(intersected_errors_for_txt, column_names, output_path,
                           create=True, print_column_names=False, add_column=None):
    mode = "w" if create else "a"
    with open(output_path, mode) as f:
        writer = csv.writer(f)
        if print_column_names:
            writer.writerow(["Совпавшие спаны"] + column_names)

        for (begin_mist, end_mist), error_infos in intersected_errors_for_txt:
            # ann_type, mistake_type, begin_mist, end_mist, error_text, weight
            row = ["%s %s %s" % (begin_mist, end_mist, error_infos[0][4])]
            for error_info in error_infos:
                try:
                    weight = error_info[5]
                except IndexError:
                    weight = None

                try:
                    index = WEIGHTS.index(weight) + 1
                except (IndexError, ValueError):
                    index = "N/A"
                row.append(index)
            if add_column:
                row.append(add_column)
            writer.writerow(row)


def get_column_names(paths_group, ann_folder_postfixes):
    columns = []
    for path in sorted(paths_group):
        dirname = os.path.dirname(path)
        postfix = dirname[-2:]
        if postfix in ann_folder_postfixes:
            columns.append(postfix)
        else:
            columns.append("_")
    return columns


def create_all_in_one_error_main_type_table(intersected_errors_for_txts, paths, columns):
    all_in_one_spans_out = os.path.join(
        os.path.dirname(__name__),
        "result",
        "AllInOneMainTypeRes.csv"
    )

    is_first_items = True
    for index, intersected_errors_for_txt in enumerate(intersected_errors_for_txts):
        get_error_main_type_table(intersected_errors_for_txt,
                                  columns + ["Файл"],
                                  all_in_one_spans_out,
                                  is_first_items,
                                  is_first_items,
                                  paths[index])
        is_first_items = False


def create_all_in_one_weight_table(intersected_errors_for_txts, paths, columns):
    all_in_one_spans_out = os.path.join(
        os.path.dirname(__name__),
        "result",
        "AllInOneWeightRes.csv"
    )

    is_first_items = True
    for index, intersected_errors_for_txt in enumerate(intersected_errors_for_txts):
        get_error_weight_table(intersected_errors_for_txt,
                               columns + ["Файл"],
                               all_in_one_spans_out,
                               is_first_items,
                               is_first_items,
                               paths[index])
        is_first_items = False


def create_tables(annotations_by_files, ann_folder_postfixes):
    intersected_errors_for_txts = []
    paths = []
    columns = []
    for index, paths_group in enumerate(annotations_by_files):
        ann_errors_dict_for_txt = get_errors_for_paths_group(paths_group)
        intersected_errors_for_txt = find_intersected_errors(ann_errors_dict_for_txt)

        if intersected_errors_for_txt:
            intersected_errors_for_txts.append(intersected_errors_for_txt)
            paths.append(paths_group[0])

        columns = get_column_names(paths_group, ann_folder_postfixes)

        path_parts = os.path.split(paths_group[0])
        main_type_out = os.path.join(
            os.path.dirname(__name__),
            "result",
            os.path.splitext(path_parts[-1])[0] + "MainType.csv"
        )
        get_error_main_type_table(intersected_errors_for_txt, columns, main_type_out, print_column_names=True)

        weight_out = os.path.join(
            os.path.dirname(__name__),
            "result",
            os.path.splitext(path_parts[-1])[0] + "Weight.csv"
        )
        get_error_weight_table(intersected_errors_for_txt, columns, weight_out, print_column_names=True)

    create_all_in_one_error_main_type_table(intersected_errors_for_txts, paths, columns)
    create_all_in_one_weight_table(intersected_errors_for_txts, paths, columns)


if __name__ == "__main__":
    postfixes = ("", "_T", "_M")
    annotations_by_files = find_group_of_files(postfixes)
    create_tables(annotations_by_files, postfixes)