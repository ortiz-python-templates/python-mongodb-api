class SwaggerConfig:
    config = {
        "title": "Python MongoDB API",
        "version": "1.0.0",
        "description": "Product Management API.",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "openapi_tags": [

            {"name": "API Root", "description": "Endpoints needed to Introduce API"},
            {"name": "API Health", "description": "Endpoints needed check API Health"},

            {"name": "Identity", "description": "Endpoints for authentication, users, and roles"},
            {"name": "Identity / Roles", "description": "Manage roles and permissions"},
            {"name": "Identity / Users", "description": "Manage users"},
            {"name": "Identity / Authentication", "description": "Manage: login, logout, current user"},
            {"name": "Identity / User Attachments", "description": "Manage all user file/attachments"},
            {"name": "Identity / Login Activities", "description": "Manage: login activities: last login, logout, ..."},
            
            {"name": "Configurations", "description": "Endpoints for application configurations"},
            {"name": "Configurations / Basic Configurations", "description": "Manage Basic configurations"},
            {"name": "Configurations / Company Configurations", "description": "Manage Company configurations"},
            {"name": "Configurations / Feature Flags", "description": "Manage Feature flag"},

            {"name": "Files", "description": "Manage Files: upload, download, delete, ..."},
        ]
    }
