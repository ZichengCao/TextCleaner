import jieba
import pyperclip


class TextCleaner:

    def __init__(self, str):
        self.text = str

    def text_strip(self):
        """
        移除异常空格、换行
        """
        if TextCleaner.is_contain_chinese(text):
            # 如果是中文，则去除行内空格、行尾换行
            self.text = self.text.replace(' ', '').replace('\n', '')
        else:
            # 如果是英文，则只去除行尾换行。
            self.text = self.text.replace('\n', '')

        return self

    def punctuation_convert(self):
        """
        将英文标点符号替换成中文标点
        """
        e_pun = u',.!?()<>"\':;'
        c_pun = u'，。！？（）《》“‘：；'
        table = {ord(f): ord(t) for f, t in zip(e_pun, c_pun)}
        self.text = self.text.translate(table)
        return self

    def remove_chaos(self):
        """
        去除乱码
        """
        gbk_text_list = []

        for c in self.text:
            if not TextCleaner.if_contain_chaos(c):
                gbk_text_list.append(c)

        self.text = "".join(gbk_text_list)
        return self

    def full_to_half(self):
        """
        全角转半角
        """
        fullString = str(self.text)
        halfString = ""
        for schar in fullString:
            char_code = ord(schar)
            if char_code == 12288:
                char_code = 32
            elif (char_code >= 65281 and char_code <= 65374):
                char_code -= 65248

            halfString += chr(char_code)
        self.text = halfString
        return self

    def add_en_cn_space(self):
        """
        对英文单词、数字添加空格
        """
        list1 = list(map(lambda n: ' ' + n + ' ' if (n.encode().isalnum()) else n, jieba.cut(self.text)))
        self.text = "".join(list1).strip()
        return self

    @staticmethod
    def if_contain_chaos(text_):
        """
        判断字符是否为GBK字符，如果不是则认为是乱码。因为人眼能识别的乱码在计算机看来并没有想象中那么简单，
        “涓囧厓锛屾厛锽勬崘鐚”本身也是正常的字符，故将生僻字认为是乱码，这是一个折中的办法。
        """
        try:
            text_.encode("gb2312")
        except UnicodeEncodeError:
            return True
        return False

    @staticmethod
    def is_contain_chinese(check_str):
        """
        判断字符串中是否包含中文
        """
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False


if __name__ == '__main__':
    # text: str = """２００１年９月１７日,世 贸 组 织 中 国 工 作 组 第１８次 会 议 通 过 了 中 国 入 世 议
    # 定 书 及 附 件 和 中 国 工 作 组 报 告 书,标 志 着 我 国 加 入 世 贸 组 织 的 谈 判 全 部 结 束;
    # ２００１年１１月１０日,在 卡 塔 尔 首 都 多 哈 举 行 的 世 界 贸 易 组 织(ＷＴＯ)第 四 届
    # 部 长 级 会 议 审 议 并 通 过 了 中 国 加 入 世 界 贸 易 组 织 的 决 定。同 年１２月１１日,中 国
    # 正 式 加 入 ＷＴＯ, 成 为其第１４３个成员."""

    text: str = pyperclip.paste()
    cleaner = TextCleaner(text)
    cleaner.remove_chaos().text_strip().full_to_half().punctuation_convert().add_en_cn_space()
    pyperclip.copy(cleaner.text)
    # print(cleaner.text)
