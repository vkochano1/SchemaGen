import property
import loader.common
import model.field

class Loader(object):
    @staticmethod
    def load(namespace, fieldElement):
        dataType =  fieldElement["DataType"]
        args = {
             "name" : fieldElement["Name"]
            ,"tag" : fieldElement["Tag"]
            ,"dataType" : dataType
            ,"displayName" : fieldElement["DisplayName"]
            ,"namespace" : namespace
        }
        attrsStartPos = dataType.find('[')
        if attrsStartPos != -1:
            attrsEndPos = dataType.find('[', attrsStartPos)
            if attrsEndPos == -1:
                raise Exception('Invalid data type %s ' % dataType )
            args["dataType"] = dataType[:attrsStartPos]
            args["attrs"] =  [attr.strip for attr in dataType[attrsStartPos : attrsEndPos].split(',')]

        return model.field.Field(**args)
