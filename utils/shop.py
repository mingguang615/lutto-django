from shop import models
from collections import OrderedDict
from django.db.models import Count
def Greatgoods(good):
    print('this is Greatgoods')
    goods = []
    for gg in good:
        if gg:
            good_id=gg['goods_id']
            url = list(models.GoodPicture.objects.filter(good_id=good_id,size='1').values('good_id','url'))
            b = OrderedDict()
            for item in url:
                b.setdefault(item['good_id'], {**item, })
            b = list(b.values())
            goods_comment = models.GoodComment.objects.filter(good_id=good_id).aggregate(
                goods_comment=Count('content'))
            G = gg['goods_gooddesc']
            if G:
                good_name = G.split('@')
                aa = []
                for g in good_name:
                    if g:
                        if '店铺' in g or '价位' in g:
                            pass
                        else:
                            aa.append(g)
                ss = {
                    "name": gg['goods_name'],
                    # "good_kucun": gg['goods_kuncun'],
                    "intergal": gg['goods_intergal'],
                    # "gooddesc": gg['goods_gooddesc'],
                    "goodbrand_name": gg['goods_band_name'],
                    # "goodclass_name": gg['good_class_name'],
                    "goode_url":b[0]['url'],
                    "good_id": good_id,
                    "good_comment":goods_comment['goods_comment']

                }
                goods.append(ss)
            # print(ss)
        else:
            print('错了宝贝')
    return goods
