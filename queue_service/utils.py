
def group_has_label(label, lst):
    for item in lst:
        if item.data.get('label') == label:
            return True

    return False