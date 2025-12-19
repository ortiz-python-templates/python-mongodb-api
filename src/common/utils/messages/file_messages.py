class FileMsg:

    class Success:
        UPLOADED = "File uploaded successfuly by user '{}'"
        DOWNLOADED = "File downloaded successfuly by user '{}'"
        DELETED = "File deleted successfuly by user '{}'"
        METADATA_UPDATED = "File metadata updated successfully"
        
    class Error:
        NOT_FOUND = "File with id '{}' not found"
        STORAGE_ERROR = "Could not connect to storage provider"
        CORRUPTED = "File integrity check failed (Checksum mismatch)"
        TOO_LARGE = "File size exceeds the limit of {}"
        INVALID_TYPE = "File type '{}' is not allowed"
        PERMISSION_DENIED = "User '{}' does not have permission to access this file"