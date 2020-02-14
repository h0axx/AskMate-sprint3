def export_data(filename, data):
    with open(filename,'w') as datafile:
        for list in data:
            loop = 0
            for string in list:
                list[loop] = string.replace(',','<&>')
                list[loop] = list[loop].replace('\r\n','<br>')
                loop+=1

            datafile.write(','.join(list) + '\n')

def import_data(filename):
    result = []
    with open(filename, 'r') as datafile:
        for list in datafile.readlines():
            result.append(list.strip().split(','))
        for list in result:
            loop = 0
            for string in list:
                list[loop] = string.replace('<&>',',')
                list[loop] = list[loop].replace('<br>','\r\n')
                loop += 1

        return result


