"""
Application constants
"""

# Document Types
DOCUMENT_TYPES = {
    'EMIRATES_ID': 'Emirates ID',
    'TRADE_LICENSE': 'Trade License',
    'DESIGN': 'Design File',
    'OTHER': 'Other',
}

# Order Statuses
ORDER_STATUSES = {
    'PENDING': 'Pending',
    'CONFIRMED': 'Confirmed',
    'PROCESSING': 'Processing',
    'READY': 'Ready',
    'SHIPPED': 'Shipped',
    'DELIVERED': 'Delivered',
    'CANCELLED': 'Cancelled',
}

# Payment Statuses
PAYMENT_STATUSES = {
    'PENDING': 'Pending',
    'PAID': 'Paid',
    'FAILED': 'Failed',
    'REFUNDED': 'Refunded',
}

# File Upload Limits
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

# Allowed File Extensions
ALLOWED_DOCUMENT_EXTENSIONS = [
    'pdf', 'jpg', 'jpeg', 'png', 'ai', 'eps', 'psd', 'cdr', 'svg', 'doc', 'docx'
]

ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp']

