def merge_all_tables(infos):
    merged_table = infos[0].copy()
    for i, table in enumerate(infos):
        if i != 0:
            merged_table = merged_table.add(table, fill_value=0)

    return merged_table
