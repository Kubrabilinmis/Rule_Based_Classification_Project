# Kural Tabanlı Sınıflandırma ile Potansiyel Müşteri Getirisi Hesaplama
"""
İş Problemi :
Bir oyun şirketi müşterilerinin bazı özelliklerini kullanarak
seviye tabanlı (level based) yeni müşteri tanımları
(persona) oluşturmak ve bu yeni müşteri tanımlarına
göre segmentler oluşturup bu segmentlere göre yeni
gelebilecek müşterilerin şirkete ortalama ne kadar
kazandırabileceğini tahmin etmek istemektedir.

Örneğin:
Türkiye’den IOS kullanıcısı olan 25 yaşındaki bir erkek
kullanıcının ortalama ne kadar kazandırabileceği
belirlenmek isteniyor.

Veri Seti Hikayesi:
Persona.csv veri seti uluslararası bir oyun şirketinin sattığı ürünlerin fiyatlarını
ve bu ürünleri satın alan kullanıcıların bazı demografik bilgilerini barındırmaktadır.
Veri seti her satış işleminde oluşan kayıtlardan meydana gelmektedir.
Bunun anlamı tablo tekilleştirilmemiştir.
Diğer bir ifade ile belirli demografik özelliklere sahip bir kullanıcı birden fazla alışveriş yapmış olabilir.

Değişkenler:
PRICE   – Müşterinin harcama tutarı
SOURCE  – Müşterinin bağlandığı cihaz türü
SEX     – Müşterinin cinsiyeti
COUNTRY – Müşterinin ülkesi
AGE     – Müşterinin yaşı

"""

# Gorev 1 :
# soru 1  : persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.

import pandas as pd
df = pd.read_csv("datasets/persona.csv")
pd.pandas.set_option('display.max_columns', None)

def check_df(dataframe, head=5):
    print("##################### shape #####################")
    print(dataframe.shape)
    print("##################### columns #####################")
    print(dataframe.columns)
    print("##################### dtypes #####################")
    print(dataframe.dtypes)
    print("##################### head #####################")
    print(dataframe.head(head))
    print("##################### tail #####################")
    print(dataframe.tail(head))
    print("##################### describe #####################")
    print(dataframe.describe().T)
    print("##################### NA #####################")
    print(dataframe.isnull().sum())

check_df(df)


# soru 2  : Kaç unique SOURCE vardır? Frekansları nedir?
df["SOURCE"].nunique()
df["SOURCE"].value_counts()

# soru 3  : Kaç unique PRICE vardır?
df["PRICE"].nunique()

# soru 4  : Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
df["PRICE"].value_counts()

# soru 5  : Hangi ülkeden kaçar tane satış olmuş?
df["COUNTRY"].value_counts()

# soru 6  : Ülkelere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("COUNTRY")["PRICE"].sum()

# soru 7  : SOURCE türlerine göre göre satış sayıları nedir?
df["SOURCE"].value_counts()

# soru 8  : Ülkelere göre PRICE ortalamaları nedir?
df.groupby("COUNTRY")["PRICE"].mean()

# soru 9  : SOURCE'lara göre PRICE ortalamaları nedir?
df.groupby("SOURCE")["PRICE"].mean()

# soru 10 :COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
df.groupby(["COUNTRY","SOURCE"]).agg({"PRICE": "mean" })


# GOREV 2 : COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE" : "mean"})


# GOREV 3 :
# Çıktıyı PRICE’a göre sıralayınız.
# Önceki sorudaki çıktıyı daha iyi görebilmek için sort_values metodunu azalan olacak şekilde PRICE’a göre uygulayınız.
# Çıktıyı agg_df olarak kaydediniz.

agg_df = df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE" : "sum"}).sort_values(by='PRICE',ascending=False)
agg_df.head()


# GOREV 4 :
# Index’te yer alan isimleri değişken ismine çeviriniz.
# Üçüncü sorunun çıktısında yer alan price dışındaki tüm değişkenler index isimleridir.
# Bu isimleri değişken isimlerine çeviriniz.

agg_df = agg_df.reset_index()
agg_df


# GOREV 5 :
# age değişkenini kategorik değişkene çeviriniz ve
# agg_df’e ekleyiniz.
# Age sayısal değişkenini kategorik değişkene çeviriniz.
# Aralıkları ikna edici şekilde oluşturunuz.
# Örneğin: ‘0_18', ‘19_23', '24_30', '31_40', '41_70'

df["AGE"].nunique()
#46
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"] , bins = [0, 18, 23, 30, 40, 66], labels = ["0_18", "19_23", "24_30", "31_40", "41_66"])

agg_df.head()



# GOREV 6 :
# Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
# Yeni seviye tabanlı müşterileri (persona) tanımlayınız ve veri setine değişken olarak ekleyiniz.
# Yeni eklenecek değişkenin adı: customers_level_based
# Önceki soruda elde edeceğiniz çıktıdaki gözlemleri bir araya getirerek customers_level_based
# değişkenini oluşturmanız gerekmektedir.

agg_df.columns

agg_df["customers_level_based"] = [col[0].upper() + "_" + col[1].upper() + "_" + col[2].upper() + "_" + col[5].upper() for col in agg_df.values]

agg_df = agg_df[["customers_level_based", "PRICE"]]
agg_df.head()

agg_df["customers_level_based"].value_counts()

agg_df = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"})

agg_df = agg_df.reset_index()
agg_df



# GOREV 7 :
# Yeni müşterileri (personaları) segmentlere ayırınız.
# Yeni müşterileri (Örnek: USA_ANDROID_MALE_0_18) PRICE’a göre 4 segmente ayırınız.
# Segmentleri SEGMENT isimlendirmesi ile değişken olarak agg_df’e ekleyiniz.
# Segmentleri betimleyiniz (Segmentlere göre group by yapıp price mean, max, sum’larını alınız).
# C segmentini analiz ediniz (Veri setinden sadece C segmentini çekip analiz ediniz).

agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"] , 4 , labels = ["D","C","B","A"])
agg_df.groupby("SEGMENT").agg({"PRICE": ["mean","max","sum"]})
agg_df[agg_df["SEGMENT"] == "C"]


# GOREV 8 :
# Yeni gelen müşterileri segmentlerine göre sınıflandırınız ve ne kadar gelir getirebileceğini tahmin ediniz.
# 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?
# 35 yaşında IOS kullanan bir Fransız kadını hangi segmente ve ortalama ne kadar gelir kazandırması beklenir?

new_user = "TUR_ANDROID_FEMALE_31_40"
new_user2 = "FRA_IOS_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]
agg_df[agg_df["customers_level_based"] == new_user2]




