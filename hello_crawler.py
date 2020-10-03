import crawler as cr

#one rule file, no thread
cr.crawler('rules_20minutos-es.json')


# from threading import Thread
# import os 

#for all rule files
# def crawl2(my_list):
#     for the_l in my_list:
#         cr.crawler('000//' + the_l)

# l0 = os.listdir('000/')
# l01 = l0[:2]
# l02 = l0[2:]
# l03 = l0[4:6]
# l04 = l0[6:]
# l05 = l0[8:10]
# l06 = l0[10:12]
# l07 = l0[12:14]
# l08 = l0[14:16]
# l09 = l0[16:18]
# l10 = l0[18:]


# t1 = Thread(target = crawl2, args = (l01,))
# t2 = Thread(target = crawl2, args = (l02,))
# t3 = Thread(target = crawl2, args = (l03,))
# t4 = Thread(target = crawl2, args = (l04,))
# t5 = Thread(target = crawl2, args = (l05,))
# t6 = Thread(target = crawl2, args = (l06,))
# t7 = Thread(target = crawl2, args = (l07,))
# t8 = Thread(target = crawl2, args = (l08,))
# t9 = Thread(target = crawl2, args = (l09,))
# t10 = Thread(target = crawl2, args = (l10,))

# t1.start()
# t2.start()
# t3.start()
# t4.start()
# t5.start()
# t6.start()
# t7.start()
# t8.start()
# t9.start()
# t10.start()