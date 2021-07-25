def average_hsv(idx, p, hsv_roi):
        """ Average the HSV colors in a region of interest.
        :param roi: the image array
        :returns: tuple
        """
        h   = 0
        s   = 0
        v   = 0
        num = 0
        X = p[idx][0]
        Y = p[idx][1]
        for y in range(Y-3,Y+4):
                for x in range(X-3,X+4):
                        chunk = hsv_roi[y][x]
                        num += 1
                        h += chunk[0]
                        s += chunk[1]
                        v += chunk[2]
        h /= num
        s /= num
        v /= num
        return (int(h), int(s), int(v))


def detect_color(hsv):
    (h,s,v) = hsv
    if s<=75:
        return "w"
    elif h>=82 and h<=133:
        return "b"
    elif h>=30 and h<=78:
        return "g"
    elif h>=20 and h<30:
        return "y"
    elif h>=7 and h<=19:
        return "o"
    elif h<7:
        return "r"
    else:
        return "NR"
