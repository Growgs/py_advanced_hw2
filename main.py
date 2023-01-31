import re
import csv
from config import phone_pattern, ext_pattern, text_pattern


def extract_contacts_list():
    with open("phonebook_raw.csv") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    temp_list = []
    for c in range(len(contacts_list)):
        if c == 0:
            temp_list.append(contacts_list[c])
        else:
            line = ",".join(contacts_list[c])
            result = re.search(text_pattern, line)
            temp_list.append(list(result.groups()))
            if temp_list[c][5] is not None:
                temp_list[c][5] = phone_pattern.sub(r"+7(\2)\3-\4-\5", temp_list[c][5])
                temp_list[c][5] = ext_pattern.sub(r" \1\2", temp_list[c][5])

    final_list = []
    for i in range(len(temp_list)):
        for s in range(len(temp_list)):
            if temp_list[i][0] == temp_list[s][0]:
                temp_list[i] = [x or y for x, y in zip(temp_list[i], temp_list[s])]
        if temp_list[i] not in final_list:
            final_list.append(temp_list[i])
    print(final_list)

    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(final_list)


if __name__ == "__main__":
    extract_contacts_list()
