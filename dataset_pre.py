def replace(file_path, website, patterns):
    oldfile = file_path + website + '/output.text.txt'
    newfile = file_path + website + '/' + website + '_output.csv'
    with open(newfile, 'w') as new_file:
        with open(oldfile) as old_file:
            for line in old_file:
                matches = [a for a in patterns if a in line]
                if len(matches) > 0:
                    new_file.write(line.replace('\n', '') + ',1\n')
                else:
                    new_file.write(line.replace('\n', '') + ',0\n')

path = 'D:/Users/asus/Desktop/crawler-master2/crawler-master/'
# dir = "boyner"
# pattern = ['mnresize/900/']
# dir = "hepsiburada"
# pattern = ['jpg,500,500', 'jpg,1000,1000']
# dir = "pierrecardin"
# pattern = ['500,649,']
dir = "trendyol"
pattern = ['415,622,']

replace(path, dir, pattern)



