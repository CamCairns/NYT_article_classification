import glob

nytd_section = ['Arts', 'Business', 'Obituaries', 'Sports', 'World']

for section in nytd_section:
    save_dirpath = "/Users/camcairns/Dropbox/Datasets/nyt_sections/txt_document/" + section + "/"
    paths = glob.glob(save_dirpath + '/*')
    for path in paths:
        s = open(path).read()
        s = s.replace("AdvertisementAdvertisement", " ")
        s = s.replace("advertisementadvertisement", " ")
        s = s.replace("2015", "")
        s = s.replace("This is a more complete version of the story than the one that appeared in print.", "")
        s = s.replace("PHOTO", "")
        f = open(path, 'w')
        f.write(s)
        f.close()