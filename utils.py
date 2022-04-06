import pandas as pd


# put in here every function we will need for our dashboard



# def gen_sheet(originfile, sheetname):
#     file_dict = {key:i for i, key in enumerate(originfile.sheet_names)}
#     globals()[f"sheet{file_dict[sheetname]}"] = pd.read_excel(originfile,file_dict[sheetname])
#     globals()[f"sheet{file_dict[sheetname]}"].iloc[1,globals()[f"sheet{file_dict[sheetname]}"].columns.get_loc("Unnamed: 0")] = globals()[f"sheet{file_dict[sheetname]}"].columns[1]
#     globals()[f"sheet{file_dict[sheetname]}"].columns = globals()[f"sheet{file_dict[sheetname]}"].iloc[1]
#     globals()[f"sheet{file_dict[sheetname]}"] = globals()[f"sheet{file_dict[sheetname]}"][2:59]
#     return globals()[f"sheet{file_dict[sheetname]}"]