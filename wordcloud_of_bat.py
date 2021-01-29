import jieba
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import multidict as multidict
import numpy as np
from PIL import Image



bat_mask = np.array(Image.open("/root/Scripts/bat_black_white.png"))


fullTermsDict = multidict.MultiDict()
#text = "symbol of good fortune "*98 + "vampire "*412 + "COVID-19 virus carrier "*639 + "Pest control " * 302 + "food "*22 + "ugly "*189 + "ultrasonic "*29 + "mammals "*13 + "batman "*49 + "Fearsome "*135 + "animal "*69 + "Upside down "*3 + "mouse "*5
text = {"Symbol of good fortune":98,
        "Vampire" : 412, 
        "COVID-19" : 639, 
        "Virus carrier": 639,
        "Pest Control": 302, 
        "Food" : 22, 
        "Ugly": 189, 
        "Ultrasonic": 29, 
        "Mammals": 13, 
        "Batman": 49, 
        "Fearsome" : 135, 
        "Animal": 69, 
        "Upside down" : 3, 
        "mouse" : 5,
        "Nothing": 25, 
        "Don't Know": 13,
        "Nocturnal": 35,
        "Summer": 20}

for key in text:
    fullTermsDict.add(key, text[key])


wc = WordCloud(scale=2, max_font_size=200, max_words= 100, background_color="white", width=5000, height=5000, mask = bat_mask, contour_color="grey", contour_width=50)
wc.generate_from_frequencies(fullTermsDict)

plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.tight_layout()

wc.to_file("test.png")
plt.show()

WordCloud()