from Dream.models import Document as dp
import os

m_list = os.listdir(r'C:\Users\kjuk0\Desktop\multiple\media')
for each in m_list:
    dp.objects.create(title='each', file=each)