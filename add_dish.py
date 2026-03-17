import json
import os

def add_dish():
    file_path = 'menu.json'
    
    # 1. 读取现有的菜单文件
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except:
                data = {"dishes": []}
    else:
        data = {"dishes": []}

    # 2. 让你输入新菜的信息
    print("\n=== 我的私人厨房 · 加菜系统 ===")
    name = input("请输入菜名: ")
    desc = input("请输入菜品描述: ")
    price = input("请输入价格 (直接回车默认0元): ") or "0"

    # 3. 组合成新菜数据
    new_item = {
        "id": len(data["dishes"]) + 1,
        "name": name,
        "description": desc,
        "price": price
    }

    # 4. 保存回文件
    data["dishes"].append(new_item)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 成功！'{name}' 已经加入菜单。")

if __name__ == "__main__":
    add_dish()