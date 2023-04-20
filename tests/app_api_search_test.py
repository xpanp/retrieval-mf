import sys
sys.path.append('../')
from app.api.search import check_and_intercept
import shutil

# 1.jpg 500*333
shutil.copyfile('1.jpg', '2.jpg')
print(check_and_intercept('2.jpg', 0, 0, 100, 332))