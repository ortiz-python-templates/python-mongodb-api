class ProductMsg:
    
    class Success:
        CREATED = "Product '{}' has been successfully created."
        UPDATED = "Product '{}' has been successfully updated."
        ACTIVATED = "Product '{}' has been successfully activated."
        DEACTIVATED = "Product '{}' has been successfully deactivated."

    class Error:
        pass


class CategoryMsg:
    
    class Success:
        CREATED = "Category '{}' has been successfully created."
        UPDATED = "Category '{}' has been successfully updated."
        ACTIVATED = "Category '{}' has been successfully activated."
        DEACTIVATED = "Category '{}' has been successfully deactivated."

    class Error:
        pass
