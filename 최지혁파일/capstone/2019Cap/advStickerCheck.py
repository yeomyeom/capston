


def advStickerChecker():
    adv_dir = '광고성sticker.txt'
    nonadv_dir = '비광고성sticker.txt'
    content_dir = 'content.txt'
    fread = open(adv_dir, 'r', encoding="ANSI")
    data_dir = 'picture_adv.txt'


    line = fread.readlines()
    print(line)

if __name__ == '__main__':
    advStickerChecker()