import sys

vis = {}

def main():
    file_out = open("./data/xh.txt","w+")
    with open("./data/xuehao.txt","r") as file_in:
        for user in file_in.readlines():
            user = user.strip('\n')
            if user not in vis:
                vis[user] = 1
                print(user,file=file_out)
    file_out.close()

if __name__ == "__main__":
    main()
else:
    pass