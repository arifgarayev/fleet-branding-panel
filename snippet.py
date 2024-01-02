sample_dict = {  "key1":
                    {"key10": 5},

                "key2":
                    {"key21": 20},

                "key3":
                    {"key11": 0},

                "key4":
                    {"key20": 3}
              }


def sort_dict_by_values(dictionary):

    # keep track of key's by indecies

    keys = list(dictionary.keys())

    for key_index in range(len(keys) - 1):

        i = key_index + 1

        current = dictionary[keys[key_index]]

        while i < len(keys):

            if int(tuple(current.values())[0]) > tuple(dictionary[keys[i]].values())[0]:

                now = dictionary[keys[key_index + i]]

                dictionary[keys[key_index + i]], dictionary[keys[key_index]] = current, now

            i += 1

    return dictionary


if __name__ == '__main__':
    print(sort_dict_by_values(sample_dict))