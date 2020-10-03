import os

import requests #download images
import shutil
import imagesize #image dimensions problem: webp?
from PIL import Image
import time

import re #for getting img>src

def _timeit(method):
    def timed(self, *args, **kw):
        ts = time.time()
        result = method(self, *args, **kw)
        te = time.time()
        with open(self.project_path + '/time_logs.txt', 'a', errors='ignore') as myfile:
            myfile.write(self.project_name + '\t' + method.__name__ + '\t' + str(te - ts) + '\n')
        return result
    return timed

class io_operation:
    'dosya işlemleri sınıfı'
    def __init__(self, project_name, crawler):
        self.project_name = project_name
        self.path = os.getcwd()
        #TODO: Fix compability of the directory structure on Linux and Mac
        self.project_path = self.path + "/" + project_name + "/"
        self.project_webpath = self.project_path + "webpages/"
        if not os.path.exists(self.project_path):    
            os.mkdir(self.project_path)
        if not os.path.exists(self.project_webpath):
            os.mkdir(self.project_webpath) 
        self.crawler = crawler 

    def file_count_in_directory(self):
        return len([name for name in os.listdir(self.project_webpath) if os.path.isfile(os.path.join(self.project_webpath, name))])
    
    def save_html_file(self, html):
        sayi = self.file_count_in_directory() + 1
        fn = self.project_webpath + str(sayi).zfill(3) + ".html"
        with open(fn, "w", errors='ignore') as myfile:
            myfile.write(html)
    
    @_timeit
    def download_image(self, img_url):
        try:
            return requests.get(img_url, stream=True)
        except:
            return None

    def download_save_file(self, imgs, web_site, type, url, html):
        #directory settings
        sayi = self.file_count_in_directory()
        fn = self.project_webpath + str(sayi).zfill(3)
        if not os.path.exists(fn):
            os.mkdir(fn)

        len_html = len(html)
        
        imgs = list(set(imgs))
        imgs = [x for x in imgs if "#" not in str(x)]
        
        with open(self.project_path + 'map_url_to_number.txt', 'a', errors='ignore') as myfile:
            myfile.write(str(sayi) + '\t' + web_site + '\t' + url + '\t' + str(len_html) + '\t' + str(len(imgs)) + '\n')

        #dom-based solution, all image elements 
        temp_data = []
        for i in range(len(imgs)):
            print(">>>" + str(imgs[i]))
            src = ""
            if type == 'text-based':
                matches = re.search('src\\s*=\\s*\\\\*"(.+?)\\\\*"', imgs[i]) #TODO:Testing...
                src = matches[0]
            else: #'dom' or 'selenium':
                parent1_str, parent2_str = self.find_parent(imgs[i])
                src = self.find_src(imgs[i])
                len_attrs, bool_class, bool_id, bool_alt, bool_style, bool_align, bool_itemprop, bool_ariahidden, attr_height, attr_width = self.find_attributes(imgs[i])  
                
            if src != "": # and 'sync.search.spotxchange' not in src and 'ads.stickyadstv.com' not in src
                last_ch = src.rfind('/')
                filename = src[last_ch + 1:]
                filename = filename.replace("=", "_").replace("/", "_").replace("\\", "_").replace("?", "_").replace("&", "_").replace("%", "_").replace("?", "_").replace("\n", "").replace("*", "_").replace(":", "_").replace("!", "_").replace("|", "_")
                
                if len(filename) > 50:
                    filename = filename[-50:]

                filename = str(i).zfill(3) + "_" + filename 
                #not expected
                if os.path.exists(fn + '/' + filename):
                    filename = src[src[:last_ch-1].find('/') + 1:]
                    filename = filename.replace("=", "_").replace("/", "_").replace("\\", "_").replace("?", "_").replace("&", "_").replace("%", "_").replace("?", "_").replace("\n", "").replace("*", "").replace(":", "_").replace("!", "_").replace("|", "_")
                    filename = str(i).zfill(3) + "_" + filename

                #repair img_url
                img_url = src
                if not src.startswith("http"):
                    if '../' in src:
                        ind = src.rfind('../')
                        img_url = web_site + src[ind + 3:]
                    elif src.startswith("/"): 
                        if len(src) > 2:
                            if src[1] != '/': #to eliminate "//" 
                                img_url = web_site + src[1:]
                            else:
                                img_url = "https:" + src
                        else:
                            img_url = "https:" + src #not expected
                    else:
                        img_url = web_site + src
                    
                if not 'data:' in img_url:
                    theImg = str(imgs[i]).replace("\n", "").replace("\r", "").replace("\t", "")
                    if theImg in self.crawler.dict_img: #this url downloaded before... cache mechanism
                        if self.crawler.dict_img[theImg] != 'error': #don't search the broken link
                            img_pos, ratio_img_pos = self.find_imgpos(src, html)                            

                            #web_site, img_tag, scr, width, height, filesize, ratio, file_extension,len_scr
                            tmp_str = str(sayi) + '\t' + web_site + '\t'
                            tmp_str += str(img_pos) + '\t' + str(len_html) + '\t' + ratio_img_pos + '\t'
                            tmp_str += str(len_attrs) + '\t' + bool_class + '\t' + bool_id + '\t' + bool_style + '\t'
                            tmp_str += bool_alt + '\t' + bool_align + '\t' + bool_itemprop + '\t' + bool_ariahidden + '\t'
                            tmp_str += attr_height + '\t' + attr_width + '\t' + theImg + '\t' + parent1_str + '\t' + parent2_str + '\t 1 \t' 

                            tmp_strs = self.crawler.dict_img[theImg]
                            tmp_str += tmp_strs
                            temp_data.append(tmp_str)
                            with open(fn + '/image_urls.txt', 'a', errors='ignore') as myfile:
                                myfile.write(tmp_str + '\n')
                    else:                       
                        img_url = img_url.replace("\n", "").replace("\r", "").replace("\t", "")
                        r = self.download_image(img_url)
                        if r is not None:
                            if r.status_code == 200: #image file is ok
                                _, file_extension = os.path.splitext(img_url)

                                image_file_extensions = [".apng", ".bmp", ".gif", ".ico", ".cur", ".jpg", 
                                ".jpeg", ".jfif", ".pjpeg", ".pjp", ".png", ".svg", ".tif", ".tiff", ".webp"]

                                if file_extension not in image_file_extensions:
                                    file_extension = ".jpg"
                                    filename += ".jpg" 

                                with open(fn + '/' + filename, 'wb') as f:
                                    for chunk in r.iter_content(1024):
                                        f.write(chunk)
                                    # second stage
                                    # r.raw.decode_content = True
                                    # shutil.copyfileobj(r.raw, f)
                                
                                temp_filename = filename
                                width, height, ratio_w_h = -1, -1, -1
                                if '.svg' not in filename:
                                    try:
                                        if file_extension == '.webp':
                                            filename = filename.replace('.webp', '.png')
                                            os.system("ffmpeg -i {0} {1}".format(fn + '/' + temp_filename, fn + '/' + filename))
                                            time.sleep(1) # to find webp file size
                                        
                                        im = Image.open(fn + '/' + filename)
                                        width, height = im.size
                                        ratio_w_h = width / height
                                    except: 
                                        try:
                                            width, height = imagesize.get(fn + '/' + filename)#second library
                                            ratio_w_h = width / height
                                        except:
                                            width, height = -2, -2
                                            ratio_w_h = -2

                                filesize = os.path.getsize(fn + '/' + temp_filename)
                                img_pos, ratio_img_pos = self.find_imgpos(src, html)
                                #web_site, img_tag, scr, width, height, filesize, ratio, file_extension,len_scr
                                tmp_str = str(sayi) + '\t' + web_site + '\t'
                                tmp_str += str(img_pos) + '\t' + str(len_html) + '\t' + str(ratio_img_pos) + '\t'
                                tmp_str += str(len_attrs) + '\t' + bool_class + '\t' + bool_id + '\t' + bool_style + '\t'
                                tmp_str += bool_alt + '\t' + bool_align + '\t' + bool_itemprop + '\t' + bool_ariahidden + '\t'
                                tmp_str += attr_height + '\t' + attr_width + '\t' + theImg + '\t' + parent1_str + '\t' + parent2_str + '\t 0 \t'

                                #static members
                                tmp_strs = img_url + '\t' + str(len(img_url)) + '\t' + str(width) + '\t' + str(height) + '\t' + str(filesize) + '\t' 
                                tmp_strs += str(ratio_w_h) + '\t' + file_extension

                                tmp_str +=  tmp_strs
                                self.crawler.dict_img[theImg] = tmp_strs
                                temp_data.append(tmp_str)
                                with open(fn + '/image_urls.txt', 'a', errors='ignore') as myfile:
                                    myfile.write(tmp_str + '\n')
                            else:
                                with open(fn + '/hatalar.txt', 'a', errors='ignore') as myfile:
                                    myfile.write(">>>HATA1 Download: " + img_url + '\n')
                                print(">>>HATA1 Download: " + img_url)
                                self.crawler.dict_img[theImg] = "error"
                        else:
                            with open(fn + '/hatalar.txt', 'a', errors='ignore') as myfile:
                                myfile.write(">>>HATA2 not image file: " + img_url + '\n')
                            print(">>>HATA2 not image file: " + img_url)
                            self.crawler.dict_img[theImg] = "error"
        return temp_data

    @_timeit
    def find_parent(self, theImg):
        parent1_str, parent2_str = '', ''
        try:
            parent1 = theImg.findParent()
            parent1_str = str(parent1)
            parent1_str = parent1_str[:parent1_str.find('>') + 1] #parent tag
            parent1_str = parent1_str.replace("\n", "").replace("\r", "").replace("\t", "")
        except:
            parent1_str = ''
        else:
            try:
                parent2 = parent1.findParent()
                parent2_str = str(parent2)
                parent2_str = parent2_str[:parent2_str.find('>') + 1] #parent tag
                parent2_str = parent2_str.replace("\n", "").replace("\r", "").replace("\t", "")
            except:
                parent2_str = ''
        return parent1_str, parent2_str
    
    @_timeit
    def find_src(self, theImg):
        src = ''
        if 'src' in theImg.attrs:
            src = theImg['src'] #get a src attributes of the element
            if src == "" or "data:image/gif" in src:
                if 'data-src' in theImg.attrs:
                    src = theImg['data-src']
                elif 'srcset' in theImg.attrs:
                    tmp = theImg['srcset']
                    src = tmp.split(',')[-1].strip()
                    if ' ' in src:
                        src = src[:src.find(' ') + 1]
                elif 'data-srcset' in theImg.attrs:
                    tmp = theImg['data-srcset']
                    src = tmp.split(',')[-1].strip()
                    if ' ' in src:
                        src = src[:src.find(' ') + 1]
        else:
            if 'data-src' in theImg.attrs:
                src = theImg['data-src']
            elif 'srcset' in theImg.attrs:
                tmp = theImg['srcset']
                src = tmp.split(',')[-1].strip()
                if ' ' in src:
                    src = src[:src.find(' ') + 1]
            elif 'data-srcset' in theImg.attrs:
                tmp = theImg['data-srcset']
                src = tmp.split(',')[-1].strip()
                if ' ' in src:
                    src = src[:src.find(' ') + 1]
        return src
    
    @_timeit
    def find_attributes(self, theImg):
        len_attrs = len(theImg.attrs)
        bool_class = "1" if "class" in theImg.attrs else "0"
        bool_id = "1" if "id" in theImg.attrs else "0"
        bool_alt= "1" if "alt" in theImg.attrs else "0"
        bool_style= "1" if "style" in theImg.attrs else "0"
        bool_align= "1" if "align" in theImg.attrs else "0"
        bool_itemprop= "1" if "itemprop" in theImg.attrs else "0"
        bool_ariahidden= "1" if "aria-hidden" in theImg.attrs else "0"
        attr_height = "-1" if "height" not in theImg.attrs else str(theImg['height']).replace('px', '').replace('%', '').replace('auto', '').strip()
        attr_width = "-1" if "width" not in theImg.attrs else str(theImg['width']).replace('px', '').replace('%', '').replace('auto', '').strip()

        if attr_height == "-1" or attr_width == "-1":
            tmpstr = str(theImg).replace("\n", "").replace("\r", "").replace("\t", "")
            pos1 = tmpstr.find('style="')
            if pos1 > 0:
                tmpstr = tmpstr[pos1+7:]
                pos1 = tmpstr.find('"')
                tmpstr = tmpstr[:pos1]
                if attr_width == "-1":
                    attr_width = parse_style(tmpstr, 'width')
                if attr_height == "-1":
                    attr_height = parse_style(tmpstr, 'height')
        
        attr_width=re.sub("[^0-9]", "", attr_width)
        attr_height=re.sub("[^0-9]", "", attr_height)

        attr_width= '-1' if attr_width.strip() == '' else attr_width
        attr_height= '-1' if attr_height.strip() == '' else attr_height
        #
        attr_width = str(int(float(attr_width)))
        attr_height = str(int(float(attr_height)))
        if int(attr_width) > 3000: attr_width = "3000"
        if int(attr_height) > 3000: attr_height = "3000" #normalization

        return len_attrs, bool_class, bool_id, bool_alt, bool_style, bool_align, bool_itemprop, bool_ariahidden, attr_height, attr_width
    
    @_timeit
    def find_imgpos(self, src, html):
        len_html = len(html)
        tmp_src = src
        pos = tmp_src.find('/')
        pos = tmp_src.find('/', pos + 1)
        pos = tmp_src.find('/', pos + 1) #third /
        tmp_src = tmp_src[pos + 1:]
        img_pos = html.replace('&amp;', '&').find(tmp_src)
        ratio_img_pos = "-1" if img_pos == -1 else str(img_pos / len_html)
        return img_pos, ratio_img_pos

    def save_extraction_results(self, rows, filename="outputs"):
        fn = self.project_path + filename + ".txt"
        with open(fn, "a", errors='ignore') as myfile:
            for row in rows:
                if row != None:
                    myfile.write(row + "\n")

    def preparedatatoSave(self, result):
        'data preaparing to save, rows, simple csv file'
        temp = []
        for key in result.keys():
            if len(temp) == 0:
                temp = result[key]
            else:
                for ind in range(len(result[key])):
                    try:
                        temp[ind] += "\t" + result[key][ind]
                    except:
                        continue
        return temp

def parse_style(tmpstr, attr = 'width'):     
    pos1 = tmpstr.find(attr) 
    if pos1 > -1:
        tmpw = tmpstr[pos1 + len(attr) + 1:]
        pos1 = tmpw.find(';')
        if pos1 > -1:
            tmpw = tmpw[:pos1]
        l = re.findall(r"[-+]?\d*\.\d+|\d+", tmpw)
        if len(l) > 0:
            s = '-1'
            if l[0].strip() == '':
                if len(l) > 1:
                    s = l[1].strip()
                    if s == '':
                        s = '-1'
                else:
                    s = '-1'
            else:
                s = l[0].strip()
            return s
    return '-1'