from main_handler import MainHandler

test_01 = MainHandler(path="img.png", password="password")
test_01.encrypt()

test_02 = MainHandler(path="img.png.bin", password="password")
test_02.decrypt()
