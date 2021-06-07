def get_filter_payload(param):
    return (
        {"parent": None}
        if param.get("response_type") == "family"
        else {}
        if param.get("response_type") == "children"
        else None
    )
