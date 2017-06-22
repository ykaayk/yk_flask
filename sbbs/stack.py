# coding:utf8

# 栈: 后进先出，尾进尾出，单向死胡同
# queue = []
#
#
# def pushit():
#     queue.append(raw_input('Enter new string: ').strip())
#
#
# def popit():
#     if len(queue) == 0:
#         print 'Cannot pop from an empty queue'
#     else:
#         print 'Removed [', queue.pop(), ']'
#
#
# def viewqueue():
#     print queue  # calls str() internally
#
#
# CMDs = {'u': pushit, 'o': popit, 'v': viewqueue}
#
#
# def showmenu():
#     pr = '''
#     p(U)sh
#     p(O)p
#     (V)iew
#     (Q)uit
#
#     Enter choice:'''
#
#     while True:
#         while True:
#             try:
#                 choice = raw_input(pr).strip()[0].lower()
#             except (EOFError, KeyboardInterrupt, IndexError):
#                 choice = 'q'
#
#             print '\nYou picked: [%s]' % choice
#             if choice not in 'uovq':
#                 print 'Invalid option, try again!'
#             else:
#                 break
#
#         if choice == 'q':
#             break
#
#         CMDs[choice]()


# 队列：先进先出，尾进头出，单向车道
# queue = []
#
#
# def enQ():
#     queue.append(raw_input('Enter new string: ').strip())
#
#
# def deQ():
#     if len(queue) == 0:
#         print 'Cannot pop from an empty queue'
#     else:
#         print 'Removed [', queue.pop(0), ']'
#
#
# def viewQ():
#     print queue  # calls str() internally
#
#
# CMDs = {'e': enQ, 'd': deQ, 'v': viewQ}
#
#
# def showmenu():
#     pr = '''
#     (E)nqueue
#     (D)equeue
#     (V)iew
#     (Q)uit
#
#     Enter choice:'''
#
#     while True:
#         while True:
#             try:
#                 choice = raw_input(pr).strip()[0].lower()
#             except (EOFError, KeyboardInterrupt, IndexError):
#                 choice = 'q'
#
#             print '\nYou picked: [%s]' % choice
#             if choice not in 'devq':
#                 print 'Invalid option, try again!'
#             else:
#                 break
#
#         if choice == 'q':
#             break
#
#         CMDs[choice]()
#
#
# if __name__ == '__main__':
#     showmenu()















