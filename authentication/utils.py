"""
Common API response utilities for consistent response format
"""
from rest_framework import status
from rest_framework.response import Response
from typing import Any, Dict, Optional, List
from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException
import logging

logger = logging.getLogger(__name__)


class APIResponse:
    """
    Standardized API response format for all endpoints
    """
    
    @staticmethod
    def success(
        data: Any = None,
        message: str = "Success",
        status_code: int = status.HTTP_200_OK,
        meta: Optional[Dict] = None
    ) -> Response:
        """
        Create a standardized success response
        
        Args:
            data: Response data
            message: Success message
            status_code: HTTP status code
            meta: Additional metadata
            
        Returns:
            Response: Standardized success response
        """
        response_data = {
            "success": True,
            "message": message,
            "data": data,
            "status_code": status_code
        }
        
        if meta:
            response_data["meta"] = meta
            
        return Response(response_data, status=status_code)
    
    @staticmethod
    def error(
        message: str = "An error occurred",
        status_code: int = status.HTTP_400_BAD_REQUEST,
        errors: Optional[List[str]] = None,
        error_code: Optional[str] = None,
        details: Optional[Dict] = None
    ) -> Response:
        """
        Create a standardized error response
        
        Args:
            message: Error message
            status_code: HTTP status code
            errors: List of specific errors
            error_code: Custom error code
            details: Additional error details
            
        Returns:
            Response: Standardized error response
        """
        response_data = {
            "success": False,
            "message": message,
            "status_code": status_code
        }
        
        if errors:
            response_data["errors"] = errors
            
        if error_code:
            response_data["error_code"] = error_code
            
        if details:
            response_data["details"] = details
            
        return Response(response_data, status=status_code)
    
    @staticmethod
    def validation_error(
        errors: Dict[str, List[str]],
        message: str = "Validation failed"
    ) -> Response:
        """
        Create a standardized validation error response
        
        Args:
            errors: Validation errors from serializer
            message: Error message
            
        Returns:
            Response: Standardized validation error response
        """
        # Get the first error message as a simple string
        first_error = None
        for field, field_errors in errors.items():
            if field_errors:
                first_error = f"{field_errors[0]}"
                break
        
        # Use the first error as the main message, or fallback to default
        error_message = first_error if first_error else message
        
        return APIResponse.error(
            message=error_message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="VALIDATION_ERROR",
            details={"validation_errors": errors}
        )
    
    @staticmethod
    def not_found(
        message: str = "Resource not found",
        resource_type: str = "Resource"
    ) -> Response:
        """
        Create a standardized not found response
        
        Args:
            message: Error message
            resource_type: Type of resource not found
            
        Returns:
            Response: Standardized not found response
        """
        return APIResponse.error(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND",
            details={"resource_type": resource_type}
        )
    
    @staticmethod
    def unauthorized(
        message: str = "Authentication required",
        error_code: str = "UNAUTHORIZED"
    ) -> Response:
        """
        Create a standardized unauthorized response
        
        Args:
            message: Error message
            error_code: Custom error code
            
        Returns:
            Response: Standardized unauthorized response
        """
        return APIResponse.error(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=error_code
        )
    
    @staticmethod
    def forbidden(
        message: str = "Access denied",
        error_code: str = "FORBIDDEN"
    ) -> Response:
        """
        Create a standardized forbidden response
        
        Args:
            message: Error message
            error_code: Custom error code
            
        Returns:
            Response: Standardized forbidden response
        """
        return APIResponse.error(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code=error_code
        )
    
    @staticmethod
    def server_error(
        message: str = "Internal server error",
        error_code: str = "SERVER_ERROR"
    ) -> Response:
        """
        Create a standardized server error response
        
        Args:
            message: Error message
            error_code: Custom error code
            
        Returns:
            Response: Standardized server error response
        """
        return APIResponse.error(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code=error_code
        )


class APIExceptionHandler:
    """
    Global exception handler for API responses
    """
    
    @staticmethod
    def handle_validation_error(exc: ValidationError) -> Response:
        """
        Handle Django validation errors
        
        Args:
            exc: ValidationError exception
            
        Returns:
            Response: Standardized error response
        """
        logger.error(f"Validation error: {exc}")
        return APIResponse.error(
            message="Validation failed",
            errors=[str(error) for error in exc.messages] if hasattr(exc, 'messages') else [str(exc)],
            error_code="VALIDATION_ERROR"
        )
    
    @staticmethod
    def handle_api_exception(exc: APIException) -> Response:
        """
        Handle DRF API exceptions
        
        Args:
            exc: APIException
            
        Returns:
            Response: Standardized error response
        """
        logger.error(f"API exception: {exc}")
        return APIResponse.error(
            message=exc.detail if isinstance(exc.detail, str) else str(exc.detail),
            status_code=exc.status_code,
            error_code=getattr(exc, 'error_code', 'API_ERROR')
        )
    
    @staticmethod
    def handle_generic_exception(exc: Exception) -> Response:
        """
        Handle generic exceptions
        
        Args:
            exc: Generic exception
            
        Returns:
            Response: Standardized error response
        """
        logger.error(f"Unexpected error: {exc}", exc_info=True)
        return APIResponse.server_error(
            message="An unexpected error occurred",
            error_code="UNEXPECTED_ERROR"
        )


def handle_api_exception(exc, context=None):
    """
    Global exception handler for DRF
    
    Args:
        exc: Exception
        context: Request context
        
    Returns:
        Response: Standardized error response
    """
    handler = APIExceptionHandler()
    
    if isinstance(exc, ValidationError):
        return handler.handle_validation_error(exc)
    elif isinstance(exc, APIException):
        return handler.handle_api_exception(exc)
    else:
        return handler.handle_generic_exception(exc)
