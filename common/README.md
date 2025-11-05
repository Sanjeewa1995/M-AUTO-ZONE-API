# Common App

This app contains shared utilities and helpers that are used across multiple apps in the project.

## Structure

```
common/
├── __init__.py
├── utils.py          # Common utilities (APIResponse, exception handlers, etc.)
├── services/         # Shared services (optional - for future services)
├── helpers/          # Helper functions (optional - for future helpers)
└── constants.py      # Shared constants (optional - for future constants)
```

## Usage

### Importing Common Utilities

```python
# Import APIResponse for standardized responses
from common.utils import APIResponse

# Use in views
return APIResponse.success(data=my_data, message="Operation successful")
return APIResponse.error(message="Something went wrong", status_code=400)
```

### What Goes Here

- **API Response Utilities**: Standardized response formats
- **Exception Handlers**: Global exception handling
- **Helper Functions**: Reusable utility functions
- **Constants**: Shared constants across apps
- **Services**: Shared services (email, SMS, etc.) that multiple apps use

### What Doesn't Go Here

- **App-specific logic**: Keep app-specific code in their respective apps
- **Models**: Models belong in their respective apps
- **Views/URLs**: These belong in their respective apps

