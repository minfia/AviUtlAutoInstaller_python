# -*- coding: utf-8 -*-


def __read_ini_file(ini_file_path):
    """iniファイルを読み出し、読み出した行をリストで返す
    Parameters
    ----------
    ini_file_path : str
        iniファイルのフルパス
    Returns
    -------
        lines : 読み出した行のリスト
    """
    lines = []
    with open(ini_file_path, encoding = "shift_jis") as fp:
        while True:
            line = fp.readline().rstrip("\r\n")
            if line == "":
                break
            lines.append(line)
    return lines

def __write_ini_file(ini_file_path, lines):
    """iniファイルを書き出す
    Parameters
    ----------
    ini_file_path : str
        iniファイルのフルパス
    lines : list
        iniファイルに書き出す内容のリスト
    """
    # iniファイルに書き出し(上書き)
    with open(ini_file_path, "w", encoding = "shift_jis") as fp:
        for l in lines:
            fp.write(l + "\n")

def add_param(ini_file_path, section, param_list):
    """iniファイルのセクションにパラメータを追加する
    セクションが存在しない場合は、セクションごと追加する
    Parameters
    ----------
    ini_file_path : str
        iniファイルのフルパス
    section : str
        iniファイルのセクション名([]で括ること)
    param_list : list
        iniファイルのパラメータ
    """
    lines = []
    lines = __read_ini_file(ini_file_path)

    file_line_count = len(lines)

    # セクションの記述位置を検索
    section_pos = 0
    for line in lines:
        if section in line:
            break
        section_pos += 1
    if file_line_count == section_pos:
        # セクションが存在しない
        lines.append(section)
        lines.extend(param_list)
    else:
        # セクションが存在する
        section_pos += 1
        lines[section_pos:section_pos] = param_list

    __write_ini_file(ini_file_path, lines)

def update_param(ini_file_path, section, option, value):
    """iniファイルのセクションのパラメータを変更する
    セクションまたはパラメータが存在しない場合は、追加する
    Parameters
    ----------
    ini_file_path : str
        iniファイルのフルパス
    section : str
        iniファイルのセクション名([]で括ること)
    option : str
        パラメータのオプション名
    value
        optionに紐付けられる値
    """
    lines = []
    lines = __read_ini_file(ini_file_path)

    file_line_count = len(lines)

    section_pos = 0
    for line in lines:
        if section in line:
            break
        section_pos += 1

    if file_line_count == section_pos:
        # セクションが存在しない
        lines.append(section)
        lines.extend(["{0}={1}".format(option, value)])
    else:
        # セクションが存在する

        # セクション間の位置を取得
        next_section_pos = section_pos + 1
        for line in lines[section_pos:len(lines)]:
            if "[" in line:
                break
            next_section_pos += 1
        # 追加するパラメータが存在するか検索
        param_pos = section_pos + 1
        for line in lines[section_pos:next_section_pos]:
            if option in line:
                break
            param_pos += 1
        if not param_pos == next_section_pos:
            # パラメータが存在する
            lines.pop(param_pos - 1)
        lines[section_pos + 1:section_pos + 1] = (["{0}={1}".format(option, value)])

    __write_ini_file(ini_file_path, lines)

def main():
    pass

if __name__ == "__main__":
    main()

