from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Person
from .serializers import (PersonResponseSerializer, PersonSerializer,
                          PersonUpdateSerializer)
from .services import PersonResetService, PersonUpdateService


class BaseView(APIView):
    """
    View created for common configurations.
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class LogoutView(BaseView):
    """
    View create to logout current user.
    """

    @staticmethod
    def post(request):
        request.auth.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class FamilyListView(BaseView):
    """
    View create to send list of families.
    """

    @staticmethod
    def get(_):
        return Response(
            PersonSerializer(Person.objects.filter(parent=None), many=True).data
        )


class PersonListView(BaseView):
    """
    View created to send list of all persons.
    """

    @staticmethod
    def get(_, family_id):
        return Response(
            PersonResponseSerializer(Person.objects.filter(), many=True).data
        )


class PersonDetailView(BaseView):
    """
    View created to get detail, reset, update and delete the single instance of person.
    """

    @staticmethod
    def get(_, person_id):
        try:
            person = Person.objects.filter(id=person_id)
            return Response(PersonResponseSerializer(person, many=True).data)
        except Person.DoesNotExist:
            return Response(
                {"Error": "Person does not exists"}, status=status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def put(request, person_id):
        payload = PersonUpdateSerializer(data=request.data)
        if payload.is_valid(raise_exception=True):
            return PersonResetService.execute(
                {"person_id": person_id, "payload": payload.validated_data}
            )

    @staticmethod
    def patch(request, person_id):
        payload = PersonUpdateSerializer(data=request.data, partial=True)
        if payload.is_valid(raise_exception=True):
            return PersonUpdateService.execute(
                {"person_id": person_id, "payload": payload.validated_data}
            )

    @staticmethod
    def delete(_, person_id):
        try:
            person = Person.objects.filter(id=person_id)
            person.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Person.DoesNotExist:
            return Response(
                {"Error": "Person does not exists"}, status=status.HTTP_400_BAD_REQUEST
            )
