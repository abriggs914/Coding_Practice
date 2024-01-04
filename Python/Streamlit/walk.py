import os


# def collect_all_files(root):
#     walked = list(os.walk(root))
#     all_files = []
#
#     for root, directories, files in walked:
#         for file in files:
#             abs_path = os.path.normpath(f"{root}/{file}")
#             if os.path.isfile(abs_path):
#                 all_files.append(abs_path)
#
#     return all_files


def collect_all_files(root):
    walked = os.walk(root)
    all_files = []

    for root, directories, files in walked:
        all_files += [os.path.normpath(f"{root}/{file}") for file in files]

    return all_files


pth = r"\\nas1\Public\IT\Instructions"

if __name__ == '__main__':

    files = collect_all_files(pth)
    # files2 = collect_all_files2(pth)

    print(f"{len(files)=}")
    # print(f"{len(files2)=}")
