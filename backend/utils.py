def deduplication(row_data: list):
    try:
        seen = set()
        unique_list = list()
        for items in row_data:
            tupled_item = tuple(items)
            if tupled_item not in seen:
                seen.add(tupled_item)
                unique_list.append(items)
        print("Deduplication done.")
        return unique_list
    except Exception as e:
        print(f"Problem occured as {e}")

def trimEmptyString(list_events: list):
    clean_list = []
    for events in range(len(list_events)):
        clean_event = []
        for indices in range(len(list_events[events])):
            if list_events[events][indices] != '':
                clean_event.append(list_events[events][indices])
        clean_list.append(clean_event)
    return clean_list