class ReportMsg:

    class Success:
        GENERATED = "Report '{}' was generated successfully."
        EXPORTED = "Report '{}' was exported successfully."
        SENT = "Report '{}' was sent successfully."
        DELETED = "Report '{}' was deleted successfully."

    class Error:
        GENERATION_FAILED = "Failed to generate report '{}'."
        EXPORT_FAILED = "Failed to export report '{}'."
        SEND_FAILED = "Failed to send report '{}'."
        DELETE_FAILED = "Failed to delete report '{}'."
        NOT_FOUND = "Report '{}' was not found."
