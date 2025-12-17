class AuthMsg:
    
    class Success:
        USER_REGISTERED = "Welcome, '{}'! Your registration has been completed successfully."
        USER_LOGGED_OUT = "'{}' has logged out successfully. See you soon!"
        EMAIL_SENT = "Email sent successfully. Please check your inbox."
        PASSWORD_RESET = "Your password has been reset successfully."

    class Error:
        INVALID_CREDENTIALS = "Incorrect username or password. Please try again."
        INVALID_REFRESH_TOKEN = "Session expired. Please log in again."


class UserMsg:

    class Success:
        CREATED = "User '{}' has been created successfully."
        UPDATED = "User '{}' has been updated successfully."
        DELETED = "User '{}' has been deleted successfully."
        ACTIVATED = "User '{}' has been activated successfully."
        DEACTIVATED = "User '{}' has been deactivated successfully."
        PASSWORD_CHANGED = "User '{}' password has been changed successfully."

    class Error:
        NOT_FOUND = "User not found."
        CREATING = "An error occurred while creating the user. Please try again."

class UserAttachmentMsg:

    class Success:
        CREATED = "User Attachment for user '{}' has been created successfully."
        UPDATED = "User Attachment  for user '{}' has been updated successfully."
