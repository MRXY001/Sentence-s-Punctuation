import fastText
import jieba

classifier = fastText.train_supervised("data/tangsan_dataset.txt")
classifier.save_model("data/douluo.model")


def judge(s):
    print(s, classifier.predict(" ".join(jieba.cut(s))))


judge("天黑，别出门")
judge("这句话在残老村流传了很多年，具体是从什么时候传下来的，已经无从考证。不过这句话却是真理，无需怀疑")
judge("咦，真有婴儿的哭声")
judge("村外的黑暗中传来婴儿的哭声，村里其他老人除了耳聋的都听到了这个哭声，老人们面面相觑，残老村偏僻荒凉，怎么会有婴儿出现在附近")
judge("不可能，你听错")
judge("你疯了")
judge("死瘸子，你断了条腿，能走吗")
judge("他独臂将石像抱起，稳了稳步子")
judge("司老太婆，你打算养着他")
judge("老娘凭本事捡到的小孩，为什么要送人")


while True:
    judge(input())

