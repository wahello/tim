from rest_framework import serializers
from . import models
from common.serializers import MinMotiveSerializer, MinSectorSerializer
from observables.serializers import ObservableSerializer
from django.db.models import Manager
from django.db.models.query import QuerySet


from django_countries.serializers import CountryFieldMixin
from django_countries.serializer_fields import CountryField
from observables.models import Observable
from common.serializers import MotiveSerializer, SectorSerializer
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

class TypeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="events:type-detail",
                    )

    event = serializers.HyperlinkedRelatedField(
                    many=True,
                    read_only=True,
                    view_name='events:event-detail',
                    )

    class Meta:
        model = models.Type
        fields = ('__all__')

class EventDocumentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="events:event-document-detail",
                    )

    event = serializers.HyperlinkedRelatedField(
                    many=False,
                    read_only=True,
                    view_name='events:event-detail',
                    )


    class Meta:
        model = models.EventDocument
        fields = ('__all__')

class ObservableField(serializers.Field):

    def to_representation(self, obj):
        return obj.uuid

    def to_internal_value(self, data):
        return data.strip(' ')


class EventObservablesSerializer(serializers.ModelSerializer):
    observable = ObservableField()
    event = serializers.PrimaryKeyRelatedField(read_only=True)

    id = serializers.ReadOnlyField()
    obs = None

    def validate_empty_values(self, data):
        if isinstance(data, str):
            data = {"observable" : data}
        return (False, data)

    def validate(self, attrs):
        return attrs

    class Meta:
        model = models.EventObservable
        fields = ('__all__')

    def to_representation(self, instance):
        ret = super(EventObservablesSerializer, self).to_representation(instance)
        return ret["observable"]

    def to_internal_value(self, instance):
        ret = super(EventObservablesSerializer, self).to_internal_value(instance)
        #print("event observ: %s" % ret)
        #ret["observable"] = ret["observable"].uuid
        return ret


    def update(self, instance, validated_data):

        try:
            observable = Observable.objects.get(uuid=validated_data["observable"])
            object, create = self.Meta.model.objects.get_or_create(observable=observable, event=instance)
            return object
        except Exception as error:
            raise serializers.ValidationError("%s" % error)


    @transaction.atomic
    def create(self, validated_data):
        return None



class EventSerializer(CountryFieldMixin, serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="events:event-detail",
                    )

    actor = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    observable = EventObservablesSerializer(many=True)
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()
    motive = MinMotiveSerializer(many=True)
    sector = MinSectorSerializer(many=True)

    class Meta:
        country_dict=True
        model = models.Event
        fields = ('__all__')
#        exclude = ("actor",)


    def to_internal_value(self, instance):
        ret = super(EventSerializer, self).to_internal_value(instance)
        return ret

    def get_serializer(self):
        serializers = {
            "sector": MinSectorSerializer,
            "motive": MinMotiveSerializer,
            "observable": EventObservablesSerializer
        }
        return serializers

    def get_field(self, instance):
        # don't add through tables
        fields = {
            "sector": instance.sector,
            "motive": instance.motive,
        }

        return fields

    def update(self, instance, validated_data):
        info = model_meta.get_field_info(instance)

        # update all values
        for attr, value in validated_data.items():
            # Deal with related fields
            if attr in info.relations and info.relations[attr].to_many:
                RelatedModel = info.relations[attr].related_model
                old = set(RelatedModel.objects.filter(event=instance.id))
                new = set()
                for item in value:
                    serializer = self.get_serializer()[attr](instance, data=item)
                    if serializer.is_valid():
                        new.add(serializer.save())
                    else:
                        print(serializer.errors)

                if isinstance(instance, self.Meta.model):
                    rm = old.difference(new)
                    get_field = self.get_field(instance)
                    for item in rm:
                        # special case since observable is a through table
                        if not attr in get_field:
                            item.delete()
                        else:
                            get_field[attr].remove(item)

                    add = new.difference(old)
                    for item in add:
                        # special case since observable is a through table
                        if attr in get_field:
                            item.event.add(instance)
                
            else:
                # set values to self
                setattr(instance, attr, value)

        instance.save()
        return instance

    @transaction.atomic
    def create(self, validated_data):


        ModelClass = self.Meta.model

        # Remove many-to-many relationships from validated_data.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        instance = self.Meta().model.objects.create(**validated_data)

        # maybe try remove many check ? we know they are many relations.
        for attr, value in many_to_many.items():
            # Deal with related fields
            if attr in info.relations and info.relations[attr].to_many:
                RelatedModel = info.relations[attr].related_model
                old = set(RelatedModel.objects.filter(event=instance.id))
                new = set()
                for item in value:
                    serializer = self.get_serializer()[attr](instance, data=item)
                    if serializer.is_valid():
                        new.add(serializer.save())
                    else:
                        print(serializer.errors)

                if isinstance(instance, self.Meta.model):
                    get_field = self.get_field(instance)
                    add = new.difference(old)
                    for item in add:
                        # special case since observable is a through table
                        if attr in get_field:
                            item.event.add(instance)


        return instance

