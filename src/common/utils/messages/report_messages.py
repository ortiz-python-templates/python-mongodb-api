class ReportMsg:

    class Success:
        GENERATED = "Report '{}' was generated successfully."
        EXPORTED = "Report '{}' was exported successfully."
        DELETED = "Report '{}' was deleted successfully."

    class Error:
        GENERATION_FAILED = "Failed to generate report '{}'."
        EXPORT_FAILED = "Failed to export report '{}'."
        DELETE_FAILED = "Failed to delete report '{}'."
        NOT_FOUND = "Report '{}' was not found."
