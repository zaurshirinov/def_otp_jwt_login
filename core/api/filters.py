class ManualFilter:

    @staticmethod
    def apply_filter(queryset, params):
        status = params.get("status")
        if status:
            queryset = queryset.filter(status__iexact=status)

        created_at = params.get("created_at")
        if created_at:
            queryset = queryset.filter(created_at__date=created_at)

        search_title = params.get("title")
        if search_title:
            queryset = queryset.filter(title__icontains=search_title)

        return queryset
    