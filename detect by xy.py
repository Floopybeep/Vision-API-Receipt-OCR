import os
from google.cloud import vision
credential_path = r"C:\Users\55\Desktop\client_secrets.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path

class priceindex:
    price = []
    product = []
    quantity = []
    index = []
    netprice = 0

finalresult = priceindex()


def is_hangul_character(char):
    '''Check if character is in the Hangul Jamo block'''

    if ord('가') <= ord(char) <= ord('힣'):
        return 1
    else:
        return 0


def concaetenator(words):
    """joins together any overlapping letters in given string(word)"""
    """i.e. '. 000' -> '.' ',' '000'  INSTEAD OF '0' '0' '0' """
    strletters = list(words)
    tempstrletters = list(words)
    i = 1
    j = 1

    for y in strletters:
        if strletters[i] == strletters[j - 1]:
            tempstr = [strletters[i], tempstrletters[j - 1]]
            tempstrletters[j - 1] = ''.join(tempstr)
            del tempstrletters[j]
        else:
            j = j + 1
        if i == len(strletters) - 1:
            break
        if j == len(tempstrletters):
            break
        i = i + 1

    return tempstrletters


# def strscanner(word, searchstr):
#     """scans a string for a certain string, and returns yes/no and index location as [1/0, number]"""
#     i = 0
#     letters = list(word)
#     strletters = concaetenator(searchstr)
#
#     for x in letters:
#         for y in strletters:
#             if x == y


def pricefixer(numbers):
    """Given a list of numbers and , and . and spaces, outputs a single number"""
    wordl = list(numbers)
    i = 0

    for char in wordl:
        if not char.isdigit():
            wordl.pop(i)
        i = i + 1
    result = ''.join(wordl)
    return result

def maxrighter(texts):
    global maxright
    maxright = 0

    for text in texts:
        k = text.bounding_poly.vertices[1].x
        if k > maxright:
            maxright = k
#normal : 576


def numscanner(texts):
    """Given a text, outputs a list of indices of numbers fitting criteria"""
    #Input: texts
    #Output: list of indexes
    #Function: scans text for 3 consecutive numbers without any characters around it

    prelims = priceindex()
    whitelist = [' ', '.', ',']
    i = 0
    j = 0
    iscomma = 0
    ystandard = 0


    for word in texts:
        # if word is less than 3 letters long, it's not price (I am discounting stuff that costs less than 100 won)
        k = word.description
        if len(word.description) < 3:
            j = j + 1
            continue
        wordl = list(word.description)
        for letter in k:
            # if word has 3 consecutive digits
            if wordl[i].isalpha():
                break
            if wordl[i] == ',' or wordl[i]=='.':
                iscomma = 1
            if wordl[i].isdigit() and wordl[i + 1].isdigit() and wordl[i + 2].isdigit():
                if len(k) >= i + 4:
                    if iscomma == 1:
                        if xstandard < word.bounding_poly.vertices[0].x + 15:
                            if ystandard < word.bounding_poly.vertices[0].y:
                                if word.bounding_poly.vertices[1].x + 40 > maxright:
                                    prelims.price.append(word.description)
                                    prelims.index.append(j)
                                    ystandard = texts[prelims.index[0]].bounding_poly.vertices[0].y
                                    xstandard = texts[prelims.index[0]].bounding_poly.vertices[0].x
                                    break
                    elif not (wordl[i + 3] == '.' or wordl[i + 3].isspace() or wordl[i+3] == '원'):
                        break
                    else:
                        # if word is within 30 x-pixels of maxright
                        if word.bounding_poly.vertices[1].x + 40 > maxright:
                            prelims.price.append(word.description)
                            prelims.index.append(j)
                            ystandard = texts[prelims.index[0]].bounding_poly.vertices[0].y
                            xstandard = texts[prelims.index[0]].bounding_poly.vertices[0].x
                            break
                else:
                    # if word is within 30 x-pixels of maxright
                    if word.bounding_poly.vertices[1].x + 40 > maxright:
                        prelims.price.append(word.description)
                        prelims.index.append(j)
                        ystandard = texts[prelims.index[0]].bounding_poly.vertices[0].y
                        xstandard = texts[prelims.index[0]].bounding_poly.vertices[0].x
                        break
            if i == len(k) - 3:
                break
            i = i + 1
        i = 0
        j = j + 1
        iscomma = 0
    i = 0
    j = 0

    for word in prelims.price:
        x = word
        for char in word:
            if i == len(word):
                break
            y = char
            # if word has anything other than numbers or . or , or space, then remove it from list
            if ((not char.isdigit()) and (not char.isspace()) and char != ',' and char != '.' and char != '*') or char == '-' or char == '(' or char == ')':
                prelims.price.pop(j)
                prelims.index.pop(j)
                break
            i = i + 1
        i = 0
        j = j + 1
    j = 0


    finalresult = prelims
    return prelims.index


def pricescanner(texts, indexes):
    """Given a text and indices of price candidates, outputs numbers fitting the criteria for prices"""
    #Criteria: within 30 pixels of maxright, has 3 consecutive numbers, with a space or comma before it"""
    #Input: texts
    #Output: list of prices and index of said prices (finalresult)

    prelims = priceindex()
    templist = []
    i = 0

    for index in indexes:
        highy = texts[index].bounding_poly.vertices[1].y  # y coordinate of upper vertice of given text
        if i < len(indexes) - 1:
            if (highy + 5) > (texts[indexes[i+1]].bounding_poly.vertices[1].y + 2) > highy:
                indexes.pop(i)

        for text in texts:
            # if y-pixel of text is close to y-pixel of texts[index]
            if (highy + 10) > (text.bounding_poly.vertices[1].y + 5) > highy and texts[index].description != text.description:
                # if x-pixel of text is close to x-pixel of texts[index]
                if text.bounding_poly.vertices[1].x + 10 > texts[index].bounding_poly.vertices[0].x:
                    templist.append(text.description)
        templist.append(texts[index].description)
        prelims.price[i] = ''.join(templist)
        prelims.index[i] = index
        i = i + 1
        templist = []
    i = 0

    for prices in prelims.price:
        prelims.price[i] = pricefixer(prices)
        i = i + 1

    finalresult = prelims
    return prelims



def authenticator(texts):
    #Cuts the total amount (합계, 총 금액) from the price list
    #Looks for '합계', '금액'
    #Also compares y-distance between each 'price', and cuts out the biggest gap

    gap = 0
    gapindex = 0
    netsumindex = 0
    i = 0
    j = 0
    temp = finalresult.price[len(finalresult.price) - 1]
    tempfinal = 0

    #Finds the largest y-distance between prices and saves it to gap
    #Saves the index of the largest distance price to gapindex (the price lower on the receipt)
    # for ind in finalresult.index:
    #     if i == 0:
    #         i = 1
    #         continue
    #
    #     if texts[ind].bounding_poly.vertices[1].y - texts[finalresult.index[i-1]].bounding_poly.vertices[1].y > gap:
    #         gap = max(texts[ind].bounding_poly.vertices[1].y - texts[finalresult.index[i-1]].bounding_poly.vertices[1].y, gap)
    #         gapindex = ind
    #     i = i + 1
    # i = 0

    m = 0
    #Searches all text in same row as indexes, to see if it includes '합계' or '금액' or '물품'
    for ind in finalresult.index:
        k = texts[ind].bounding_poly.vertices[3].y
        samerow = []
        rowstring = ""
        isnetsum = 0

        if i == 0:
            i = 1
            continue


        #saves all text in same row as price into samerow
        #May require a change, so that text between prices are saved, instead of same line
            #However, 합계 or 금액 tends to be on the same line as price
        for text in texts:
            n = text.description
            o = text.bounding_poly.vertices[0].y
            if texts[finalresult.index[i-1]].bounding_poly.vertices[3].y < text.bounding_poly.vertices[0].y + 10 < k:
                samerow.append(text.description)

        for element in samerow:
            rowstring += str(element)

        rowstring.replace(" ", "")

        if rowstring.find('합계') != -1 or rowstring.find('금액') != -1 or rowstring.find('물품') != -1 or rowstring.find('면세') != -1 or rowstring.find('과세') != -1:
            isnetsum = 1
            netsumindex = i
            break

        i = i + 1
    i = 0




    if isnetsum:
        for x in range(netsumindex, len(finalresult.price)):
            finalresult.price.pop(netsumindex)
            finalresult.index.pop(netsumindex)

    for price in finalresult.price:
        tempfinal += int(price)


    if abs(tempfinal - int(temp)) > 1000:
        finalresult.netprice = tempfinal

    else:
        finalresult.netprice = temp

def prodname(texts):
    #Input: response (+ finalresult.price and index)
    #Output: finalresult.product
    #Function: Using the input, scans adjacent characters to find product name
    #Methodology: scans for hangul/english characters between each price's y-pixels, and any other text within 5 adjacent x-pixels

    i = 0
    j = 0
    samerow = []


    #For the first item, scans 15 pixels above price
    k = texts[finalresult.index[0]].bounding_poly.vertices[0].y
    l = texts[finalresult.index[0]].bounding_poly.vertices[3].y
    name = []

    for text in texts:
        if k < text.bounding_poly.vertices[3].y + 15 < l + 20:
            samerow.append(text.description)

    for item in samerow:
        isname = 0
        for char in item:
            if char.isalpha() or is_hangul_character(char) or char == '(' or char == ')':
                isname = 1
        if isname:
            name.append(item)

    finalresult.product.append(''.join(name))

    for ind in finalresult.index:
        samerow = []
        name = []
        k = texts[ind].bounding_poly.vertices[3].y

        if i == 0:
            i = 1
            continue

        l = texts[finalresult.index[i-1]].bounding_poly.vertices[3].y

        for text in texts:
            a = text.description
            b = text.bounding_poly.vertices[3].y
            if l <= text.bounding_poly.vertices[0].y + 10 <= k + 5:
                samerow.append(text.description)

        for item in samerow:
            isname = 0
            for char in item:
                x = char
                if char.isalpha() or is_hangul_character(char) or char == '(' or char == ')' or char == '+':
                    isname = 1
            if isname:
                name.append(item)


        finalresult.product.append(''.join(name))
        i = i + 1
    i = 0


def quannum(texts):
    i = 0
    j = 0
    samerow = []
    templist = []


    for ind in finalresult.index:
        samerow = []
        temp = 0
        k = texts[ind].bounding_poly.vertices[0].y
        l = texts[ind].bounding_poly.vertices[3].y

        # if i == 0:
        #     i = 1
        #     continue


        for text in texts:
            if k <= text.bounding_poly.vertices[0].y + 10 <= l + 10:
                samerow.append(text.description)

        samerow.reverse()

        for item in samerow:
            if len(item) <= 2 and item.isdigit():
                finalresult.quantity.append(item)
                temp = 1
                break

        if temp == 0:
            finalresult.quantity.append('Not Found')

        i = i + 1



def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations[0].description
    textxy = response.text_annotations
    textxy.pop(0)

    maxrighter(textxy)

    results = priceindex()
    list1 = numscanner(textxy)
    results = pricescanner(textxy, list1)

    authenticator(textxy)
    prodname(textxy)
    quannum(textxy)

    print(finalresult.price)
    print(finalresult.product)
    print(finalresult.quantity)

    print("합계: ", finalresult.netprice)


    # for ind in finalresult.index:
    #     print(textxy[ind].description)


def detect_text_uri(uri):
    """Detects text in the file."""

    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations[0].description
    textxy = response.text_annotations

    authenticator(textxy)
    prodname(textxy)
    quannum(textxy)

    print(finalresult.price)
    print(finalresult.product)
    print(finalresult.quantity)

    print("합계: ", finalresult.netprice)



    # for text in textxy:
    #     print('=' * 30)
    #     print(text.description)
    #     vertices = ['(%s,%s)' % (v.x, v.y) for v in text.bounding_poly.vertices]
    #     print('bounds:', ",".join(vertices))


#detect_text_uri(r"http://image.kmib.co.kr/online_image/2018/0114/611211110012048428_1.jpg")

detect_text(r"D:\Google 드라이브\Uni\CCP\13.jpg")

#5, 10 cannot be recognized
#9 needs a little work