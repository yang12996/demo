import  re
from  common.handle_config import Config
from common.handle_config import conf

#使用正则替换数据
class Test():

    def replace_data(data,cls):
        """
       替换数据
       :param data: 要进行替换的用例数据（字符串）
       :param cls: 测试类
       :return:
       """
        # while re.search('#(.+?)#', data):  #注意: search匹配到了返回一个对象，没有匹配到返回None
        #     res2 = re.search('#(.+?)#',data)
        #     item= res2.group()
        #     attr = res2.group(1)
        #     value = getattr(cls,attr)
        #     #进行替换
        #     data = data.replace(item, str( value))
        # return data

        #todo ********************升级版，先去类查找是否有值可以替换，没有去配置文件找替换*******************************************
        while re.search('#(.+?)#', data):  #注意: search匹配到了返回一个对象，没有匹配到返回None
            res2 = re.search('#(.+?)#',data)
            item= res2.group()
            attr = res2.group(1)
            try :
                value = getattr(cls,attr)
            except AttributeError:
                # value=Config.get("test",attr)
                value=conf.get("test",attr)
            #进行替换
            data = data.replace(item, str( value))
        return data