from rest_framework import serializers

from .models import Person


class PersonSerializer(serializers.ModelSerializer):
    """
    Serializer created for person list response.
    """

    class Meta:
        model = Person
        fields = ("id", "first_name")


class PersonUpdateSerializer(PersonSerializer):
    """
    Serializer created to update person instance.
    """

    parent_id = serializers.IntegerField(source="parent")

    class Meta:
        model = Person
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "email_address",
            "address",
            "date_of_birth",
            "parent_id",
        )


class PersonResponseSerializer(serializers.ModelSerializer):
    """
    Serializer created for customize response.
    """

    parent = serializers.SerializerMethodField("get_parent")
    children = serializers.SerializerMethodField("get_child")
    grand_father = serializers.SerializerMethodField("get_grand_father")
    sibling = serializers.SerializerMethodField("get_sibling")
    cousins = serializers.SerializerMethodField("get_cousins")

    class Meta:
        model = Person
        fields = (
            "id",
            "first_name",
            "parent",
            "children",
            "grand_father",
            "sibling",
            "cousins",
        )

    @staticmethod
    def get_parent(attrs):
        return PersonSerializer(attrs.parent).data if attrs.parent else None

    @staticmethod
    def get_child(attrs):
        return (
            PersonSerializer(attrs.persons_on_parent.filter(), many=True).data
            if attrs
            else None
        )

    @staticmethod
    def get_grand_father(attrs):
        parent = attrs.parent
        return (
            PersonSerializer(attrs.parent.parent).data
            if parent and parent.parent
            else None
        )

    @staticmethod
    def get_sibling(attrs):
        parent = attrs.parent
        return (
            PersonSerializer(
                parent.persons_on_parent.exclude(id=attrs.id), many=True
            ).data
            if parent
            else None
        )

    @staticmethod
    def get_cousins(attrs):
        parent = attrs.parent
        grand_father = parent.parent if parent else None
        brother_of_parent = (
            grand_father.persons_on_parent.exclude(id=parent.id) if grand_father else []
        )
        x = []
        [x.extend(a.persons_on_parent.filter()) for a in brother_of_parent]
        return PersonSerializer(x, many=True).data if parent else None
