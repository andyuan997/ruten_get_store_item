#獲取露天賣家總商品資訊
from selenium import webdriver
import time
import pandas as pd

#一些必要參數
print("擷取露天賣家商品機器!!\n請輸入露天賣家帳號: ")
ruten_account = input() #賣場帳號
print("請輸入要擷取的頁數: ")
b=input() #頁數
print("請輸入chromedriver路徑: ") #chrome driver路徑
driver_path = input()
print("搜尋露天賣家帳號"+ ruten_account )
b = int(b)

#以下設定預設值
"""
if ruten_account == '' :
    ruten_account = '###這邊點血預設值###'
if b == "":
    b = ###這邊點血預設值###
if driver_path == '' :
    driver_path='###這邊點血預設值###'
"""

delay=3 #延遲時間
a=30 #每頁商品數量(30個)，正常不會做更動。


#創建空列表
product_number_list = []
product_name_list = []
product_number=0
item_number_list = []

#每頁獲取商品號碼及名稱
def get_product(j,a):
    """
    j:目前頁數
    a:每頁商品數
    x:商品名稱列表
    """
    for i in range(1,a+1):
        try:
            step = i+(j-1)*30
            product_name_element_xpath='//*[@id="app"]/div[2]/div[2]/div[3]/div[5]/div[{}]/div[2]/a'.format(i)
            product_name_element = driver.find_element_by_xpath(product_name_element_xpath)
            #去除多餘資料
            product_number = (product_name_element.get_attribute("href")[-14:])
            product_name = (product_name_element.get_attribute("title")[2:-4])
            product_number_list.append(product_number)
            product_name_list.append(product_name)
            print(step)
            #print(product_name_element)
            #print(product_number,product_name)
        except:
            step = i-1
            print("錯誤!!未讀取到商品".format(step))

def main(b=10,a=30,delay=delay):
    """
    b:總頁數
    a:每頁商品數
    delay:每頁延遲時間
    """
    for j in range(1,b+1):
        web = 'https://www.ruten.com.tw/user/index00.php?s='+ruten_account+'&o=3&p={}'.format(j)
        driver.get(web)
        print('進入{}!!'.format(web))
        time.sleep(delay)
        #如果找到此元素，代表輸入帳號錯誤
        try:
            error = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]').text
            print(error)
            if error == "對不起，露天拍賣搜尋不到此會員帳號，請確認後重新查詢。":
                break
        except:
            pass
        #獲取目前網站上的總商品數量
        global product_number
        product_number=driver.find_element_by_xpath('//*[@id="classframe"]/div/div[1]/a').text
        get_product(j=j,a=a)

#比對商品總數
def compare():
    print("數據比對...")
    global product_name_list
    global product_number
    if str(len(product_name_list)) == product_number[6:-1]:
        print("比對OK，商品數量為{}".format(product_number[6:-1]))
    else:
        print("比對失誤，商品總數為{}，獲取總數為{}".format(product_number[6:-1],str(len(product_name_list))))

#獲取商品細項
def get_item():
    for j in range(0,len(product_number_list)):
        next_web='https://www.ruten.com.tw/item/show?'+ product_number_list[j]
        driver.get(next_web)
        print("j=",j)
        item_number_list.append("#")
        item_number_list.append("*")
        for i in range(1,60):
            try:
                items_name_element_xpath='//*[@id="main_form"]/div/div[2]/div/div/div[1]/div/div/ul/li[{}]/label'.format(i)
                x = driver.find_element_by_xpath(items_name_element_xpath)
                data = "     " + (x.text)
                item_number_list.append(data)
                #print(data)
            except:
                #給500次迴圈，遇到錯誤跳出。
                for x in range(1,50):
                    try:
                        items_name_element_xpath='//*[@id="main_form"]/div/div[2]/div/div/div[1]/div[2]/div/ul/li[{}]/label'.format(x)
                        x = driver.find_element_by_xpath(items_name_element_xpath)
                        data="          " + (x.text)
                        item_number_list.append(data)
                        #print(data)
                    except:
                        for y in range(1,50):
                            try:
                                items_name_element_xpath='//*[@id="main_form"]/div/div[3]/div/div/div[1]/div[2]/div/ul/li[{}]/label'.format(y)
                                x = driver.find_element_by_xpath(items_name_element_xpath)
                                data="               " + (x.text)
                                item_number_list.append(data)
                                #print(data)
                            except:
                                break
                        break
                break
        time.sleep(1)

#將資料結合
def append():
    global item_number_list
    global product_name_list
    global product_number_list
    k = 0
    l = 0
    for i in range(0, len(item_number_list)):
        if item_number_list[i] == '#':
            del item_number_list[i]
            item_number_list.insert(i, product_name_list[k])
            k = k + 1
        if item_number_list[i] == '*':
            del item_number_list[i]
            item_number_list.insert(i, product_number_list[l])
            l = l + 1


if __name__ == "__main__":
    driver = webdriver.Chrome(driver_path)
    main(b, a, delay)
    try:
        compare()
    except:
        print("出了點問題，未進行數據比對")
    get_item()
    append()
    if item_number_list != []:
        # 列表轉成DataFrame
        df = pd.DataFrame(item_number_list, columns=['list'])
        # 存成excel檔
        df.to_excel("list.xlsx", index=True)
        print("擷取成功!!!")
    elif item_number_list == []:
        print("擷取失敗!!!")
