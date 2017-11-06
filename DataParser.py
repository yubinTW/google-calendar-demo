# raw_data parser for csv-format
import csv

# return Event-dict array
def getEvents():
	result = []
	date = ''
	file = open('raw_data.csv', 'r', encoding='big5')
	csvCursor = csv.reader(file)
	for row in csvCursor:
		print(row)
		if row[1] == '':
			tmp = str.replace(row[0].split('日')[0], '年', '-')
			date = str.replace(tmp, '月', '-')
			continue
		else:
			if row[0][0].isnumeric() == False:
				continue
			event = {}
			event['datetime'] = "{}T{}:00+08:00".format(date, row[0])
			event['country'] = str.replace(row[1], '?', '').strip()
			event['title'] = row[3]
			event['actual'] = row[4]
			event['prediction'] = row[5]
			event['history'] = row[6]
			result.append(event)
	return result


if __name__ == '__main__':
	for item in getEvents():
		print(item)
