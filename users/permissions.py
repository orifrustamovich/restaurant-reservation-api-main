from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Faqat restaurant owner uchun ruxsat"""

    message = "Only restaurant owners can perform this action"

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.is_owner
        )


class IsCustomer(BasePermission):
    """Faqat customer uchun ruxsat"""

    message = "Only customers can perform this action"

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.is_customer
        )


class IsOwnerOrReadOnly(BasePermission):
    """O'qish — hamma, yozish — faqat restoran egasi"""

    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return obj.owner == request.user


class IsReservationOwner(BasePermission):
    """Faqat o'z bronini ko'ra/o'zgartira oladi"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if request.user.is_owner:
            return obj.table.restaurant.owner == request.user
        return obj.customer == request.user
