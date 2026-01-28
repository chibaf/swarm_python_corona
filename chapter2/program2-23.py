i=0

while i<50:
    print(i)
    i = i + 1 #iに1を加える．

    if i==7:
        print("このままだと50回ほどループ処理するので，iが7のときに抜け出す．")
        break #while文から抜け出す．

print("while文から脱出成功！！")