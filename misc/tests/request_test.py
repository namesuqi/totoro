def test_if(idsss, illegal):
    if idsss == 'id':
        if illegal == 'correct':
            result = 1
        elif illegal == 'missing':
            result = 2
        else:
            result = 3
    elif idsss == 'ids':
        result =4
    print result


if __name__ == '__main__':
    test_if('id', 'correct')
