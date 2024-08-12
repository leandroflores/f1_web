from fastapi import HTTPException, status


class HTTPExceptionFactory:
    @staticmethod
    def bad_request(message: str) -> HTTPException:
        """
        Creates an `fastapi.HTTPException` with status code 400 (bad request)
        and a detail message indicating that the provided request is invalid.

        Parameters:
            message (str): The message to include in the detail.

        Returns:
            :class:`fastapi.HTTPException`: The created Exception with a detail
            message "Bad request: {message}"
        """
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{message}",
        )

    @staticmethod
    def conflict(message: str) -> HTTPException:
        """
        Creates an `fastapi.HTTPException` with status code 409 (conflict) and
        a detail message indicating that the provided resource already exists.

        Parameters:
            resource (str): The resource that already exists.

        Returns:
            :class:`fastapi.HTTPException`: The created Exception with a detail
            message "{resource} already exists."
        """
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=message,
        )

    @staticmethod
    def not_found(resource: str) -> HTTPException:
        """
        Creates an `fastapi.HTTPException` with status code 404 (not found) and
        a detail message indicating that the provided resource does not exist.

        Parameters:
            resource (str): The resource that does not exist.

        Returns:
            :class:`fastapi.HTTPException`: The created Exception with a detail
            message "{resource} not found."
        """
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found.",
        )

    @staticmethod
    def credentials(
        msg: str = "Could not validate credentials",
    ) -> HTTPException:
        """
        Creates an `fastapi.HTTPException` with status code 401 (unauthorized),
        a detail message indicating that the provided credentials are invalid
        and a `WWW-Authenticate` header indicating the authentication scheme
        used.

        Returns:
            :class:`fastapi.HTTPException`: The created Exception with a detail
            message "Could not validate credentials."
        """
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=msg,
            headers={"WWW-Authenticate": "Bearer"},
        )
