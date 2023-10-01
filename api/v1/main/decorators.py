from rest_framework import status
from rest_framework.response import Response

def group_required(group_names):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                if (
                    not bool(request.user.groups.filter(name__in=group_names))
                    | request.user.is_superuser
                ):
                    response_data = {}
                    response_data["status"] = "false"
                    response_data["stable"] = "true"
                    response_data["title"] = "Permission Denied"
                    response_data[
                        "message"
                    ] = "You have no permission to do this action."
                    return Response(response_data, status=status.HTTP_200_OK)
            return view_method(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper