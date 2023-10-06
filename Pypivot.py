# Step 1: Loading Data from CSV File
# 第一步，加载数据，由于数据不能使用pandas，openxl等库，只能用这种方式-利用csv文件加载。

def load_data(file_path):
    """
    从 CSV 文件中加载数据。

    参数:
        file_path (str): 文件的路径。

    返回:
        data (list of dict): 数据列表，其中每个条目是一个包含列名和值的字典。
        columns (list of str): 列名列表。
    """
    data = []
    columns = []

    with open(file_path, "r") as file:
        lines = file.readlines()
        columns = lines[0].strip().split(",")  # Assuming the first row contains column names
        for line in lines[1:]:  # Skipping the first row
            values = line.strip().split(",")
            row = {col: val for col, val in zip(columns, values)}
            data.append(row)

    return data, columns

# For testing purposes, let's manually create a small CSV file and load data from it.
# 为了测试数据，先生成一个小的数据集


# # Loading data from the created CSV file
# test_data, test_columns = load_data(test_csv)
# test_data,test_columns
#%%
# Step 2: Adding/Deleting Columns and Rows
# 添加行，列；删除行，列。

def add_column(data):
    """
    向数据集中添加一个新列。

    参数:
        data (list of dict): 数据列表。
        column_name (str): 新列的名称。
    """
    column_name = input(f"Add:")

    # 验证 column_name 是否是字母数字的
    if not column_name.isalnum():
        raise ValueError("列名称必须是字母数字的")

    # 如果数据集至少有一行，提示用户输入新列的默认值
    if len(data) > 0:
        default_value = input(f"请输入列 '{column_name}' 的默认值（直接按Enter使用基于1的索引编号）: ")
        if default_value == "":
            # 使用基于1的行索引编号作为默认值
            for i, row in enumerate(data):
                row[column_name] = i + 1
        else:
            # 使用用户输入的默认值
            for row in data:
                row[column_name] = default_value
    else:
        # 如果数据集为空，不进行任何操作
        pass



def delete_column(data):
    """
    从数据集中删除一个列。

    参数:
        data (list of dict): 数据列表。
        column_name (str): 要删除的列的名称。
    """
    column_name = input(f"Delete:")


    # 检查数据集是否至少有一行
    if len(data) == 0:
        print("数据集为空，没有列可以删除。")
        return

    # 检查要删除的列是否存在于数据集中
    if column_name not in data[0]:
        print(f"列 '{column_name}' 不存在于数据集中，无法删除。")
        return

    # 删除列
    for row in data:
        del row[column_name]

    print(f"列 '{column_name}' 已从数据集中删除。")



def add_row(data):
    """
    向数据集中添加一个新行。

    参数:
        data (list of dict): 数据列表。
    """
    # 检查数据集是否至少有一个列
    if len(data) == 0 or len(data[0]) == 0:
        print("数据集应至少包含一个列。")
        return

    # 获取数据集中的列名
    columns = list(data[0].keys())

    # 为新行创建一个字典，并提示用户为每个列输入值
    new_row = {}
    for column in columns:
        new_row[column] = input(f"'{column}':")

    # 将新行添加到数据集中
    data.append(new_row)



def delete_row(data):
    """
    从数据集中删除一个行。

    参数:
        data (list of dict): 数据列表。
        row_index (int): 要删除的行的索引（基于1）。
    """
    # 调整行索引以适应基于0的索引

    row_index = int(input("Delete:"))

    row_index -= 1

    # 检查行索引是否在有效范围内
    if 0 <= row_index < len(data):
        del data[row_index]
        print(f"第 {row_index + 1} 行已从数据集中删除。")
    else:
        print(f"错误：没有找到索引为 {row_index + 1} 的行。")
#%%
# Step 3: Defining Pivot Fields
# 数据透视表字段定义；

def view_pivot_fields(data_structure):
    """
    查看当前添加的透视表字段列表。

    参数:
        data_structure (dict): 存储透视字段的数据结构。
    """
    print("Columns:")
    print("•", "、".join([field[0] for field in data_structure["columns"]]))

    print("Rows:")
    print("•", "、".join([field[0] for field in data_structure["rows"]]))

    print("Values:")
    print("•", "、".join([f"{field[0]} – {field[1].capitalize()}" for field in data_structure["values"]]))


def add_pivot_field(data_structure):
    """
    通过提示用户输入属性名和字段类型来添加一个透视表字段。
    对于值字段，提示用户选择所需的聚合函数。
    参数:
        data_structure (dict): 存储透视字段的数据结构。
    """
    field_name = input("请输入属性名称: （在Name、Gender、Age、Employment（columns、rows）；Salary（values）中选择）: ")
    field_type = input("请输入字段类型（columns/rows/values）: ")

    if field_type not in ["columns", "rows", "values"]:
        print("无效的字段类型。必须是 'columns'、'rows' 或 'values'。")
        return

    if any(field_name in field[0] for field in data_structure[field_type]):
        print("错误：该属性已作为透视表字段添加。")
        return

    aggregation = None
    if field_type == "values":
        aggregation = input("请选择聚合函数（count/sum/average/minimum/maximum）: ")
        if aggregation not in ["count", "sum", "average", "minimum", "maximum"]:
            print("无效的聚合函数。")
            return

    data_structure[field_type].append(field_name)
    data_structure["funcs"].append(aggregation)
    print(f"{field_name} 已添加到 {field_type}。")


def remove_pivot_field(data_structure):
    """
    通过提示用户输入属性名称来删除一个透视表字段。

    参数:
        data_structure (dict): 存储透视字段的数据结构。
    """
    field_name = input("请输入要删除的属性名称: ")

    field_removed = False
    for field_type in ["columns", "rows", "values"]:
        original_length = len(data_structure[field_type])
        data_structure[field_type] = [field for field in data_structure[field_type] if field[0] != field_name]
        if len(data_structure[field_type]) < original_length:
            field_removed = True

    if field_removed:
        print(f"{field_name} 已从透视表字段中删除。")
    else:
        print("错误：该属性未作为透视表字段添加。")


#%%
#Step 10:生成多维透视表

def generate_pivot_table(data, row_keys, col_keys, value_key, aggregation_funcs):
    """
    生成透视表并在控制台上打印它。

    参数：
        data (list of dict): 数据列表，其中每个条目是一个包含列名和值的字典。
        row_keys (list of str): 用于行分组的列名的列表。
        col_keys (list of str): 用于列分组的列名的列表。
        value_key (str): 用于值字段的列名。
        aggregation_funcs (list of str): 用于聚合函数的列表。
    """
    pivot_data = {}

    for row in data:
        row_key = tuple(row[k] for k in row_keys)
        col_key = tuple(row[k] for k in col_keys)
        value = float(row[value_key])

        if row_key not in pivot_data:
            pivot_data[row_key] = {}
        if col_key not in pivot_data[row_key]:
            pivot_data[row_key][col_key] = {'sum': 0, 'count': 0, 'mean': 0}

        pivot_data[row_key][col_key]['sum'] += value
        pivot_data[row_key][col_key]['count'] += 1
        pivot_data[row_key][col_key]['mean'] = pivot_data[row_key][col_key]['sum'] / pivot_data[row_key][col_key][
            'count']

    unique_col_labels = sorted(list(set(col_key for row_data in pivot_data.values() for col_key in row_data.keys())))

    # 打印列标签
    for i in range(len(col_keys)):
        # 在第二行导入行标签
        row_labels = "/".join(row_keys)
        col_labels_line = [row_labels] + [""] * (len(row_keys) - 1) + [str(col[i]) for col in unique_col_labels for _ in
                                                                       aggregation_funcs] + [""]
        print(",".join(col_labels_line))
    func_labels_line = [""] * len(row_keys) + [func for _ in unique_col_labels for func in aggregation_funcs] + [""]
    print(",".join(func_labels_line))

    total_per_col = [0] * len(unique_col_labels) * len(aggregation_funcs)
    total_all = 0

    for row_key, row_data in pivot_data.items():
        row = [str(item) for item in row_key]
        row_total = 0

        for col_key in unique_col_labels:
            for func in aggregation_funcs:
                value = row_data.get(col_key, {}).get(func, None)
                row.append(str(value))
        print(",".join(row))


#Step 11:多维透视表加入统计

def generate_pivot_table_no_csv(data, row_keys, col_keys, value_key, aggregation_funcs, output_file):
    """
    生成透视表并将其保存到CSV文件中。

    参数：
        data (list of dict): 数据列表，其中每个条目是一个包含列名和值的字典。
        row_keys (list of str): 用于行分组的列名的列表。
        col_keys (list of str): 用于列分组的列名的列表。
        value_key (str): 用于值字段的列名。
        aggregation_funcs (list of str): 用于聚合函数的列表。
        output_file (str): 输出文件的路径。
    """
    pivot_data = {}

    for row in data:
        row_key = tuple(row[k] for k in row_keys)
        col_key = tuple(row[k] for k in col_keys)
        value = float(row[value_key])

        if row_key not in pivot_data:
            pivot_data[row_key] = {}
        if col_key not in pivot_data[row_key]:
            pivot_data[row_key][col_key] = {'sum': 0, 'count': 0, 'mean': 0}

        pivot_data[row_key][col_key]['sum'] += value
        pivot_data[row_key][col_key]['count'] += 1
        pivot_data[row_key][col_key]['mean'] = pivot_data[row_key][col_key]['sum'] / pivot_data[row_key][col_key][
            'count']

    unique_col_labels = sorted(list(set(col_key for row_data in pivot_data.values() for col_key in row_data.keys())))

    with open(output_file, 'w', newline='') as file:
        # 写入列标签
        for i in range(len(col_keys)):
            # 在第二行导入行标签
            row_labels = "/".join(row_keys)
            col_labels_line = [row_labels] + [""] * (len(row_keys) - 1) + [str(col[i]) for col in unique_col_labels for
                                                                           _ in aggregation_funcs] + [""]
            file.write(",".join(col_labels_line) + "\n")
        func_labels_line = [""] * len(row_keys) + [func for _ in unique_col_labels for func in aggregation_funcs] + [""]
        file.write(",".join(func_labels_line) + "\n")

        total_per_col = [0] * len(unique_col_labels) * len(aggregation_funcs)
        total_all = 0

        for row_key, row_data in pivot_data.items():
            row = [str(item) for item in row_key]
            row_total = 0

            for col_key in unique_col_labels:
                for func in aggregation_funcs:
                    value = row_data.get(col_key, {}).get(func, None)
                    row.append(" " if value is None else str(value))  # Update here
                    if value is not None:
                        col_index = unique_col_labels.index(col_key) * len(aggregation_funcs) + aggregation_funcs.index(
                            func)
                        total_per_col[col_index] += value
                        row_total += value
                        total_all += value

            row.append(str(row_total))
            file.write(",".join(row) + "\n")

        total_per_col_str = [str(val) for val in total_per_col]
        file.write("Total," + ",".join(total_per_col_str) + f",{total_all}\n")


def generate_pivot_table_console(data, row_keys, col_keys, value_key, aggregation_funcs):
    """
    生成透视表并在控制台上打印它。

    参数：
        data (list of dict): 数据列表，其中每个条目是一个包含列名和值的字典。
        row_keys (list of str): 用于行分组的列名的列表。
        col_keys (list of str): 用于列分组的列名的列表。
        value_key (str): 用于值字段的列名。
        aggregation_funcs (list of str): 用于聚合函数的列表。
    """
    pivot_data = {}

    for row in data:
        row_key = tuple(row[k] for k in row_keys)
        col_key = tuple(row[k] for k in col_keys)
        value = float(row[value_key])

        if row_key not in pivot_data:
            pivot_data[row_key] = {}
        if col_key not in pivot_data[row_key]:
            pivot_data[row_key][col_key] = {'sum': 0, 'count': 0, 'mean': 0}

        pivot_data[row_key][col_key]['sum'] += value
        pivot_data[row_key][col_key]['count'] += 1
        pivot_data[row_key][col_key]['mean'] = pivot_data[row_key][col_key]['sum'] / pivot_data[row_key][col_key][
            'count']

    unique_col_labels = sorted(list(set(col_key for row_data in pivot_data.values() for col_key in row_data.keys())))

    # 打印列标签
    for i in range(len(col_keys)):
        # 在第二行导入行标签
        row_labels = "/".join(row_keys)
        col_labels_line = [row_labels] + [""] * (len(row_keys) - 1) + [str(col[i]) for col in unique_col_labels for _ in
                                                                       aggregation_funcs] + [""]
        print(",".join(col_labels_line))
    func_labels_line = [""] * len(row_keys) + [func for _ in unique_col_labels for func in aggregation_funcs] + [""]
    print(",".join(func_labels_line))

    total_per_col = [0] * len(unique_col_labels) * len(aggregation_funcs)
    total_all = 0

    for row_key, row_data in pivot_data.items():
        row = [str(item) for item in row_key]
        row_total = 0

        for col_key in unique_col_labels:
            for func in aggregation_funcs:
                # 此处填充数值
                value = row_data.get(col_key, {}).get(func, None)
                row.append(str(value))
                # 此处引入列总计，行总计
                if value is not None:
                    col_index = unique_col_labels.index(col_key) * len(aggregation_funcs) + aggregation_funcs.index(
                        func)
                    total_per_col[col_index] += value
                    row_total += value
                    total_all += value

        row.append(str(row_total))
        print(",".join(row))

    total_per_col_str = [str(val) for val in total_per_col]
    print("Total," + ",".join(total_per_col_str) + f",{total_all}")

#%%
# 定义测试数据
primary_data = [
    {"S/N": 1, "Name": "Albert", "Gender": "Male", "Age": 21, "Employment": "Employee", "Salary": 4800},
    {"S/N": 2, "Name": "Bob", "Gender": "Male", "Age": 21, "Employment": "Employee", "Salary": 5000},
    {"S/N": 3, "Name": "Charles", "Gender": "Male", "Age": 22, "Employment": "Employee", "Salary": 6000},
    {"S/N": 4, "Name": "Derrick", "Gender": "Male", "Age": 23, "Employment": "Self-Employed", "Salary": 10000},
    {"S/N": 5, "Name": "Fred", "Gender": "Male", "Age": 23, "Employment": "Unemployed", "Salary": 1200},
    {"S/N": 6, "Name": "George", "Gender": "Male", "Age": 25, "Employment": "Self-Employed", "Salary": 12000},
    {"S/N": 7, "Name": "Hubert", "Gender": "Male", "Age": 26, "Employment": "Unemployed", "Salary": 1000},
    {"S/N": 8, "Name": "Issac", "Gender": "Male", "Age": 28, "Employment": "Employee", "Salary": 3000},
    {"S/N": 9, "Name": "John", "Gender": "Male", "Age": 30, "Employment": "Employee", "Salary": 2500},
    {"S/N": 10, "Name": "Kerry", "Gender": "Male", "Age": 30, "Employment": "Self-Employed", "Salary": 8500},
    {"S/N": 11, "Name": "Linda", "Gender": "Female", "Age": 21, "Employment": "Self-Employed", "Salary": 9000},
    {"S/N": 12, "Name": "Mindy", "Gender": "Female", "Age": 21, "Employment": "Self-Employed", "Salary": 8500},
    {"S/N": 13, "Name": "Nicole", "Gender": "Female", "Age": 22, "Employment": "Unemployed", "Salary": 2000},
    {"S/N": 14, "Name": "Oprah", "Gender": "Female", "Age": 22, "Employment": "Employee", "Salary": 6500},
    {"S/N": 15, "Name": "Penny", "Gender": "Female", "Age": 23, "Employment": "Employee", "Salary": 7500},
    {"S/N": 16, "Name": "Queenie", "Gender": "Female", "Age": 25, "Employment": "Employee", "Salary": 7000},
    {"S/N": 17, "Name": "Ruby", "Gender": "Female", "Age": 25, "Employment": "Employee", "Salary": 4000},
    {"S/N": 18, "Name": "Stacy", "Gender": "Female", "Age": 27, "Employment": "Employee", "Salary": 3500},
    {"S/N": 19, "Name": "Tiffany", "Gender": "Female", "Age": 27, "Employment": "Self-Employed", "Salary": 5000},
    {"S/N": 20, "Name": "Ursula", "Gender": "Female", "Age": 27, "Employment": "Unemployed", "Salary": 1500},
]

test_csv = 'Data/test_data_1.csv'  # 你可以指定你想要的文件名

# 打开文件以写入数据
with open(test_csv, "w") as file:
    # 写入头部信息
    file.write("S/N,Name,Gender,Age,Employment,Salary\n")

    # 遍历 primary_data 并将每一行数据写入文件
    for data in primary_data:
        file.write(f"{data['S/N']},{data['Name']},{data['Gender']},{data['Age']},{data['Employment']},{data['Salary']}\n")

#%%

def main_menu():
    """
    主菜单：展示功能列表，获取用户输入，并调用相应的功能。
    """
    # 推荐的执行顺序
    recommended_order = [1,2,3,4,5]
    current_step = 0  # 跟踪当前步骤

    while True:  # 主循环，除非选择退出，否则一直运行
        # 显示功能列表及推荐的执行顺序
        print("\n请选择一个功能（按推荐顺序执行）：")
        print("1(1): 加载数据")
        print("2(3): 添加/删除 列/行")
        print("3(2): 定义透视表字段")
        print("4(4): 生成多维透视表")
        print("5: 退出程序")

        # 获取用户输入
        choice = input("输入数字选择功能：")

        # 如果输入是一个数字，并且这个数字是推荐的下一个步骤，更新current_step
        if choice.isdigit() and int(choice) == recommended_order[current_step]:
            current_step += 1
        elif not choice.isdigit() or int(choice) not in recommended_order:
            # 如果输入不是一个数字，或者数字不在推荐的步骤中，显示错误消息
            print("无效输入，请输入1-5的数字选择功能。")
            continue
        elif int(choice) != recommended_order[current_step]:
            # 如果数字不是推荐的下一个步骤，显示错误消息
            print("请按照推荐的顺序执行功能。")
            continue

        # 根据用户输入执行相应功能
        if choice == "1":
            print("功能1: 加载数据")
            test_data, test_columns = load_data(test_csv)
            input("按Enter键返回主菜单")
        elif choice == "2":
            print("功能2: 添加/删除 列/行")
            # Testing the functions

            # 测试函数
            # Adding a column
            add_column(test_data)
            print("After adding column:", test_data)

            # Deleting a column
            delete_column(test_data)
            print("After deleting column:", test_data)

            # Adding a row
            add_row(test_data)
            print("After adding row:", test_data)

            # Deleting a row
            delete_row(test_data)  # Deleting the row we just added
            print("After deleting row:", test_data)
            input("按Enter键返回主菜单")

        elif choice == "3":
            print("功能3: 定义透视表字段")

            # 初始化一个空的透视表字段数据结构
            pivot_fields = {
                "rows": [],
                "columns": [],
                "values": [],
                "funcs":[]
            }

            # 一个子菜单，允许用户多次添加或删除字段，直到他们选择完成
            while True:
                # 显示当前的透视表字段
                print("当前状态：")
                view_pivot_fields(pivot_fields)

                print("\n请选择一个功能：")
                print("1: 添加字段")
                print("2: 删除字段")
                print("3: 完成定义")

                sub_choice = input("输入数字选择功能：")

                # 添加字段
                if sub_choice == "1":
                    print("\n添加字段：")
                    try:
                        add_pivot_field(pivot_fields)
                    except Exception as e:
                        print(str(e))

                # 删除字段
                elif sub_choice == "2":
                    print("\n删除字段：")
                    try:
                        remove_pivot_field(pivot_fields)
                    except Exception as e:
                        print(str(e))

                # 完成定义，返回主菜单
                elif sub_choice == "3":
                    print("\n完成定义，返回主菜单。")
                    break

                # 无效输入
                else:
                    print("\n无效输入，请输入1-3的数字选择功能。")

            input("按Enter键返回主菜单")

        elif choice == "4":
            print("功能4: 生成多维透视表")
            # 用于测试的函数调用参数
            row_keys_test = pivot_fields["rows"]
            print(row_keys_test)
            col_keys_test = pivot_fields["columns"]
            print(col_keys_test)
            value_key_test = pivot_fields["values"][0]
            print(value_key_test)
            aggregation_funcs_test = [func for func in pivot_fields["funcs"] if func is not None]
            print(aggregation_funcs_test)
            output_file_test = "output_test8.csv"  #若导出文件，需修改路径名

            # 如果不导出文件，可以不使用这一函数，如果导出文件，需要取消注释，生成到对应目录下；
            # 再次测试函数
            generate_pivot_table_no_csv(test_data,row_keys_test, col_keys_test, value_key_test, aggregation_funcs_test, output_file_test)

            # 验证生成的CSV文件
            with open(output_file_test, "r") as file:
                print(file.read())

            # 使用先前定义的测试数据和参数调用函数,这里直接在控制台动态显示
            generate_pivot_table(
                test_data,
                row_keys_test,
                col_keys_test,
                value_key_test,
                aggregation_funcs_test
            )

            generate_pivot_table_console(
                test_data,
                row_keys_test,
                col_keys_test,
                value_key_test,
                aggregation_funcs_test
            )

            input("按Enter键返回主菜单")
        elif choice == "5":
            print("退出程序")
            break

# 运行主菜单
main_menu()