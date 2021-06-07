from rest_framework import status
from rest_framework.response import Response
from service_objects.services import Service

from .models import Person


class PersonResetService(Service):
    """
    Service created to reset the person object
    """

    def process(self):
        Person.objects.filter(id=self.data.get("person_id")).uddate(
            **self.data.get("payload")
        )
        return Response({}, status=status.HTTP_205_RESET_CONTENT)


class PersonUpdateService(Service):
    """
    Service created to update the person object
    """

    def process(self):
        try:
            person = Person.objects.get(id=self.data.get("person_id"))
            for key, value in self.data["payload"].items():
                if key == "parent_id":
                    key = "parent"
                    value = Person.objects.get(id=value)
                setattr(person, key, value)
            person.save()
            return Response({}, status=status.HTTP_200_OK)
        except Person.DoesNotExist:
            return Response({"Error": "Person does not exist"})
