async def read_csv_file(constructor, file_path: str, separator: str = ','):
    with open(file_path, "r") as fileContent:
        lines = fileContent.readlines()
        result_list = []

        row = 0
        for line in lines:
            columns = line.split(separator)
            result_item = columns if constructor is None else constructor(row + 1, columns)
            if result_item is not None:
                result_list.append(result_item)
                row += 1

        return result_list
