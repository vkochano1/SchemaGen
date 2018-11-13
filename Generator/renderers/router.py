from  model.common import *

class TemplateRouter(object):
    @staticmethod
    def routeObject(modelObj):
        if modelObj.objectType() == ObjectType.Message:
            if modelObj.isVector == True:
                return "templates/message_vector.cog"
            if modelObj.countFields() == 0:
                return "templates/message_no_props.cog"
            else:
                return "templates/message.cog"
        elif modelObj.objectType() == ObjectType.Payload:
            if modelObj.isAbstractHeader == True:
                return "templates/payload_abstract.cog"
            else:
                return "templates/payload.cog"
        elif modelObj.objectType() == ObjectType.Configuration:
            return "templates/configuration.cog"
        elif modelObj.objectType() == ObjectType.Field:
            return "templates/field.cog"
        elif modelObj.objectType() == ObjectType.Enumeration:
            return "templates/enum.cog"

        raise Exception("Unknown object type")

    @staticmethod
    def routeGroupObject(modelObj):
        if modelObj.objectType() == ObjectType.Message:
            return "templates/messages.cog"
        elif modelObj.objectType() == ObjectType.Payload:
            return "templates/payloads.cog"
        elif modelObj.objectType() == ObjectType.Configuration:
            return "templates/configurations.cog"
        elif modelObj.objectType() == ObjectType.Field:
            return "templates/fields.cog"
        elif modelObj.objectType() == ObjectType.Enumeration:
            return "templates/enums.cog"

        raise Exception("Unknown object type")

    @staticmethod
    def objectNameInTemplate(modelObj):
        if modelObj.objectType() == ObjectType.Message:
            return "msg"
        elif modelObj.objectType() == ObjectType.Payload:
            return "payload"
        elif modelObj.objectType() == ObjectType.Configuration:
            return "conf"
        elif modelObj.objectType() == ObjectType.Field:
            return "field"
        elif modelObj.objectType() == ObjectType.Enumeration:
            return "enum"

        raise Exception("Unknown object type")

    @staticmethod
    def objectGroupNameInTemplate(modelObj):
        if modelObj.objectType() == ObjectType.Message:
            return "msgs"
        elif modelObj.objectType() == ObjectType.Payload:
            return "payloads"
        elif modelObj.objectType() == ObjectType.Configuration:
            return "configurations"
        elif modelObj.objectType() == ObjectType.Field:
            return "fields"
        elif modelObj.objectType() == ObjectType.Enumeration:
            return "enums"

        raise Exception("Unknown object type")
