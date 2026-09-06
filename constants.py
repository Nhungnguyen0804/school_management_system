import enum
class EnrollmentStatus(str, enum.Enum): # enum là Liệt kê
    ACTIVE = "ACTIVE"          # Đang học
    CANCELLED = "CANCELLED"    # Đã hủy / Rút môn
    COMPLETED = "COMPLETED"    # Đã hoàn thành môn