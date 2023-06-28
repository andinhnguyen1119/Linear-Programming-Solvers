import pulp
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable, GLPK, LpMinimize


def nhap_Min_Max():
    print("\nBài toán tìm Min mời nhập vào 0, bài toán tìm Max mời nhập vào 1:")
    sense = int(input())
    while(sense!=0 and sense!=1):
        print("\nBạn đã nhập sai! Xin vui lòng nhập lại yêu cầu bài toán.")
        print("\nBài toán tìm Min mời nhập vào 0, bài toán tìm Max mời nhập vào 1:")
        sense = int(input())
    return sense

def nhap_so_luong_bien():
    print("\nNhập vào số lượng biến của bài toán:")
    n = int(input())
    while(n<=1):
        print("\nSố lượng biến của bài toán tối thiếu bằng 2")
        print("\nBạn đã nhập sai! Xin vui lòng nhập lại số lượng biến của bài toán.")
        n = int(input())
    return n

def nhap_rang_buoc_dau(n):
    a = [[0] * 2 for i in range(n)]
    for i in range(n):
        print("\nNhập khoảng giá trị của x(" + str(i+1) + ") : ")
        for j in range(2):
            a[i][j] = input()
    return a


def nhap_rang_buoc_bien():
    print("\nNhập vào các hệ số của ràng buộc biến theo ma trận:")
    print("\nNhập vào số dòng của ma trận:")
    n = int(input())
    while(n<1):
        print("\nMời nhập lại số dòng của ma trận! Số dòng phải là số dương:")
        n = int(input())
    print("\nNhập vào số cột của ma trận:")
    m = int(input())
    while(m<1):
        print("\nMời nhập lại số cột của ma trận! Số cột phải là số dương:")
        m = int(input())
    a = [[0] * m for i in range(n)]
    print("Nhập vào các hệ số theo thứ tự từ trái sang phải, từ trên xuống dưới:")
    for i in range(n):
        for j in range(m):
            print("a[" + str(i) +"][" +str(j)+"] = ")
            a[i][j] = int(input())
    return a

def nhap_ham_muc_tieu(n):
    print("\nNhập vào các hệ số của hàm mục tiêu theo thứ tự của các biến:")
    a = [[0] * n for i in range(1)]
    for i in range(1):
        for j in range(n):
            a[i][j] = int(input())
    return a

def main():
    # Define the model
    min_max = nhap_Min_Max()

    if min_max == 1:
        model = LpProblem(name="Max", sense=LpMaximize)
    else:
        model = LpProblem(name="Min", sense=LpMinimize)

    # Define the decision variables
    so_luong_bien = nhap_so_luong_bien()
    rang_buoc_dau = nhap_rang_buoc_dau(so_luong_bien)

    x = {}
    for i in range(1, so_luong_bien + 1):
        if (rang_buoc_dau[i - 1][0] == "inf" and rang_buoc_dau[i - 1][1] != "inf"):
            x[i] = LpVariable(name=f"x{i}", lowBound=None, upBound=int(rang_buoc_dau[i - 1][1]))
        elif (rang_buoc_dau[i - 1][0] != "inf" and rang_buoc_dau[i - 1][1] == "inf"):
            x[i] = LpVariable(name=f"x{i}", lowBound=int(rang_buoc_dau[i - 1][0]), upBound=None)
        elif (rang_buoc_dau[i - 1][0] == "inf" and rang_buoc_dau[i - 1][1] == "inf"):
            x[i] = LpVariable(name=f"x{i}", lowBound=None, upBound=None)
        else:
            if (rang_buoc_dau[i - 1][0] != "inf" and rang_buoc_dau[i - 1][1] != "inf"):
                x[i] = LpVariable(name=f"x{i}", lowBound=int(rang_buoc_dau[i - 1][0]),
                                  upBound=int(rang_buoc_dau[i - 1][1]))

    a = nhap_rang_buoc_bien()

    for i in range(len(a)):
        temp1 = 0
        j = 0
        while (j < so_luong_bien):
            temp1 = temp1 + a[i][j] * x[j + 1]
            j = j + 1
        temp2 = a[i][j]
        print("\nNhập dấu của ràng buộc thứ " + str(i+1))
        dau = input()
        match dau:
            case "<":
                model += (temp1 < temp2)

            case ">":
                model += (temp1 > temp2)

            case ">=":
                model += (temp1 >= temp2)

            case "<=":
                model += (temp1 <= temp2)

            case "=":
                model += (temp1 == temp2)
            case _:
                print("\nCú pháp dấu không hợp lệ!")

    b = nhap_ham_muc_tieu(so_luong_bien)
    temp = 0
    j = 0
    for i in range(so_luong_bien):
        temp = temp + b[j][i] * x[i + 1]
    model += temp

    # Solve the optimization problem
    status = model.solve()

    # Get the results
    print(f"status: {model.status}, {LpStatus[model.status]}")
    if (model.status == 1):
        print(f"The math is optimal. Objective: {model.objective.value()}")
        for var in x.values():
            print(f"{var.name}: {var.value()}")

    if (model.status == -2):
        if min_max == 1:
            print(f"The math is unbounded. Objective: max = inf")
        else:
            print(f"The math is unbounded. Objective: min = -inf")

    if (model.status == -1):
        print(f"The math is infeasible ")

    if (model.status == -3):
        print(f"The math is undefined ")

    if (model.status == 0):
        print(f"The math is not solved ")


if __name__ == "__main__":
    main()
