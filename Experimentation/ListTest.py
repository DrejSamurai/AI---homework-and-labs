if __name__ == '__main__':
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    new_list = list[: int(len(list) * 0.3)]
    new_list_2 = list[int(0.3 * len(list)):int(0.6 * len(list))]
    new_list_3 = list[int(len(list) * 0.6):]


    print(new_list)
    print(new_list_2)
    print(new_list_3)
    test_list = input().split(", ")
    print(test_list)
