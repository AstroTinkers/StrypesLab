display_num = "-65"
for num in display_num[1:]:
    if num.isdigit():
        display_num2 = display_num[:display_num.index(num)+1]

    else:
        break
display_num = display_num2
print(display_num)