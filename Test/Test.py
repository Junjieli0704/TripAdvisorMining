#coding=utf-8

from UsefulLibs import usefulAPI
import shutil

if __name__ == '__main__':
    dst_file_fold = '../Data/HtmlData/TripAdvisorHotelInCitesHomePage/'
    src_file_fold_list = usefulAPI.get_dir_files(dst_file_fold,True)
    print src_file_fold_list
    for src_file_fold in src_file_fold_list:
        src_file_fold = src_file_fold + '/'
        file_name_list = usefulAPI.get_dir_files(src_file_fold,True)
        for file_name in file_name_list:
            shutil.move(file_name,dst_file_fold)

