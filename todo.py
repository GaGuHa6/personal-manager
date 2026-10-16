# 导入 sys 模块，用来修改标准输出的编码，解决 Windows 终端中文乱码
import sys
# 把标准输出重新配置为 UTF-8 编码，这样 print 中文就不会变成方块
sys.stdout.reconfigure(encoding="utf-8")

# 导入 json 模块，用来把数据存成 JSON 文件，以及从 JSON 文件读回来
import json


# 定义一个 Task 类，表示“一个任务”
class Task:
    # 初始化方法，创建 Task 对象时自动调用
    # id：任务编号；title：任务标题；done：是否完成，默认 False
    def __init__(self, id, title, done=False):
        self.id = id          # 把传入的 id 存到对象自己的属性里
        self.title = title    # 把传入的 title 存到对象自己的属性里
        self.done = done      # 把传入的 done 存到对象自己的属性里

    # 把 Task 对象转成字典，方便存成 JSON
    # JSON 不认识 Python 对象，只认识字典、列表、字符串、数字这些
    def to_dict(self):
        return {"id": self.id, "title": self.title, "done": self.done}

    # 定义 print(task) 时显示什么内容
    # 这个方法会在打印对象时自动被调用
    def __str__(self):
        # 如果 done 是 True，mark 就是 "✓"，否则是空格
        mark = "✓" if self.done else " "
        # 返回格式化后的字符串，例如 "[ ] 1. 学 Python"
        return f"[{mark}] {self.id}. {self.title}"


# 定义一个 TaskList 类，表示“任务列表”，管理所有 Task 对象
class TaskList:
    # 初始化方法，创建一个空的任务列表
    def __init__(self):
        self.tasks = []      # 用来存放所有 Task 对象的列表
        self.next_id = 1     # 下一个要分配的任务编号，只增不减，避免重复

    # 添加任务
    # title：任务标题
    def add(self, title):
        # 用当前的 next_id 创建一个新 Task 对象
        task = Task(id=self.next_id, title=title)
        # 把 next_id 加 1，为下一个任务做准备
        self.next_id += 1
        # 把新任务追加到任务列表里
        self.tasks.append(task)
        # 打印提示，这里会自动调用 Task 的 __str__ 方法
        print("已添加:", task)

    # 显示所有任务
    def show(self):
        # 如果任务列表为空，提示并直接返回
        if not self.tasks:
            print("暂无任务")
            return
        # 遍历每个任务，逐个打印
        for t in self.tasks:
            print(t)         # 这里也会自动调用 Task 的 __str__

    # 把任务列表保存到 JSON 文件
    def save(self):
        # 用 with open 打开文件，模式 "w" 表示写入
        # encoding="utf-8" 保证中文能正确保存
        with open("todos.json", "w", encoding="utf-8") as f:
            # 把每个 Task 对象转成字典，组成一个列表
            data = [t.to_dict() for t in self.tasks]
            # 用 json.dump 把数据写入文件
            # ensure_ascii=False 让中文原样保存，indent=2 让文件格式好看
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("已保存")

    # 从 JSON 文件加载任务
    def load(self):
        # 用 try/except 捕获文件不存在的情况
        try:
            # 打开文件，模式 "r" 表示读取
            with open("todos.json", "r", encoding="utf-8") as f:
                # 从文件读取 JSON 数据，转成 Python 的列表/字典
                data = json.load(f)
            # 把读出来的字典列表，逐个转换成 Task 对象，重新赋值给 self.tasks
            self.tasks = [Task(item["id"], item["title"], item["done"]) for item in data]
            # 如果读到了任务，就把 next_id 设为当前最大 id 加 1
            if self.tasks:
                self.next_id = max(t.id for t in self.tasks) + 1
            # 打印读取到的任务数量
            print("已读取", len(self.tasks), "条任务")
        except FileNotFoundError:
            # 如果文件不存在，说明是第一次运行，从空列表开始
            print("还没有存档，从空开始")


# 这个判断表示：只有直接运行这个文件时，才执行下面的代码
# 如果别人 import 这个文件，下面的代码不会自动执行
if __name__ == "__main__":
    # 创建一个 TaskList 对象
    tl = TaskList()
    # 尝试从文件加载已有任务
    tl.load()
    # 添加两个测试任务
    tl.add("学 Python")
    tl.add("刷 LeetCode")
    # 显示所有任务
    tl.show()
    # 保存任务到文件
    tl.save()