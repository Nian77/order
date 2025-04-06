
import os

INPUT_FILE = "orders.json"
OUTPUT_FILE = "output_orders.json"


def load_data(filename):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_data(filename, data):
    """將 data（list）以 JSON 格式寫回指定檔案。"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def is_positive_int(s):
    """檢查字串 s 是否能轉為正整數，若可以則回傳 True。"""
    if not s.isdigit():
        return False
    # s 為純數字時，進一步檢查是否 > 0
    return int(s) > 0


def add_order():
    """新增訂單並寫入 orders.json。"""
    orders = load_data(INPUT_FILE)

    # 訂單編號
    while True:
        order_id = input("請輸入訂單編號(例如 O001)：").strip()
        if not order_id:
            print("訂單編號不可為空，請重新輸入。")
            continue
        order_id = order_id.upper()  # 轉大寫

        if any(o["order_id"] == order_id for o in orders):
            print(f"訂單編號 {order_id} 已存在！請重新輸入。")
            continue
        break

    customer_name = input("請輸入顧客姓名：").strip()
    if not customer_name:
        customer_name = "未命名顧客"  
    items = []
    while True:
        item_name = input("\n請輸入商品名稱(按 Enter 直接結束輸入商品)：").strip()
        if not item_name:
            break

        price_str = input("請輸入商品價格：").strip()
        if not is_positive_int(price_str):
            print("【錯誤】商品價格必須為正整數，請重新輸入此商品。")
            continue

        quantity_str = input("請輸入商品數量：").strip()
        if not is_positive_int(quantity_str):
            print("【錯誤】商品數量必須為正整數，請重新輸入此商品。")
            continue

        price = int(price_str)
        quantity = int(quantity_str)
        items.append({
            "name": item_name,
            "price": price,
            "quantity": quantity
        })

    if len(items) == 0:
        print("未輸入任何商品，此筆訂單不建立。")
        return

    new_order = {
        "order_id": order_id,
        "customer": customer_name,
        "items": items
    }
    orders.append(new_order)
    save_data(INPUT_FILE, orders)
    print(f"\n訂單 {order_id} 已新增完成，存入 {INPUT_FILE}。\n")


def print_order_report(orders):
    if not orders:
        print("目前無任何訂單資料。")
        return

    for idx, order in enumerate(orders, start=1):
        print("=" * 50)
        print(f"[訂單 {idx}] 編號：{order['order_id']} | 客戶：{order['customer']}")
        items = order.get("items", [])
        total_amount = 0
        for item in items:
            item_name = item["name"]
            price = item["price"]
            quantity = item["quantity"]
            subtotal = price * quantity
            total_amount += subtotal
            print(f"  - {item_name} / NT${price:,} x {quantity} = NT${subtotal:,}")
        print(f"  >>> 總金額：NT${total_amount:,}")
    print("=" * 50)


def show_orders():
    orders = load_data(INPUT_FILE)
    if not orders:
        print("目前沒有尚未出餐的訂單。")
    else:
        print("\n---【尚未出餐的訂單報表】---")
        print_order_report(orders)


def process_order():
    orders = load_data(INPUT_FILE)
    if not orders:
        print("目前沒有尚未出餐的訂單。")
        return

    # 列出簡易清單
    print("\n---【目前尚未出餐的訂單列表】---")
    for i, o in enumerate(orders, start=1):
        print(f"{i}. 訂單編號：{o['order_id']} / 客戶：{o['customer']}")

    # 輸入要處理的序號
    while True:
        choice = input("\n請輸入要出餐的訂單「序號」(按 Enter 取消)：").strip()
        if not choice:  # 按下 Enter 代表取消
            print("已取消出餐操作。")
            return
        if not choice.isdigit():
            print("請輸入有效的數字序號。")
            continue

        idx = int(choice)
        if idx < 1 or idx > len(orders):
            print("序號超出範圍，請重新輸入。")
            continue
        break

    # 將訂單搬移到 output_orders.json
    target_order = orders.pop(idx - 1)  # 移除指定訂單
    save_data(INPUT_FILE, orders)

    completed_orders = load_data(OUTPUT_FILE)
    completed_orders.append(target_order)
    save_data(OUTPUT_FILE, completed_orders)

    print(f"\n已成功出餐，以下為該筆訂單明細：")
    print_order_report([target_order])


def main():
    """主程式入口，顯示選單並執行對應功能。"""
    while True:
        print("\n***************選單***************")
        print("1. 新增訂單")
        print("2. 顯示訂單報表")
        print("3. 出餐處理")
        print("4. 離開")
        print("**********************************")
        choice = input("請選擇操作項目(Enter 離開)：").strip()

        # 若按下 Enter 直接離開
        if choice == "":
            print("程式結束，感謝使用。")
            break

        if choice == "1":
            add_order()
        elif choice == "2":
            show_orders()
        elif choice == "3":
            process_order()
        elif choice == "4":
            print("程式結束，感謝使用。")
            break
        else:
            print("輸入錯誤，請重新選擇。")


if __name__ == "__main__":
    main()

