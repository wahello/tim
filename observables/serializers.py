from rest_framework import serializers, fields

from . import models
from events.models import EventObservable, Event
from django.db import transaction

import traceback
from rest_framework.utils import model_meta
from django.core.validators import validate_email, validate_ipv46_address
from django.urls import reverse_lazy

def get_validator():
    validators = {
        "email": validate_email,
        "ip": validate_ipv46_address
    }
    return validators

def get_object():
    objects = {
        "email": models.EmailValue,
        "ip": models.IpValue,
        "string": models.StringValue
    }
    return objects


class IpValuesSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="observables:ip-value-detail",
                    )

    id = serializers.ReadOnlyField()
    type = "ip"

    value = serializers.IPAddressField(protocol='both')
    class Meta:
        model = models.IpValue
        fields = ('url','id', 'value', 'rateing', 'to_ids')

#    def validate_empty_values(self, data):
#        if data is None:
#           raise serializers.ValidationError('Value cannot be empty')
#
#        # if you return True all other validations will be skipped
#        return (False, data)

    def validate(self, attrs):
        value = attrs["value"]
        try:
            get_validator()[self.type](value)
        except Exception as e:
           raise serializers.ValidationError(e)
        return attrs


    def to_representation(self, instance):
        ret = super(IpValuesSerializer, self).to_representation(instance)
        ret.pop("id")
        return ret

    def to_internal_value(self, instance):
        ret = super(IpValuesSerializer, self).to_internal_value(instance)
        
        return ret

    def update(self, instance, validated_data):
        values = self.Meta().model.objects.filter(value = validated_data["value"])
        obj = self.Meta().model.objects.filter(id=instance.id)
        if len(values) == 1:
            validated_data.pop("value")
        obj.update(**validated_data)

        instance.refresh_from_db()
        return instance


class EmailValuesSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="observables:email-value-detail",
                    )

    value = serializers.EmailField()
    id = serializers.ReadOnlyField()
    type = "email"

    class Meta:
        model = models.EmailValue
        fields = ('url','id', 'value', 'rateing', 'to_ids')

#    def validate_empty_values(self, data):
#        if data is None:
#           raise serializers.ValidationError('Value cannot be empty')
#        return (False, data)

    def validate(self, attrs):
        value = attrs["value"]
        try:
            get_validator()[self.type](value)
        except Exception as e:
           raise serializers.ValidationError(e)
        return attrs

    def to_representation(self, instance):
        ret = super(EmailValuesSerializer, self).to_representation(instance)
        ret.pop("id")
        return ret

    def to_internal_value(self, instance):
        ret = super(EmailValuesSerializer, self).to_internal_value(instance)
        return ret

    @transaction.atomic
    def create(self, validated_data):
        values, create = self.Meta().model.objects.get_or_create(value=validated_data["value"])
        if create:
            do_also = self.Meta().model.objects.filter(id=values.id)
            do_also.update(**validated_data)
            
        values.refresh_from_db()
        return values

    def update(self, instance, validated_data):
        values = self.Meta().model.objects.filter(value = validated_data["value"])
        obj = self.Meta().model.objects.filter(id=instance.id)
        if len(values) == 1:
            validated_data.pop("value")
        obj.update(**validated_data)

        instance.refresh_from_db()
        return instance


class StringValuesSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="observables:string-value-detail",
                    )

    id = serializers.ReadOnlyField()
    type = "string"
    value = serializers.CharField()

    class Meta:
        model = models.StringValue
        fields = ('url','id', 'value', 'rateing', 'to_ids')

#    def validate_empty_values(self, data):
#        if data is None:
#           raise serializers.ValidationError('Value cannot be empty')
#        return (False, data)

    def validate(self, attrs):
        print(attrs)
        return attrs

    def to_representation(self, instance):
        ret = super(StringValuesSerializer, self).to_representation(instance)
        ret.pop("id")
        return ret

    def to_internal_value(self, instance):
        ret = super(StringValuesSerializer, self).to_internal_value(instance)
        
        return ret

    @transaction.atomic
    def create(self, validated_data):
        values, create = self.Meta().model.objects.get_or_create(value=validated_data["value"])
        if create:
            print("New")
        else:
            print("Old")
        return values

    def update(self, instance, validated_data):
        values = self.Meta().model.objects.filter(value = validated_data["value"])
        obj = self.Meta().model.objects.filter(id=instance.id)
        if len(values) == 1:
            validated_data.pop("value")
        obj.update(**validated_data)

        instance.refresh_from_db()
        return instance


class FileValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FileValue
        fields = ('__all__')


class ObservableTypeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    url = serializers.HyperlinkedIdentityField(
                    view_name="observables:observable-type-detail",
                    )

    class Meta:
        model = models.ObservableType
        fields = ('__all__')

    def validate(self, attrs):
        return attrs

    def to_representation(self, instance):
        ret = super(ObservableTypeSerializer, self).to_representation(instance)
        return ret

    def to_internal_value(self, instance):
        ret = super(ObservableTypeSerializer, self).to_internal_value(instance)
        return ret

    @transaction.atomic
    def create(self, validated_data):
        values, create = self.Meta().model.objects.get_or_create(value=validated_data["value"])
        return values

    def update(self, instance, validated_data):
        values = self.Meta().model.objects.filter(value = validated_data["value"])
        obj = self.Meta().model.objects.filter(id=instance.id)
        if len(values) == 1:
            validated_data.pop("value")
        obj.update(**validated_data)

        instance.refresh_from_db()
        return instance


class ObservableValueSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="observables:observable-value-detail",
                    )

    observable = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Observable.objects.all())
    ip = IpValuesSerializer(required=False, allow_null=True)
    email = EmailValuesSerializer(required=False, allow_null=True)
    string = StringValuesSerializer(required=False, allow_null=True)
    type = ObservableTypeSerializer(required=True)
    id = serializers.ReadOnlyField()
    own_id = None
    skip_fields = list()

    def validate_empty_values(self, data):
        ret = data.copy()
        for item, value in data.items():
            if value is None:
                self.skip_fields.append(item)
                ret.pop(item)
        return (False, data)

    def validate(self, attrs):
        print(attrs) 
        if ("type" and "observable" in attrs):
            valid = dict()

            # validate observable
            if "observable" in attrs:
                valid["observable"] = attrs["observable"]
                attrs.pop("observable", None)
            

            for key, value in attrs.items():
                valid[key] = None

                if value:
                    if str(value) == "NULL":
                        valid[key] = "NULL"

                valid[key] = value

                if str(value) == "NULL":
                    continue
                if not key in attrs["type"]["type_class"] and value:
                    raise serializers.ValidationError('%s field must be empty with type: %s' % (key, type_class))

            return valid
        else:
            return attrs

    class Meta:
        model = models.ObservableValue
        fields = ('__all__')

#    def to_internal_value(self, data):
#        try:
#            self.own_id = data["id"]
#        except:
#            self.own_id = None
#        return super(ObservableValueSerializer,self).to_internal_value(data)
#

    def select_serializer(self):
        serializer = {
            "ip": IpValuesSerializer,
            "email": EmailValuesSerializer,
            "string": StringValuesSerializer
        }
        return serializer

    def select_model(self):
        models = {
            "ip": models.IpValue,
            "email": models.EmailValue,
            "string": models.StringValue
        }

    def get_orig_value(self, instance):
        value = {
            "ip": instance.ip,
            "email": instance.email,
            "string": instance.string
        }
        return value

    @transaction.atomic
    def update(self, instance, validated_data):
        pk = instance.id
        object = models.ObservableValue.objects.filter(id=pk)
        serializer = self.select_serializer()
        for key, value in validated_data.items():
            if key in serializer and value:
                svalue = serializer[key](data=value)
                if not svalue.is_valid():
                    print(serializer.errors)
                else:
                    new = svalue.save()
                    svalue.update(new, svalue.validated_data)
                    new.obs_values.add(instance)
                    continue
            elif value:
                if "observable" in key:
                    value.values.add(instance)

        instance.refresh_from_db()
        return instance

    @transaction.atomic
    def create(self, validated_data):
        observable = validated_data["observable"]
        validated_data.pop("observable")
        obj = None
        for key, value in validated_data.items():
            if key is "type":
                type = models.ObservableType.objects.filter(name=value)
                if type:
                    validated_data["type"] = type.get()
                continue
            if value:
                obj, created = get_object()[key].objects.get_or_create(value=value)
                validated_data[key] = obj
        
        values = models.ObservableValue.objects.create(**validated_data)
        observable.values.add(values)
        return values


class ObservableSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="observables:observable-detail",
                    )


    event = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    id = serializers.ReadOnlyField()
    values = ObservableValueSerializer(many=True, read_only=False)
    value_ids = list()

    class Meta:
        model = models.Observable
        fields = ('__all__')

    def validate(self, attrs):
        return attrs

    def to_internal_value(self, data):
        
        self.value_ids = list()
        for item in data["values"]:
            item["id"]
            self.value_ids.append(item["id"])
        return super(ObservableSerializer,self).to_internal_value(data)

    @transaction.atomic
    def update(self, instance, validated_data):
        pk = instance.id
        update = dict()
        for key, value in validated_data.items():
            if not key == "values":
                update[key] = value
            else:
                for index, val_pk in enumerate(self.value_ids):
                    send = dict()
                    if value and "observable" in value[index]:
                        send = value[index]
                        send["observable"] = value[index]["observable"].id
                        value_filter = models.ObservableValue.objects.filter(pk=val_pk)
                        if value_filter.values():
                            value_instance = value_filter.get()
                            serializer = ObservableValueSerializer(data=send)
                            if not serializer.is_valid():
                                print(serializer.errors)
                            else:
                                print(serializer.validated_data)
                                serializer.update(instance=value_instance, validated_data=send)

        excisting = instance.values.all()
        orig_val = list()

        for item in excisting.values():
            orig_val.append(item["id"])

        if orig_val:
            for item in orig_val:
                if item in self.value_ids:
                    continue
                else:
                    rem = instance.values.get(id=item)
                    instance.values.remove(rem)

        for item in self.value_ids:
            if not item in excisting.values():
                try:
                    new = models.ObservableValue.objects.get(id=item)
                except:
                    continue
                instance.values.add(new)

        object = models.Observable.objects.filter(id=pk).update(**update)
        instance.refresh_from_db()
        return instance

