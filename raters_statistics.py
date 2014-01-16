#coding: utf-8

"""Скрипт сбора статистики по разметчикам
"""

import csv
import os
from constants import CURRENT_DIRECTORY, CONTENT_MISTAKES, LANG_MISTAKES


def find_annotations_by_postfix(postfix):
    """Получение списка аннотаций по постфиксу папки
    """
    annotations = []
    for dir in os.listdir(CURRENT_DIRECTORY):
        dir_path = os.path.join(CURRENT_DIRECTORY, dir)
        if len(dir_path) > 2 and (dir_path[-2:] == postfix or dir_path[-2] != "_"):
            for fn in os.listdir(dir_path):
                ann_file_path = os.path.join(dir_path, fn)
                if os.path.splitext(ann_file_path)[1] == ".ann" and os.path.isfile(ann_file_path):
                    annotations.append(ann_file_path)
    return annotations


def get_error_counters(ann_file_path):
    """Подсчет ошибок по их типу
    """
    content_errors = lang_errors = good_job = 0
    with open(ann_file_path, "r") as f:
        for line in f:
            parts = line.strip().split('\t')
            ann_type = parts[0]

            if ann_type.strip()[0] is "T":
                mistake_type = parts[1].split(' ')[0]
                if mistake_type != "Good_job":
                    if mistake_type in CONTENT_MISTAKES:
                        content_errors += 1
                    elif mistake_type in LANG_MISTAKES:
                        lang_errors += 1
                    else:
                        print u"Неизвестный тип ошибки %s: %s" % (ann_type, ann_file_path)
                else:
                    good_job += 1
    return content_errors, lang_errors, good_job


def collect_statistics(output_dir, postfixes):
    """Сбор статистики по постфиксам и сохранение ее в файлы папки output_dir
    """
    for postfix in postfixes:
        with open(os.path.join(output_dir, postfix + "RaterStatistics.csv"), "w") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(["File", "Content", "Language", "Total", "GoodJob"])
            total_content_errors = total_lang_errors = total_good_jobs = 0
            for file_path in find_annotations_by_postfix(postfix):
                content_errors, lang_errors, good_job = get_error_counters(file_path)
                total_content_errors += content_errors
                total_lang_errors += lang_errors
                total_good_jobs += good_job
                csv_writer.writerow([file_path, content_errors, lang_errors,
                                     content_errors + lang_errors, good_job])
            csv_writer.writerow(["", "", "", "", ""])
            csv_writer.writerow(["Overall", total_content_errors, total_lang_errors,
                                 total_content_errors + total_lang_errors, total_good_jobs])

if __name__ == "__main__":
    postfixes = ("", "_T", "_M")
    output_path = os.path.join(os.path.dirname(__name__), "result")
    collect_statistics(output_path, postfixes)
