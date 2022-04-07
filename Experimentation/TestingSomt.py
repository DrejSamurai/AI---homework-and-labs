if __name__ == '__main__':
    snake_man_head = (0, 7)
    snake_man_body = [(0, 8), (0, 9), (0, 10)]
    snake_head_x = snake_man_head[0]
    snake_head_y = snake_man_head[1]
    new_snake_head = (snake_head_x, snake_head_y - 1)
    new_snake_body = []
    snakeBodyLen = len(snake_man_body)
    snake_tail = tuple(snake_man_body[snakeBodyLen-1])

    new_snake_body.append(snake_man_head)
    for x in range(snakeBodyLen - 1):
        new_snake_body.append(snake_man_body[x])

    new_snake_body.append(snake_tail)

    print(new_snake_head)
    print(tuple(new_snake_body))
