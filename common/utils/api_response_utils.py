"""
Common API response utilities for consistent response format
Shared across all apps in the project
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
            errors: List of error messages
            error_code: Error code for frontend handling
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
            errors: Dictionary of field errors
            message: Error message
            
        Returns:
            Response: Standardized validation error response
        """
        # Get the first error message as a simple string
        first_field = list(errors.keys())[0] if errors else None
        first_error = errors[first_field][0] if first_field and errors[first_field] else None
        
        # Use the first error as the main message, or fallback to default
        error_message = first_error if first_error else message
        
        return Response({
            "success": False,
            "message": error_message,
            "errors": errors,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "error_code": "VALIDATION_ERROR"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def not_found(
        message: str = "Resource not found",
        error_code: str = "NOT_FOUND"
    ) -> Response:
        """
        Create a standardized not found response
        
        Args:
            message: Error message
            error_code: Error code
            
        Returns:
            Response: Standardized not found response
        """
        return Response({
            "success": False,
            "message": message,
            "status_code": status.HTTP_404_NOT_FOUND,
            "error_code": error_code
        }, status=status.HTTP_404_NOT_FOUND)
    
    @staticmethod
    def unauthorized(
        message: str = "Authentication required",
        error_code: str = "UNAUTHORIZED"
    ) -> Response:
        """
        Create a standardized unauthorized response
        
        Args:
            message: Error message
            error_code: Error code
            
        Returns:
            Response: Standardized unauthorized response
        """
        return Response({
            "success": False,
            "message": message,
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "error_code": error_code
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    @staticmethod
    def forbidden(
        message: str = "Access denied",
        error_code: str = "FORBIDDEN"
    ) -> Response:
        """
        Create a standardized forbidden response
        
        Args:
            message: Error message
            error_code: Error code
            
        Returns:
            Response: Standardized forbidden response
        """
        return Response({
            "success": False,
            "message": message,
            "status_code": status.HTTP_403_FORBIDDEN,
            "error_code": error_code
        }, status=status.HTTP_403_FORBIDDEN)
    
    @staticmethod
    def server_error(
        message: str = "Internal server error",
        error_code: str = "SERVER_ERROR"
    ) -> Response:
        """
        Create a standardized server error response
        
        Args:
            message: Error message
            error_code: Error code
            
        Returns:
            Response: Standardized server error response
        """
        return Response({
            "success": False,
            "message": message,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "error_code": error_code
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        
        # Handle token authentication errors with simple messages
        if exc.status_code == 401:
            # Check if it's a token-related error
            error_detail = exc.detail
            is_token_error = False
            error_message = "Unauthorized user"
            
            # Check various ways token errors might be represented
            if isinstance(error_detail, dict):
                # Check for token_not_valid or similar keys
                if 'code' in error_detail and 'token_not_valid' in str(error_detail.get('code', '')):
                    is_token_error = True
                elif 'detail' in error_detail and 'token' in str(error_detail.get('detail', '')).lower():
                    is_token_error = True
                elif 'messages' in error_detail:
                    # Check messages array for token errors
                    messages = error_detail.get('messages', [])
                    if messages and isinstance(messages, list):
                        for msg in messages:
                            if isinstance(msg, dict) and ('token' in str(msg).lower() or 'invalid' in str(msg).lower()):
                                is_token_error = True
                                break
            elif isinstance(error_detail, str):
                if 'token' in error_detail.lower() and ('invalid' in error_detail.lower() or 'expired' in error_detail.lower()):
                    is_token_error = True
            elif hasattr(error_detail, '__str__'):
                error_str = str(error_detail).lower()
                if 'token' in error_str and ('invalid' in error_str or 'expired' in error_str or 'token_not_valid' in error_str):
                    is_token_error = True
            
            if is_token_error:
                return APIResponse.unauthorized(
                    message="Unauthorized user. Please login again.",
                    error_code="UNAUTHORIZED"
                )
            
            # Other 401 errors
            return APIResponse.unauthorized(
                message="Authentication required",
                error_code="UNAUTHORIZED"
            )
        
        # Handle other API exceptions
        # Extract message from error detail
        if isinstance(exc.detail, str):
            message = exc.detail
        elif isinstance(exc.detail, dict):
            # Try to extract a simple message from dict
            if 'detail' in exc.detail:
                message = str(exc.detail['detail'])
            elif 'message' in exc.detail:
                message = str(exc.detail['message'])
            else:
                message = "An error occurred"
        elif isinstance(exc.detail, list) and len(exc.detail) > 0:
            message = str(exc.detail[0])
        else:
            message = str(exc.detail) if exc.detail else "An error occurred"
        
        return APIResponse.error(
            message=message,
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
    Global exception handler function for DRF
    
    Args:
        exc: Exception instance
        context: Request context
        
    Returns:
        Response: Standardized error response
    """
    if isinstance(exc, ValidationError):
        return APIExceptionHandler.handle_validation_error(exc)
    elif isinstance(exc, APIException):
        return APIExceptionHandler.handle_api_exception(exc)
    else:
        return APIExceptionHandler.handle_generic_exception(exc)
