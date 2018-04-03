from os.path import join

# data_set_folder = "/media/riot/5127cd94-5f74-45d1-b6e9-d7aeb19bb1d9/versions_of_projects/scriptRepo_DataSets/"
data_set_folder = "/Users/rohuntripathi/temp/Indic-Script-Recognition-RnnLib/DataSets/"

offline_word_ban_data_set = join(data_set_folder, "OfflineWordLevelStrokesRetrieved/strokesBanWord")

offline_word_hin_data_set = join(data_set_folder, "OfflineWordLevelStrokesRetrieved/strokesHinWord")

offline_word_eng_data_set = join(data_set_folder, "OfflineWordLevelStrokesRetrieved/strokesEngWord")

online_char_eng_data = join(data_set_folder, "OnlineCharLevel/DataEng")

online_char_hin_data = join(data_set_folder, "OnlineCharLevel/DataHin")
