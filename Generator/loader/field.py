import property
import loader.common
import model.field

class Loader(object):
    @staticmethod
    def load(namespace, fieldElement):
        name = fieldElement["Name"]
        tag = fieldElement["Tag"]
        dataType = fieldElement["DataType"]
        attrsStartPos = dataType.find('[')
        attrs = None
        if attrsStartPos != -1:
            attrsEndPos = dataType.find('[', attrsStartPos)
            if attrsEndPos == -1:
                raise Exception('Invalid data type %s ' % dataType )
            dataType = dataType[:attrsStartPos]
            attrs = [attr.strip for attr in dataType[attrsStartPos : attrsEndPos].split(',')]

        return model.field.Field(name, tag, dataType, namespace, attrs = attrs )
